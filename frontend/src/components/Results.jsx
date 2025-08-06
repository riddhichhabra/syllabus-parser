const API_URL = "https://riddhic.pythonanywhere.com";

function Results({ data }) {
    if (!data || data.length === 0){
        return (
            <div className="mt-8 w-[50vw] max-w-full bg-white p-4 rounded-xl shadow-sm items-center">
                <h2 className="text-2xl font-semibold text-[#500000] mb-4 items-center"> <center> Exam Schedule</center></h2>
                <span className="text-gray-500"> <center> Upload a syllabus to see the exam schedule!</center></span>
            </div>
        );
    }
    
    return (
        <div className="mt-8 w-[50vw] max-w-full bg-white p-4 rounded-xl shadow-sm">
        <h2 className="text-2xl font-semibold text-[#500000] mb-4 items-center"><center>Exam Schedule</center></h2>
        <ul>
            {data.map((exam, index) => (
            <li
                key={index}
                className="flex justify-between py-2 border-b border-gray-200 last:border-none"
            >
                <span>{exam.course}</span>
                <span className="text-gray-500">
                    <ul>
                        {exam.exams.map((item,index)=> (
                            <li key={index} className="text-gray-500 flex flex-col">
                                <h4> {item.title}: {item.date} </h4>
                                <a href={`${API_URL}/download/${item.filename}`} download className="text-blue-500"> <button> Download Calendar </button> </a>
                            </li>
                        ))}
                    </ul>
                </span>
            </li>
            ))}
        </ul>
        </div>
    );
}

export default Results;
