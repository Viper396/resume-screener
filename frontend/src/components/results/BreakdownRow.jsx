function BreakdownRow({ label, value }) {
  return (
    <div className="grid grid-cols-[110px_1fr_48px] items-center gap-3 text-sm">
      <span className="font-medium text-slate-700">{label}</span>
      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-linear-to-r from-cyan-500 to-teal-500 transition-all duration-700"
          style={{ width: `${value}%` }}
        />
      </div>
      <span className="text-right font-semibold text-slate-700">{value}</span>
    </div>
  );
}

export default BreakdownRow;
