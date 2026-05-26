import { Inbox } from "lucide-react";

export default function EmptyState({ title, detail }) {
  return (
    <div className="grid min-h-40 place-items-center rounded-md border border-dashed border-slate-300 bg-white p-8 text-center">
      <div>
        <Inbox className="mx-auto text-slate-400" size={28} />
        <div className="mt-3 text-sm font-semibold text-slate-700">{title}</div>
        {detail ? <div className="mt-1 text-sm text-slate-500">{detail}</div> : null}
      </div>
    </div>
  );
}

