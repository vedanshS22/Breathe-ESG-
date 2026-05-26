import { Filter, Search } from "lucide-react";
import { useState } from "react";
import EmptyState from "../components/EmptyState.jsx";
import RecordTable from "../components/RecordTable.jsx";
import {
  useApproveRecord,
  useRecords,
  useRejectRecord,
} from "../hooks/useApiQueries.js";

export default function ReviewQueuePage() {
  const [status, setStatus] = useState("pending");
  const [sourceType, setSourceType] = useState("");
  const [suspicious, setSuspicious] = useState("");
  const [search, setSearch] = useState("");
  const params = {
    status,
    source_type: sourceType || undefined,
    suspicious: suspicious || undefined,
    search: search || undefined,
    page_size: 100,
  };
  const records = useRecords(params);
  const approveRecord = useApproveRecord();
  const rejectRecord = useRejectRecord();
  const rows = records.data?.results || [];

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
          onChange={(event) => setStatus(event.target.value)}
        >
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
        <select
          className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
          value={sourceType}
          onChange={(event) => setSourceType(event.target.value)}
        >
          <option value="">All sources</option>
          <option value="sap">SAP</option>
          <option value="utility">Utility</option>
          <option value="travel">Travel</option>
        </select>
        <select
          className="h-10 rounded-md border border-slate-300 bg-white px-3 text-sm"
          value={suspicious}
          onChange={(event) => setSuspicious(event.target.value)}
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
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search category, reference, reason"
          />
        </label>
      </div>

      {rows.length ? (
        <RecordTable
          records={rows}
          onApprove={(id) => approveRecord.mutate(id)}
          onReject={(id) => rejectRecord.mutate(id)}
          approvingId={approveRecord.variables}
          rejectingId={rejectRecord.variables}
        />
      ) : (
        <EmptyState title="No records match this queue" detail="Adjust filters or upload a source file." />
      )}
    </div>
  );
}

