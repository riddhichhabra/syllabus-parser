import { useState } from "react";
import Header from "./components/Header";
import UploadForm from "./components/UploadForm";
import Results from "./components/Results";

function App() {
    const [file, setFile] = useState(null);
    const [data, setData] = useState([]);
    const API_URL = "https://syllabus-parser.onrender.com";

    const handleUpload = async (e) => {
        e.preventDefault();

        if (!file){
            return alert("Please upload a PDF file first!");
        }

        // Add for what happens on upload here!

        const fileData = new FormData();
        fileData.append('file', file);
        
        try{
          const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: fileData
          });

          if (response.ok){
            const parsedData = await response.json();
            setData(parsedData);
            // do smth
          }
          else{
            // Handle this
          }
        } catch(error){
          // Handle try not working
        }
    };

    return (
      <>
        <Header />
        <div className="min-h-screen bg-[#e4dccf] flex flex-col items-center p-6">
          <UploadForm 
            file={file} 
            setFile={setFile} 
            handleUpload={handleUpload}
          />
          <Results 
            data={data}
          />
        </div>
      </>
    );
  }

export default App;
