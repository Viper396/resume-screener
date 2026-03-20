import { useState } from "react";
import { scoreResume } from "../services/resumeApi";

const DEFAULT_ROLE = "software_engineer";

export function useResumeAnalyzer() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedRole, setSelectedRole] = useState(DEFAULT_ROLE);
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
      const payload = await scoreResume({
        file: selectedFile,
        jobDescription,
        role: selectedRole,
      });
      setResult(payload);
    } catch (submitError) {
      setError(submitError.message);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setSelectedRole(DEFAULT_ROLE);
    setJobDescription("");
    setResult(null);
    setError("");
    setIsLoading(false);
  };

  return {
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
  };
}
