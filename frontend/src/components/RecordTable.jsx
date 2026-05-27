import { Check, Eye, Lock, X } from "lucide-react";
import { useState } from "react";
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
  const [selectedRecord, setSelectedRecord] = useState(null);

  return (
    <>
      <div className="overflow-hidden rounded-md border border-slate-200 bg-white">
        <div className="table-scroll overflow-x-auto">
          <table className="min-w-full table-fixed divide-y divide-slate-200 text-left text-sm">
            <thead className="bg-slate-100 text-xs uppercase text-slate-500">
              <tr>
                <th className="w-24 px-4 py-3">Source</th>
                <th className="w-48 px-4 py-3">Upload File</th>
                <th className="w-24 px-4 py-3">Scope</th>
                <th className="w-44 px-4 py-3">Category</th>
                <th className="w-32 px-4 py-3">Quantity</th>
                <th className="w-56 px-4 py-3">Suspicious</th>
                <th className="w-36 px-4 py-3">Status</th>
                {!compact ? <th className="w-44 px-4 py-3 text-right">Actions</th> : null}
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
                  <td className="px-4 py-3">
                    <div className="truncate font-medium text-slate-800">{record.upload_filename}</div>
                    <div className="text-xs text-slate-500">row {record.source_row_number || "-"}</div>
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
                      <StatusBadge status={record.status}>
                        {record.locked ? `${record.status} + locked` : record.status}
                      </StatusBadge>
                      {record.locked ? <Lock size={15} className="text-slate-500" /> : null}
                    </div>
                  </td>
                  {!compact ? (
                    <td className="px-4 py-3">
                      <div className="flex justify-end gap-2">
                        <button
                          className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-slate-200 text-slate-700 transition hover:bg-slate-50"
                          title="View raw and normalized data"
                          onClick={() => setSelectedRecord(record)}
                        >
                          <Eye size={16} />
                        </button>
                        <button
                          className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-emerald-200 text-emerald-700 transition hover:bg-emerald-50 disabled:cursor-not-allowed disabled:opacity-40"
                          title="Approve"
                          disabled={record.locked || approvingId === record.id}
                          onClick={() => onApprove(record)}
                        >
                          <Check size={16} />
                        </button>
                        <button
                          className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-rose-200 text-rose-700 transition hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-40"
                          title="Reject"
                          disabled={record.locked || rejectingId === record.id}
                          onClick={() => onReject(record)}
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
      {selectedRecord ? (
        <div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/50 p-4">
          <div className="max-h-[86vh] w-full max-w-5xl overflow-hidden rounded-md bg-white shadow-xl">
            <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
              <div>
                <div className="text-sm font-semibold text-slate-950">Record #{selectedRecord.id}</div>
                <div className="text-xs text-slate-500">{selectedRecord.upload_filename}</div>
              </div>
              <button
                className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-slate-200 text-slate-700 hover:bg-slate-50"
                onClick={() => setSelectedRecord(null)}
              >
                <X size={16} />
              </button>
            </div>
            <div className="grid max-h-[72vh] gap-4 overflow-y-auto p-5 lg:grid-cols-2">
              <section>
                <h3 className="mb-2 text-xs font-semibold uppercase text-slate-500">Normalized Data</h3>
                <pre className="overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-50">
                  {JSON.stringify(
                    {
                      scope: selectedRecord.scope,
                      category: selectedRecord.category,
                      quantity: selectedRecord.quantity,
                      normalized_unit: selectedRecord.normalized_unit,
                      start_date: selectedRecord.start_date,
                      end_date: selectedRecord.end_date,
                      status: selectedRecord.status,
                      locked: selectedRecord.locked,
                      is_suspicious: selectedRecord.is_suspicious,
                      suspicious_reason: selectedRecord.suspicious_reason,
                      metadata: selectedRecord.metadata,
                    },
                    null,
                    2,
                  )}
                </pre>
              </section>
              <section>
                <h3 className="mb-2 text-xs font-semibold uppercase text-slate-500">Raw Source Row</h3>
                <pre className="overflow-auto rounded-md bg-slate-950 p-3 text-xs text-slate-50">
                  {JSON.stringify(selectedRecord.raw_data, null, 2)}
                </pre>
              </section>
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
