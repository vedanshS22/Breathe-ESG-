import { Activity, ClipboardCheck, DatabaseZap, FileUp, ShieldCheck } from "lucide-react";
import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: Activity },
  { to: "/upload", label: "Upload", icon: FileUp },
  { to: "/review", label: "Review", icon: ClipboardCheck },
  { to: "/audit", label: "Audit", icon: ShieldCheck },
];

export default function AppLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 border-r border-slate-200 bg-white lg:block">
        <div className="flex h-16 items-center gap-3 border-b border-slate-200 px-5">
          <div className="grid h-9 w-9 place-items-center rounded-md bg-emerald-600 text-white">
            <DatabaseZap size={20} />
          </div>
          <div>
            <div className="text-sm font-semibold tracking-wide">Breathe ESG</div>
            <div className="text-xs text-slate-500">Analyst operations</div>
          </div>
        </div>
        <nav className="space-y-1 p-3">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition",
                  isActive
                    ? "bg-slate-900 text-white"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-950",
                ].join(" ")
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 lg:px-8">
          <div>
            <div className="text-sm font-semibold">Enterprise ESG ingestion</div>
            <div className="text-xs text-slate-500">Raw source to locked review records</div>
          </div>
          <div className="hidden items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-xs text-slate-600 sm:flex">
            <ShieldCheck size={15} className="text-emerald-600" />
            Audit-first prototype
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-6 lg:px-8">{children}</main>
      </div>
    </div>
  );
}

