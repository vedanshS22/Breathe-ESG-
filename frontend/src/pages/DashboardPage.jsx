import { ArrowRight, RefreshCcw } from "lucide-react";
import { Link } from "react-router-dom";
import EmptyState from "../components/EmptyState.jsx";
import MetricCard from "../components/MetricCard.jsx";
import RecordTable from "../components/RecordTable.jsx";
import StatusBadge from "../components/StatusBadge.jsx";
import SourcePill from "../components/SourcePill.jsx";
import { useDashboard } from "../hooks/useApiQueries.js";

export default function DashboardPage() {
  const dashboard = useDashboard();
  const data = dashboard.data;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl font-semibold tracking-normal text-slate-950">Operational dashboard</h1>
          <p className="text-sm text-slate-500">Uploads, review queues, anomalies, and locked records.</p>
        </div>
        <button
          onClick={() => dashboard.refetch()}
          className="inline-flex items-center gap-2 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
        >
          <RefreshCcw size={16} />
          Refresh
        </button>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-6">
        <MetricCard label="Uploads" value={data?.counts.uploads} tone="sky" />
        <MetricCard label="Pending" value={data?.counts.pending} tone="amber" />
        <MetricCard label="Suspicious" value={data?.counts.suspicious} tone="rose" />
        <MetricCard label="Approved" value={data?.counts.approved} tone="emerald" />
        <MetricCard label="Rejected" value={data?.counts.rejected} tone="rose" />
        <MetricCard label="Locked" value={data?.counts.locked} tone="slate" />
      </div>

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase text-slate-600">Attention queue</h2>
          <Link to="/review" className="inline-flex items-center gap-1 text-sm font-medium text-slate-700">
            Review <ArrowRight size={14} />
          </Link>
        </div>
        {data?.attention_queue?.length ? (
          <RecordTable records={data.attention_queue} compact />
        ) : (
          <EmptyState title="No records waiting for review" detail="Upload source data to populate this queue." />
        )}
      </section>

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="space-y-3">
          <h2 className="text-sm font-semibold uppercase text-slate-600">Recent uploads</h2>
          <div className="overflow-hidden rounded-md border border-slate-200 bg-white">
            {data?.recent_uploads?.length ? (
              <div className="divide-y divide-slate-100">
                {data.recent_uploads.map((upload) => (
                  <div key={upload.id} className="flex items-center justify-between gap-4 px-4 py-3">
                    <div className="min-w-0">
                      <div className="truncate text-sm font-medium text-slate-900">{upload.original_filename}</div>
                      <div className="mt-1 flex items-center gap-2">
                        <SourcePill source={upload.source_type} />
                        <span className="text-xs text-slate-500">
                          {upload.successful_count} normalized, {upload.suspicious_count} suspicious,{" "}
                          {upload.failed_count} failed
                        </span>
                      </div>
                    </div>
                    <StatusBadge status={upload.status} />
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState title="No uploads yet" />
            )}
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-sm font-semibold uppercase text-slate-600">Records by source</h2>
          <div className="rounded-md border border-slate-200 bg-white p-4">
            <div className="space-y-3">
              {(data?.by_source || []).map((item) => (
                <div key={item.source_type} className="flex items-center justify-between">
                  <SourcePill source={item.source_type} />
                  <span className="text-sm font-semibold text-slate-800">{item.count}</span>
                </div>
              ))}
              {!data?.by_source?.length ? <EmptyState title="No source records" /> : null}
            </div>
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-sm font-semibold uppercase text-slate-600">Top issue reasons</h2>
          <div className="rounded-md border border-slate-200 bg-white p-4">
            <div className="space-y-3">
              {(data?.top_issue_reasons || []).map((item) => (
                <div key={item.reason} className="flex items-start justify-between gap-3">
                  <span className="text-sm text-slate-700">{item.reason}</span>
                  <span className="rounded-md bg-amber-50 px-2 py-1 text-xs font-semibold text-amber-800">
                    {item.count}
                  </span>
                </div>
              ))}
              {!data?.top_issue_reasons?.length ? (
                <EmptyState title="No suspicious issue patterns" detail="Clean data has no current top issues." />
              ) : null}
            </div>
          </div>
        </section>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="space-y-3">
          <h2 className="text-sm font-semibold uppercase text-slate-600">Top suspicious categories</h2>
          <div className="rounded-md border border-slate-200 bg-white p-4">
            <div className="space-y-3">
              {(data?.top_suspicious_categories || []).map((item) => (
                <div key={item.category} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-700">{item.category}</span>
                  <span className="text-sm font-semibold text-slate-900">{item.count}</span>
                </div>
              ))}
              {!data?.top_suspicious_categories?.length ? <EmptyState title="No suspicious categories" /> : null}
            </div>
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-sm font-semibold uppercase text-slate-600">Top failed units</h2>
          <div className="rounded-md border border-slate-200 bg-white p-4">
            <div className="space-y-3">
              {(data?.top_failed_units || []).map((item) => (
                <div key={item.unit} className="flex items-center justify-between">
                  <span className="font-mono text-sm text-slate-700">{item.unit}</span>
                  <span className="text-sm font-semibold text-slate-900">{item.count}</span>
                </div>
              ))}
              {!data?.top_failed_units?.length ? (
                <EmptyState title="No unknown units" detail="Unit mappings are currently handling uploaded data." />
              ) : null}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
