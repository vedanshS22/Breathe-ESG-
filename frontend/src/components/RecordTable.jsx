import { Check, Eye, Lock, X } from "lucide-react";
import StatusBadge from "./StatusBadge.jsx";
import SourcePill from "./SourcePill.jsx";

export default function RecordTable({
  records,
  onApprove,
  onReject,
  approvingId,
  rejectingId,
  compact = false,
}) {
  return (
    <div className="overflow-hidden rounded-md border border-slate-200 bg-white">
      <div className="table-scroll overflow-x-auto">
        <table className="min-w-full table-fixed divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-100 text-xs uppercase text-slate-500">
            <tr>
              <th className="w-28 px-4 py-3">Source</th>
              <th className="w-24 px-4 py-3">Scope</th>
              <th className="w-48 px-4 py-3">Category</th>
              <th className="w-32 px-4 py-3">Quantity</th>
              <th className="w-56 px-4 py-3">Suspicious</th>
              <th className="w-28 px-4 py-3">Status</th>
              {!compact ? <th className="w-36 px-4 py-3 text-right">Actions</th> : null}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {records.map((record) => (
              <tr
                key={record.id}
                className={record.is_suspicious ? "bg-amber-50/45" : "bg-white hover:bg-slate-50"}
              >
                <td className="px-4 py-3">
                  <SourcePill source={record.source_type} />
                </td>
                <td className="px-4 py-3 font-medium text-slate-700">{record.scope}</td>
                <td className="px-4 py-3">
                  <div className="font-medium text-slate-900">{record.category}</div>
                  <div className="truncate text-xs text-slate-500">{record.source_reference || "-"}</div>
                </td>
                <td className="px-4 py-3 text-slate-700">
                  {record.quantity ?? "-"} {record.normalized_unit}
                </td>
                <td className="px-4 py-3">
                  {record.is_suspicious ? (
                    <div className="flex items-start gap-2 text-amber-800">
                      <Eye size={16} className="mt-0.5 shrink-0" />
                      <span className="line-clamp-2">{record.suspicious_reason}</span>
                    </div>
                  ) : (
                    <span className="text-slate-400">Clear</span>
                  )}
                </td>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <StatusBadge status={record.status} />
                    {record.locked ? <Lock size={15} className="text-slate-500" /> : null}
                  </div>
                </td>
                {!compact ? (
                  <td className="px-4 py-3">
                    <div className="flex justify-end gap-2">
                      <button
                        className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-emerald-200 text-emerald-700 transition hover:bg-emerald-50 disabled:cursor-not-allowed disabled:opacity-40"
                        title="Approve"
                        disabled={record.locked || approvingId === record.id}
                        onClick={() => onApprove(record.id)}
                      >
                        <Check size={16} />
                      </button>
                      <button
                        className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-rose-200 text-rose-700 transition hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-40"
                        title="Reject"
                        disabled={record.locked || rejectingId === record.id}
                        onClick={() => onReject(record.id)}
                      >
                        <X size={16} />
                      </button>
                    </div>
                  </td>
                ) : null}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

