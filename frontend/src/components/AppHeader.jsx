function AppHeader() {
  return (
    <header className="mb-8 rounded-3xl bg-linear-to-r from-cyan-700 via-teal-700 to-emerald-700 p-8 text-white shadow-2xl shadow-cyan-900/30">
      <p className="mb-2 text-xs uppercase tracking-[0.3em] text-cyan-100">
        ATS Resume Screener
      </p>
      <h1 className="text-3xl font-bold leading-tight sm:text-4xl">
        Match Resume To Job Description
      </h1>
      <p className="mt-2 max-w-2xl text-sm text-cyan-50 sm:text-base">
        Upload your resume, paste a job description, and instantly see keyword
        match percentage with actionable ATS feedback.
      </p>
    </header>
  );
}

export default AppHeader;
