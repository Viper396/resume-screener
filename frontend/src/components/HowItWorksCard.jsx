function HowItWorksCard({ onReset }) {
  return (
    <aside className="rounded-3xl border border-slate-200 bg-white/95 p-6 shadow-xl shadow-slate-900/10 sm:p-7">
      <h3 className="text-xl font-semibold text-slate-900">How This Works</h3>
      <ul className="mt-4 space-y-3 text-sm text-slate-700">
        <li>1. Upload your resume file.</li>
        <li>2. Paste target job description.</li>
        <li>3. Review JD match percentage and missing keywords.</li>
        <li>4. Improve and re-run to optimize ATS alignment.</li>
      </ul>
      <button
        type="button"
        onClick={onReset}
        className="mt-6 rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-cyan-600 hover:text-cyan-700"
      >
        Reset Analyzer
      </button>
    </aside>
  );
}

export default HowItWorksCard;
