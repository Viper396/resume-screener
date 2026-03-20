function KeywordList({ title, items, emptyText }) {
  const displayItems = items.length > 0 ? items : [emptyText];

  return (
    <div>
      <h4 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-700">
        {title}
      </h4>
      <div className="flex flex-wrap gap-2">
        {displayItems.map((item) => (
          <span
            key={item}
            className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-700"
          >
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}

export default KeywordList;
