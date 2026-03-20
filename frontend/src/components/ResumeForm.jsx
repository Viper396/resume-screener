import { useState } from "react";
import { validateResumeFile } from "../utils/validateResumeFile";

function ResumeForm({
  selectedFile,
  jobDescription,
  isLoading,
  error,
  onFileChange,
  onJobDescriptionChange,
  onSubmit,
}) {
  const [dragActive, setDragActive] = useState(false);

  const isSubmitDisabled = !selectedFile || !jobDescription.trim() || isLoading;

  const handleFileChange = (file) => {
    const validationError = validateResumeFile(file);
    if (validationError) {
      onFileChange({ file: null, error: validationError });
      return;
    }

    onFileChange({ file, error: "" });
  };

  return (
    <form
      onSubmit={onSubmit}
      className="rounded-3xl border border-slate-200 bg-white/95 p-6 shadow-xl shadow-slate-900/10 sm:p-7"
    >
      <h2 className="text-xl font-semibold text-slate-900">
        Analyze Your Resume
      </h2>
      <p className="mt-1 text-sm text-slate-600">
        Supports PDF, DOCX, TXT (max 16MB)
      </p>

      <div
        className={`mt-5 rounded-2xl border-2 border-dashed p-6 text-center transition ${
          dragActive
            ? "border-cyan-500 bg-cyan-50"
            : "border-slate-300 bg-slate-50"
        }`}
        onDragOver={(event) => {
          event.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragActive(false);
          handleFileChange(event.dataTransfer.files?.[0]);
        }}
      >
        <p className="text-sm font-medium text-slate-700">
          Drag and drop your resume here
        </p>
        <p className="mt-1 text-xs text-slate-500">or choose a file</p>
        <label className="mt-3 inline-flex cursor-pointer rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-cyan-700">
          Browse File
          <input
            type="file"
            className="hidden"
            accept=".pdf,.docx,.txt"
            onChange={(event) => handleFileChange(event.target.files?.[0])}
          />
        </label>
      </div>

      {selectedFile && (
        <div className="mt-4 flex items-center justify-between rounded-xl border border-cyan-200 bg-cyan-50 px-4 py-2 text-sm text-cyan-900">
          <span className="truncate pr-3">{selectedFile.name}</span>
          <button
            type="button"
            onClick={() => onFileChange({ file: null, error: "" })}
            className="rounded-full bg-cyan-800 px-2 py-1 text-xs font-semibold text-white hover:bg-cyan-900"
          >
            Remove
          </button>
        </div>
      )}

      <label className="mt-5 block text-sm font-semibold text-slate-800">
        Job Description
      </label>
      <textarea
        value={jobDescription}
        onChange={(event) => onJobDescriptionChange(event.target.value)}
        rows={8}
        placeholder="Paste the full job description for accurate keyword matching..."
        className="mt-2 w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm outline-none ring-cyan-200 transition focus:border-cyan-500 focus:ring"
      />

      {error && (
        <p className="mt-3 rounded-lg bg-rose-100 px-3 py-2 text-sm font-medium text-rose-700">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={isSubmitDisabled}
        className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-2xl bg-linear-to-r from-cyan-600 to-teal-600 px-5 py-3 text-sm font-semibold text-white transition hover:from-cyan-700 hover:to-teal-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isLoading && (
          <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
        )}
        {isLoading ? "Analyzing..." : "Analyze Resume"}
      </button>
    </form>
  );
}

export default ResumeForm;
