const labels = {
  sap: "SAP",
  utility: "Utility",
  travel: "Travel",
};

const styles = {
  sap: "bg-indigo-50 text-indigo-700 border-indigo-200",
  utility: "bg-cyan-50 text-cyan-700 border-cyan-200",
  travel: "bg-violet-50 text-violet-700 border-violet-200",
};

export default function SourcePill({ source }) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-md border px-2 py-1 text-xs font-semibold",
        styles[source] || "border-slate-200 bg-slate-50 text-slate-700",
      ].join(" ")}
    >
      {labels[source] || source}
    </span>
  );
}

