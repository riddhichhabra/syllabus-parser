import Header from "./components/Header";
import UploadForm from "./components/UploadForm";
import Results from "./components/Results";

function App() {
  return (
    <>
      <Header />
      <div className="min-h-screen bg-[#e4dccf] flex flex-col items-center p-6">
        <UploadForm />
        <Results />
      </div>
    </>
  );
}

export default App;
