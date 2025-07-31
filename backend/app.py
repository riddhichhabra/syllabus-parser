from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz
import os
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv
import json
import re

load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    return jsonify(structured_resp)


def extractTextFromPDF(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def analyzeSyllabus(text):
    url ="https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
                Given this syllabus text, extract a schedule of all exams. 
                For each exam, include the title, like midterm 1, midterm 2, final etc, and date.
                Return the output strictly in the following JSON format: 
                [
                    {{
                        "course": "COURSE NAME",
                        "exams" : [
                            {{
                                "title": "EXAM TITLE (like midterm 1)",
                                "date": "YYYY-MM-DD"
                            }},
                            {{
                                "title": "EXAM TITLE (like midterm 1)",
                                "date": "YYYY-MM-DD"
                            }}
                            , ...
                        ]
                    }}
                ]
                Only return valid JSON. Do not include any commentary or explanation.

                Syllabus: {text} """

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

if __name__ == "__main__":
    app.run(debug=True)