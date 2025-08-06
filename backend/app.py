from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import fitz
import os
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv
import json
import re
from ics import Calendar, Event
import string

# load_dotenv()
# api_key = os.getenv("PERPLEXITY_API_KEY")

api_key = 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

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CALENDAR_FOLDER = 'calendar_files'
os.makedirs(CALENDAR_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Flask server is up and running!"

@app.route('/upload', methods=['POST'])
def uploadFile():
    print("Headers:", request.headers)
    print("Files:", request.files)
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error":"No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    text = extractTextFromPDF(file_path=file_path)
    structured_resp = analyzeSyllabus(text)

    mock_data = [
        {
            "course": "CSCE 120",
            "exams": [
                {"title": "midterm 1", "date": "2025-10-10"},
                {"title": "midterm 2", "date": "2025-11-10"},
                {"title": "final", "date": "2025-12-10"}
            ]
        }
    ]

    generateCalFiles(structured_resp)

    return jsonify(structured_resp)

@app.route("/download/<filename>")
def downloadCalendar(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(CALENDAR_FOLDER, filename)
    return send_file(file_path, as_attachment=True)


def generateCalFiles(exam_data, cal_folder=CALENDAR_FOLDER):

    for course in exam_data:
        course_name = course["course"].replace(" ", "_")

        for exams in course["exams"]:
            title = exams["title"]
            date = exams["date"]

            c = Calendar()
            e = Event()

            e.name = f"{course_name} - {title}"
            e.begin = date
            c.events.add(e)

            cal_file = course_name + title.replace(" ", "_") + ".ics"
            cal_file2 = safe_filename(cal_file)
            cal_file_path = os.path.join(cal_folder, cal_file2)
            exams["filename"] = cal_file2
            with open (cal_file_path, 'w') as f:
                f.writelines(c.serialize_iter())

def extractTextFromPDF(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    os.remove(file_path)
    return text

def analyzeSyllabus(text):
    url ="https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Given this syllabus text, extract a schedule of all exams.
For each exam, include the title (like "Midterm 1", "Final Exam", etc.) and the date in YYYY-MM-DD format.
If there are multiple sections of a course with different final exam dates, include the section number in parentheses after the title, like:
"title": "Final Exam (Section 281)".

If the **final exam date is not explicitly mentioned**, infer it based on the course’s regular meeting days and times using the following final exam schedule:

### December 11
- 7:30–9:30 a.m. → MW 5:45–7:00 p.m. or MW 7:30–8:45 p.m.
- 10:00–12:00 p.m. → MWF 8:00–8:50 a.m. or MWF 8:35–9:25 a.m.
- 12:30–2:30 p.m. → TR 9:35–10:50 a.m. or TR 10:20–11:35 a.m.
- 3:00–5:00 p.m. → TR 11:10–12:25 p.m. or TR 11:55–1:10 p.m.

### December 12
- 8:00–10:00 a.m. → MWF 9:10–10:00 a.m. or MWF 9:45–10:35 a.m.
- 10:30–12:30 p.m. → MWF 12:40–1:30 p.m. or MWF 1:15–2:05 p.m.
- 1:00–3:00 p.m. → TR 8:00–9:15 a.m. or TR 8:45–10:00 a.m.
- 3:30–5:30 p.m. → MW 4:10–5:25 p.m. or MW 5:55–7:20 p.m.
- 6:00–8:00 p.m. → MW 7:20–8:35 p.m. or MW 9:05–10:20 p.m.

### December 15
- 8:00–10:00 a.m. → MWF 10:20–11:10 a.m. or MWF 10:55–11:45 a.m.
- 10:30–12:30 p.m. → MWF 3:00–3:50 p.m. or MW 4:20–5:35 p.m.
- 1:00–3:00 p.m. → TR 3:55–5:10 p.m. or TR 4:40–5:55 p.m.
- 3:30–5:30 p.m. → MWF 1:50–2:40 p.m. or MW 2:25–3:40 p.m.
- 6:00–8:00 p.m. → TR 7:05–8:20 p.m. or TR 7:50–9:05 p.m.

### December 16
- 8:00–10:00 a.m. → TR 12:45–2:00 p.m. or TR 1:30–2:45 p.m.
- 10:30–12:30 p.m. → MWF 11:30–12:20 p.m. or MWF 12:05–12:55 p.m.
- 1:00–3:00 p.m. → TR 2:20–3:35 p.m. or TR 3:05–4:20 p.m.
- 3:30–5:30 p.m. → TR 5:30–6:45 p.m. or TR 6:15–7:30 p.m.

Only return valid JS Object structured so: . Do not include any explanation or commentary.
Return the result in the following format:
[
    {{
        "course": "COURSE NAME",
        "exams" : [
            {{
                "title": "Midterm 1",
                "date": "YYYY-MM-DD"
            }},
            {{
                "title": "Final Exam (Section XYZ)",
                "date": "YYYY-MM-DD"
            }}
        ]
    }}
]

Syllabus: {text}
"""

    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "user", 
                "content" : prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        raw_content = response.json()["choices"][0]["message"]["content"]
        clean_content = re.sub(r"```json|```", "", raw_content).strip()
        try:
            return json.loads(clean_content)  # safely convert to Python object
        except json.JSONDecodeError:
            print("Failed to parse JSON:", clean_content)
            return {"error": "Could not parse LLM output"}
    else:
        print("Perplexity API error:", response.text)
        return "Error: Could not analyze syllabus."

def safe_filename(name):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return ''.join(c if c in valid_chars else '_' for c in name)

if __name__ == "__main__":
    app.run(debug=True)