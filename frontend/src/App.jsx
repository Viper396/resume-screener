import { useState } from "react";
import AppHeader from "./components/AppHeader";
import HowItWorksCard from "./components/HowItWorksCard";
import ResumeForm from "./components/ResumeForm";
import ResultsPanel from "./components/results/ResultsPanel";
import { scoreResume } from "./services/resumeApi";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileChange = ({ file, error: fileError }) => {
    setSelectedFile(file);
    setError(fileError || "");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile || !jobDescription.trim()) {
      return;
    }

    setError("");
    setIsLoading(true);

    try {
      const payload = await scoreResume({ file: selectedFile, jobDescription });
      setResult(payload);
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setJobDescription("");
    setResult(null);
    setError("");
    setIsLoading(false);
  };

  return (
    <main className="min-h-screen bg-grid px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-5xl">
        <AppHeader />

        <section className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <ResumeForm
            selectedFile={selectedFile}
            jobDescription={jobDescription}
            isLoading={isLoading}
            error={error}
            onFileChange={handleFileChange}
            onJobDescriptionChange={setJobDescription}
            onSubmit={handleSubmit}
          />
          <HowItWorksCard onReset={resetForm} />
        </section>

        {result && <ResultsPanel result={result} />}
      </div>
    </main>
  );
}

export default App;
