import { useState } from "react";

function UploadForm() {
    const [file, setFile] = useState(null);

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!file){
            return alert("Please upload a PDF file first!");
        }

        // Add function for what happens on submitting
    };

  return (
    <form 
        onSubmit={handleSubmit}
        className="mb-4 flex flex-col items-center"
    >
      <input 
        type="file" 
        accept=".pdf"
        onChange={(e)=>setFile(e.target.files[0])}
        className="border p-2" 
    />
      <button type="submit" className="mt-1 ml-2 px-4 py-2 bg-[#500000] text-white rounded hover:bg-[#8d7b7b] transition">
        Upload & Parse
      </button>
    </form>
  );
}

export default UploadForm;
