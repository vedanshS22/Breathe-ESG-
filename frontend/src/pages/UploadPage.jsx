import { Building2, Loader2, Plus, Send } from "lucide-react";
import { useMemo, useState } from "react";
import StatusBadge from "../components/StatusBadge.jsx";
import UploadDropzone from "../components/UploadDropzone.jsx";
import {
  useCompanies,
  useCreateCompany,
  useDeleteAllIngestionData,
  useUploadSource,
  useUploads,
} from "../hooks/useApiQueries.js";

const sourceOptions = [
  { value: "sap", label: "SAP fuel/procurement" },
  { value: "utility", label: "Utility electricity" },
  { value: "travel", label: "Corporate travel" },
];

export default function UploadPage() {
  const companies = useCompanies();
  const uploads = useUploads();
  const createCompany = useCreateCompany();
  const uploadSource = useUploadSource();
  const deleteAllIngestionData = useDeleteAllIngestionData();
  const [companyId, setCompanyId] = useState("");
  const [sourceType, setSourceType] = useState("sap");
  const [file, setFile] = useState(null);
  const [companyName, setCompanyName] = useState("Northstar Manufacturing");
  const [lastUpload, setLastUpload] = useState(null);

  const selectedCompany = useMemo(() => {
    return companies.data?.find((company) => String(company.id) === String(companyId));
  }, [companies.data, companyId]);

  async function handleCreateCompany() {
    const company = await createCompany.mutateAsync(companyName.trim());
    setCompanyId(company.id);
    setCompanyName("");
  }

  async function handleUpload(event) {
    event.preventDefault();
    if (!companyId || !file) return;
    const result = await uploadSource.mutateAsync({ companyId, sourceType, file });
    setLastUpload(result);
    setFile(null);
  }

  async function handleDeleteAll() {
    const confirmed = window.confirm(
      "Delete all ingestion data? This removes raw uploads, normalized records, audit logs, and ingestion issues. This cannot be undone.",
    );
    if (!confirmed) {
      return;
    }
    if (window.prompt('Type DELETE ALL to confirm this destructive action.') !== "DELETE ALL") {
      return;
    }
    await deleteAllIngestionData.mutateAsync();
    setLastUpload(null);
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold tracking-normal text-slate-950">Upload source data</h1>
        <p className="text-sm text-slate-500">Preserve the raw artifact before parsing and normalization.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_360px]">
        <form onSubmit={handleUpload} className="space-y-4 rounded-md border border-slate-200 bg-white p-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">Company</span>
              <select
                className="h-10 w-full rounded-md border border-slate-300 bg-white px-3 text-sm outline-none focus:border-emerald-500"
                value={companyId}
                onChange={(event) => setCompanyId(event.target.value)}
              >
                <option value="">Select company</option>
                {(companies.data || []).map((company) => (
                  <option key={company.id} value={company.id}>
                    {company.name}
                  </option>
                ))}
              </select>
            </label>
            <label className="space-y-2">
              <span className="text-sm font-medium text-slate-700">Source type</span>
              <select
                className="h-10 w-full rounded-md border border-slate-300 bg-white px-3 text-sm outline-none focus:border-emerald-500"
                value={sourceType}
                onChange={(event) => setSourceType(event.target.value)}
              >
                {sourceOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
            <div className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">
              <Building2 size={16} />
              New company
            </div>
            <div className="flex gap-2">
              <input
                className="h-10 min-w-0 flex-1 rounded-md border border-slate-300 px-3 text-sm outline-none focus:border-emerald-500"
                value={companyName}
                placeholder="Company name"
                onChange={(event) => setCompanyName(event.target.value)}
              />
              <button
                type="button"
                onClick={handleCreateCompany}
                className="inline-flex h-10 items-center gap-2 rounded-md bg-slate-900 px-3 text-sm font-medium text-white hover:bg-slate-700 disabled:opacity-50"
                disabled={createCompany.isPending || !companyName.trim()}
              >
                <Plus size={16} />
                Create
              </button>
            </div>
            {createCompany.error ? (
              <div className="mt-2 text-sm text-rose-700">
                {createCompany.error.response?.data?.error || createCompany.error.message}
              </div>
            ) : null}
          </div>

          <UploadDropzone file={file} onFileChange={setFile} />

          {uploadSource.error ? (
            <div className="rounded-md border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-800">
              {uploadSource.error.response?.data?.error || uploadSource.error.message}
            </div>
          ) : null}

          {lastUpload ? (
            <div className="rounded-md border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-950">
              <div className="font-semibold">{lastUpload.original_filename} processed</div>
              <div className="mt-2 grid gap-2 sm:grid-cols-4">
                <span>{lastUpload.row_count} rows ingested</span>
                <span>{lastUpload.successful_count} normalized</span>
                <span>{lastUpload.suspicious_count} suspicious</span>
                <span>{lastUpload.failed_count} failed</span>
              </div>
            </div>
          ) : null}

          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div className="text-sm text-slate-500">
              {selectedCompany ? `Target: ${selectedCompany.name}` : "Select a company before upload"}
            </div>
            <button
              type="submit"
              disabled={!companyId || !file || uploadSource.isPending}
              className="inline-flex h-10 items-center justify-center gap-2 rounded-md bg-emerald-600 px-4 text-sm font-semibold text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {uploadSource.isPending ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
              Ingest
            </button>
          </div>
        </form>

        <aside className="space-y-3">
          <h2 className="text-sm font-semibold uppercase text-slate-600">Upload history</h2>
          <button
            type="button"
            onClick={handleDeleteAll}
            className="inline-flex h-10 w-full items-center justify-center rounded-md border border-rose-200 bg-white px-3 text-sm font-semibold text-rose-700 hover:bg-rose-50 disabled:opacity-50"
            disabled={deleteAllIngestionData.isPending}
          >
            Delete All Ingestion Data
          </button>
          <div className="rounded-md border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
            Deletes raw files, normalized records, audit logs, and issue history. This cannot be undone.
          </div>
          <div className="rounded-md border border-slate-200 bg-white">
            {(uploads.data || []).slice(0, 8).map((upload) => (
              <div key={upload.id} className="border-b border-slate-100 p-3 last:border-b-0">
                <div className="truncate text-sm font-medium text-slate-900">{upload.original_filename}</div>
                <div className="mt-2 flex items-center justify-between gap-2">
                  <span className="text-xs text-slate-500">
                    {upload.successful_count}/{upload.row_count} normalized · {upload.suspicious_count} suspicious ·{" "}
                    {upload.failed_count} failed
                  </span>
                  <StatusBadge status={upload.status} />
                </div>
              </div>
            ))}
            {!uploads.data?.length ? <div className="p-4 text-sm text-slate-500">No uploads yet.</div> : null}
          </div>
        </aside>
      </div>
    </div>
  );
}
