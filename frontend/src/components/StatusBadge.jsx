import { AlertTriangle, CheckCircle2, Clock3, Lock, XCircle } from "lucide-react";

const statusStyles = {
  pending: "border-amber-200 bg-amber-50 text-amber-800",
  approved: "border-emerald-200 bg-emerald-50 text-emerald-800",
  rejected: "border-rose-200 bg-rose-50 text-rose-800",
  processed: "border-emerald-200 bg-emerald-50 text-emerald-800",
  partial: "border-amber-200 bg-amber-50 text-amber-800",
  failed: "border-rose-200 bg-rose-50 text-rose-800",
  uploaded: "border-sky-200 bg-sky-50 text-sky-800",
};

const icons = {
  pending: Clock3,
  approved: CheckCircle2,
  rejected: XCircle,
  processed: CheckCircle2,
  partial: AlertTriangle,
  failed: XCircle,
  uploaded: Clock3,
  locked: Lock,
};

export default function StatusBadge({ status, children }) {
  const Icon = icons[status] || Clock3;
  return (
    <span
      className={[
        "inline-flex items-center gap-1 rounded-md border px-2 py-1 text-xs font-medium",
        statusStyles[status] || "border-slate-200 bg-slate-50 text-slate-700",
      ].join(" ")}
    >
      <Icon size={13} />
      {children || status}
    </span>
  );
}

