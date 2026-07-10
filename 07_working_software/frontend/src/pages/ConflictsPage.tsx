import { useEffect, useState } from "react";

import { ConflictCard } from "../components/ConflictCard";
import { conflictsApi, type ConflictDto } from "../services/api";

const SEVERITY_FILTERS = ["all", "low", "medium", "high"] as const;

export function ConflictsPage() {
  const [conflicts, setConflicts] = useState<ConflictDto[]>([]);
  const [filter, setFilter] = useState<(typeof SEVERITY_FILTERS)[number]>("all");

  async function refresh() {
    const severity = filter === "all" ? undefined : filter;
    const response = await conflictsApi.list(severity);
    setConflicts(response.data);
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  async function handleResolve(conflictId: string, notes: string) {
    await conflictsApi.resolve(conflictId, notes);
    await refresh();
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold text-primary">Identified Conflicts</h1>
      <div className="flex gap-2">
        {SEVERITY_FILTERS.map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-3 py-1.5 rounded-md text-sm ${
              filter === s ? "bg-primary text-white" : "bg-card border border-slate-200 text-secondary"
            }`}
          >
            {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>
      <div className="space-y-3">
        {conflicts.map((conflict) => (
          <ConflictCard key={conflict.conflict_id} conflict={conflict} onResolve={handleResolve} />
        ))}
        {conflicts.length === 0 && <p className="text-secondary text-sm">No conflicts found.</p>}
      </div>
    </div>
  );
}
