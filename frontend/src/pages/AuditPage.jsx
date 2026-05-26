import { AlertTriangle, History } from "lucide-react";
import EmptyState from "../components/EmptyState.jsx";
import { useAuditLogs, useIngestionIssues } from "../hooks/useApiQueries.js";

export default function AuditPage() {
  const auditLogs = useAuditLogs();
  const issues = useIngestionIssues();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold tracking-normal text-slate-950">Audit and ingestion issues</h1>
        <p className="text-sm text-slate-500">Mutation history and row-level failures remain visible.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="space-y-3">
          <div className="flex items-center gap-2 text-sm font-semibold uppercase text-slate-600">
            <History size={16} />
            Audit log
          </div>
          <div className="overflow-hidden rounded-md border border-slate-200 bg-white">
            {(auditLogs.data || []).map((log) => (
              <div key={log.id} className="border-b border-slate-100 p-4 last:border-b-0">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-semibold text-slate-900">{log.action}</div>
                  <div className="text-xs text-slate-500">
                    {new Date(log.timestamp).toLocaleString()}
                  </div>
                </div>
                <div className="mt-1 text-sm text-slate-600">
                  Record #{log.record} · {log.record_source_type} · {log.changed_by}
                </div>
              </div>
            ))}
            {!auditLogs.data?.length ? <EmptyState title="No audit events yet" /> : null}
          </div>
        </section>

        <section className="space-y-3">
          <div className="flex items-center gap-2 text-sm font-semibold uppercase text-slate-600">
            <AlertTriangle size={16} />
            Ingestion issues
          </div>
          <div className="overflow-hidden rounded-md border border-slate-200 bg-white">
            {(issues.data || []).map((issue) => (
              <div key={issue.id} className="border-b border-slate-100 p-4 last:border-b-0">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-semibold text-slate-900">{issue.stage}</div>
                  <div className="text-xs text-slate-500">row {issue.row_number || "-"}</div>
                </div>
                <div className="mt-1 text-sm text-slate-600">{issue.message}</div>
                <div className="mt-1 truncate text-xs text-slate-500">{issue.upload_filename}</div>
              </div>
            ))}
            {!issues.data?.length ? <EmptyState title="No ingestion issues" /> : null}
          </div>
        </section>
      </div>
    </div>
  );
}

