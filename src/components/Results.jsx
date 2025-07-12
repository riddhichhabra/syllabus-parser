function Results({ data }) {
    const mockData = [
        {
            course: "CSCE 120",
            exams: [
                {
                    title:"midterm 1",
                    date:"2025-10-10"
                },
                {
                    title:"midterm 2",
                    date:"2025-11-10"
                }
            ]
        },
        {
            course: "MATH 151",
            exams: [
                {
                    title:"midterm 1",
                    date:"2025-10-8"
                },
                {
                    title:"midterm 2",
                    date:"2025-11-8"
                }
            ]
        }
    ];

    if (!data || data.length === 0){
        return (
            <div className="mt-8 w-full max-w-md bg-white p-4 rounded-xl shadow-sm items-center">
                <h2 className="text-2xl font-semibold text-[#500000] mb-4 items-center"> <center> Exam Schedule</center></h2>
                <span className="text-gray-500"> <center> Upload a syllabus to see the exam schedule!</center></span>
            </div>
        );
    }

    // change mockData to data later
    
    return (
        <div className="mt-8 w-full max-w-md bg-white p-4 rounded-xl shadow-sm">
        <h2 className="text-2xl font-semibold text-[#500000] mb-4 items-center"><center>Exam Schedule</center></h2>
        <ul>
            {mockData.map((exam, index) => (
            <li
                key={index}
                className="flex justify-between py-2 border-b border-gray-200 last:border-none"
            >
                <span>{exam.course}</span>
                <span className="text-gray-500">
                    <ul>
                        {exam.exams.map((item,index)=> (
                            <li key={index} className="text-gray-500">
                                {item.title}: {item.date}
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
