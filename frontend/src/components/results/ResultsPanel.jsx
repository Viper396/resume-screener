import { useMemo } from "react";
import BreakdownRow from "./BreakdownRow";
import KeywordList from "./KeywordList";

function ResultsPanel({ result }) {
  const scoreCircleStyle = useMemo(() => {
    const score = result?.overall_score || 0;
    return {
      background: `conic-gradient(#0891b2 ${score * 3.6}deg, #dbeafe 0deg)`,
    };
  }, [result]);

  return (
    <section className="mt-8 rounded-3xl border border-slate-200 bg-white/95 p-6 shadow-xl shadow-slate-900/10 sm:p-7">
      <div className="grid gap-6 lg:grid-cols-[230px_1fr] lg:items-center">
        <div
          className="mx-auto flex w-45 items-center justify-center rounded-full p-2"
          style={scoreCircleStyle}
        >
          <div className="flex h-40 w-40 flex-col items-center justify-center rounded-full bg-white text-center">
            <p className="text-4xl font-bold text-slate-900">
              {result.overall_score}
            </p>
            <p className="text-sm font-semibold uppercase tracking-wide text-cyan-700">
              Grade {result.grade}
            </p>
          </div>
        </div>

        <div>
          <h3 className="text-2xl font-semibold text-slate-900">
            ATS Score Breakdown
          </h3>
          <div className="mt-4 space-y-3">
            {result.breakdown.jd_match !== undefined && (
              <BreakdownRow
                label="JD Match"
                value={result.breakdown.jd_match}
              />
            )}
            <BreakdownRow label="Sections" value={result.breakdown.sections} />
            <BreakdownRow label="Keywords" value={result.breakdown.keywords} />
            <BreakdownRow
              label="Formatting"
              value={result.breakdown.formatting}
            />
            <BreakdownRow label="Length" value={result.breakdown.length} />
            <BreakdownRow
              label="Contact"
              value={result.breakdown.contact_info}
            />
          </div>
        </div>
      </div>

      {result.jd_match && (
        <div className="mt-7 rounded-2xl border border-slate-200 bg-slate-50 p-5">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h4 className="text-lg font-semibold text-slate-900">
              Job Description Keyword Matching
            </h4>
            {result.jd_match.selected_role_label && (
              <span className="rounded-full border border-cyan-300 bg-cyan-100 px-3 py-1 text-xs font-semibold text-cyan-900">
                Role: {result.jd_match.selected_role_label}
              </span>
            )}
          </div>
          <p className="mt-1 text-sm text-slate-700">
            Matched {result.jd_match.matched_keywords.length} of{" "}
            {result.jd_match.total_keywords_considered} extracted JD keywords.
          </p>
          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            <KeywordList
              title="Matched Keywords"
              items={result.jd_match.matched_keywords}
              emptyText="No strong keyword matches found yet"
            />
            <KeywordList
              title="Missing Keywords"
              items={result.jd_match.missing_keywords}
              emptyText="No major missing keywords detected"
            />
          </div>
        </div>
      )}

      <div className="mt-7 rounded-2xl border border-amber-200 bg-amber-50 p-5">
        <h4 className="text-lg font-semibold text-slate-900">
          Recommendations
        </h4>
        <ul className="mt-3 space-y-2 text-sm text-slate-700">
          {result.feedback.map((item) => (
            <li key={item} className="rounded-lg bg-white px-3 py-2">
              {item}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default ResultsPanel;
