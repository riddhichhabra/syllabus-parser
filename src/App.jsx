import { useState } from "react";
import Header from "./components/Header";
import UploadForm from "./components/UploadForm";
import Results from "./components/Results";

function App() {
    const [file, setFile] = useState(null);
    const [data, setData] = useState([]);

    const handleUpload = async (e) => {
        e.preventDefault();

        if (!file){
            return alert("Please upload a PDF file first!");
        }

        // Add for what happens on upload here!
        const parsedData = [];
        setData(parsedData);
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
