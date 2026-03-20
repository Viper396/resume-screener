import AppHeader from "./components/AppHeader";
import HowItWorksCard from "./components/HowItWorksCard";
import ResumeForm from "./components/ResumeForm";
import ResultsPanel from "./components/results/ResultsPanel";
import { useResumeAnalyzer } from "./hooks/useResumeAnalyzer";

function App() {
  const {
    selectedFile,
    selectedRole,
    jobDescription,
    isLoading,
    result,
    error,
    handleFileChange,
    setSelectedRole,
    setJobDescription,
    handleSubmit,
    resetForm,
  } = useResumeAnalyzer();

  return (
    <main className="min-h-screen bg-grid px-4 py-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-5xl">
        <AppHeader />

        <section className="grid gap-6 lg:grid-cols-[1.2fr_1fr]">
          <ResumeForm
            selectedFile={selectedFile}
            selectedRole={selectedRole}
            jobDescription={jobDescription}
            isLoading={isLoading}
            error={error}
            onFileChange={handleFileChange}
            onRoleChange={setSelectedRole}
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
