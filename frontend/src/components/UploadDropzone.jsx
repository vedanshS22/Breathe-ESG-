import { FileUp } from "lucide-react";

export default function UploadDropzone({ file, onFileChange }) {
  return (
    <label className="flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-md border-2 border-dashed border-slate-300 bg-white px-6 py-8 text-center transition hover:border-emerald-500 hover:bg-emerald-50/40">
      <FileUp className="text-slate-500" size={30} />
      <div className="mt-3 text-sm font-semibold text-slate-800">
        {file ? file.name : "Choose source file"}
      </div>
      <div className="mt-1 text-xs text-slate-500">CSV for SAP/utility/travel, JSON for travel</div>
      <input
        className="sr-only"
        type="file"
        accept=".csv,.json"
        onChange={(event) => onFileChange(event.target.files?.[0] || null)}
      />
    </label>
  );
}

