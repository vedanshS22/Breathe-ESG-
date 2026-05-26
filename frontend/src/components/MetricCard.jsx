export default function MetricCard({ label, value, tone = "slate" }) {
  const tones = {
    slate: "border-slate-200 bg-white",
    emerald: "border-emerald-200 bg-emerald-50",
    amber: "border-amber-200 bg-amber-50",
    rose: "border-rose-200 bg-rose-50",
    sky: "border-sky-200 bg-sky-50",
  };

  return (
    <div className={["rounded-md border p-4", tones[tone]].join(" ")}>
      <div className="text-xs font-medium uppercase text-slate-500">{label}</div>
      <div className="mt-2 text-2xl font-semibold text-slate-950">{value ?? 0}</div>
    </div>
  );
}

