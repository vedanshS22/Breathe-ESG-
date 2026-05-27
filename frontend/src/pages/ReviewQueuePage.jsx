import { Download, Filter, Search } from "lucide-react";
import { useState } from "react";
import EmptyState from "../components/EmptyState.jsx";
import RecordTable from "../components/RecordTable.jsx";
import {
  exportUrl,
  useApproveRecord,
  useRecords,
  useRejectRecord,
} from "../hooks/useApiQueries.js";

export default function ReviewQueuePage() {
  const [status, setStatus] = useState("pending");
  const [sourceType, setSourceType] = useState("");
  const [suspicious, setSuspicious] = useState("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const params = {
    status,
    source_type: sourceType || undefined,
    suspicious: suspicious || undefined,
    search: search || undefined,
    page,
    page_size: pageSize,
  };
  const records = useRecords(params);
  const approveRecord = useApproveRecord();
  const rejectRecord = useRejectRecord();
  const rows = records.data?.results || [];
  const totalPages = records.data?.total_pages || 1;
  const count = records.data?.count || 0;

  function updateFilter(setter, value) {
    setter(value);
    setPage(1);
  }

  function handleApprove(record) {
    const ok = window.confirm(
      `Approve and lock record #${record.id} from ${record.upload_filename}? This cannot be edited after approval.`,
    );
    if (ok) {
      approveRecord.mutate(record.id);
    }
  }

  function handleReject(record) {
    const ok = window.confirm(`Reject record #${record.id} from ${record.upload_filename}?`);
    if (ok) {
      rejectRecord.mutate(record.id);
    }
  }

  const exportParams = {
    status,
    source_type: sourceType,
    suspicious,
    search,
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold tracking-normal text-slate-950">Review queue</h1>
        <p className="text-sm text-slate-500">Approve records into a locked audit state or reject bad rows.</p>
      </div>

      <div className="flex flex-col gap-3 rounded-md border border-slate-200 bg-white p-4 lg:flex-row lg:items-center">
        <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
          <Filter size={16} />
          Filters
        </div>
        <select
          className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
          value={status}
          onChange={(event) => updateFilter(setStatus, event.target.value)}
        >
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
        <select
          className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
          value={sourceType}
          onChange={(event) => updateFilter(setSourceType, event.target.value)}
        >
          <option value="">All sources</option>
          <option value="sap">SAP</option>
          <option value="utility">Utility</option>
          <option value="travel">Travel</option>
        </select>
        <select
          className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
          value={suspicious}
          onChange={(event) => updateFilter(setSuspicious, event.target.value)}
        >
          <option value="">Any anomaly state</option>
          <option value="true">Suspicious only</option>
          <option value="false">Clear only</option>
        </select>
        <label className="relative min-w-0 flex-1">
          <Search className="pointer-events-none absolute left-3 top-2.5 text-slate-400" size={16} />
          <input
            className="h-10 w-full rounded-md border border-slate-300 pl-9 pr-3 text-sm outline-none focus:border-emerald-500"
            value={search}
            onChange={(event) => updateFilter(setSearch, event.target.value)}
            placeholder="Search category, reference, reason"
          />
        </label>
        <select
          className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
          value={pageSize}
          onChange={(event) => {
            setPageSize(Number(event.target.value));
            setPage(1);
          }}
        >
          <option value={25}>25 rows</option>
          <option value={50}>50 rows</option>
          <option value={100}>100 rows</option>
          <option value={250}>250 rows</option>
        </select>
        <a
          className="inline-flex h-10 items-center gap-2 rounded-md border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 hover:bg-slate-100"
          href={exportUrl("raw", exportParams)}
        >
          <Download size={16} />
          Raw CSV
        </a>
        <a
          className="inline-flex h-10 items-center gap-2 rounded-md border border-slate-300 bg-white px-3 text-sm font-medium text-slate-700 hover:bg-slate-100"
          href={exportUrl("normalized", exportParams)}
        >
          <Download size={16} />
          Normalized CSV
        </a>
      </div>

      {rows.length ? (
        <>
          <div className="flex flex-col gap-3 rounded-md border border-slate-200 bg-white px-4 py-3 text-sm text-slate-600 sm:flex-row sm:items-center sm:justify-between">
            <span>
              Showing {(page - 1) * pageSize + 1}-{Math.min(page * pageSize, count)} of {count} records
            </span>
            <div className="flex items-center gap-2">
              <button
                className="rounded-md border border-slate-300 px-3 py-2 font-medium disabled:opacity-40"
                disabled={page <= 1}
                onClick={() => setPage((value) => Math.max(value - 1, 1))}
              >
                Previous
              </button>
              <span>
                Page {page} / {totalPages}
              </span>
              <button
                className="rounded-md border border-slate-300 px-3 py-2 font-medium disabled:opacity-40"
                disabled={page >= totalPages}
                onClick={() => setPage((value) => value + 1)}
              >
                Next
              </button>
            </div>
          </div>
          <RecordTable
            records={rows}
            onApprove={handleApprove}
            onReject={handleReject}
            approvingId={approveRecord.variables}
            rejectingId={rejectRecord.variables}
          />
        </>
      ) : (
        <EmptyState
          title="No records match this queue"
          detail="Adjust filters, upload a source file, or switch status to all records."
        />
      )}
    </div>
  );
}
