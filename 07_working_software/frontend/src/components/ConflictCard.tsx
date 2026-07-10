import { useState } from "react";

import type { ConflictDto } from "../services/api";
import { SEVERITY_COLORS } from "../utils/constants";

interface ConflictCardProps {
  conflict: ConflictDto;
  onResolve: (conflictId: string, notes: string) => Promise<void>;
}

export function ConflictCard({ conflict, onResolve }: ConflictCardProps) {
  const [open, setOpen] = useState(false);
  const [notes, setNotes] = useState("");

  return (
    <div className="bg-card border border-slate-200 rounded-lg p-4">
      <div className="flex items-center justify-between">
        <span className={`px-2 py-1 rounded text-xs ${SEVERITY_COLORS[conflict.severity]}`}>
          {conflict.severity.toUpperCase()}
        </span>
        <span className="text-xs text-secondary">{conflict.resolved ? "Resolved" : "Unresolved"}</span>
      </div>
      <p className="mt-2 text-sm">{conflict.conflict_description}</p>
      <div className="flex gap-2 mt-2">
        {conflict.source_documents.map((docId) => (
          <span key={docId} className="text-xs bg-slate-100 px-2 py-1 rounded">
            {docId.slice(0, 8)}
          </span>
        ))}
      </div>
      {!conflict.resolved && (
        <button onClick={() => setOpen(true)} className="mt-3 text-sm text-accent">
          View Details
        </button>
      )}

      {open && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
          <div className="bg-card rounded-lg p-6 w-full max-w-md">
            <h3 className="font-bold text-primary mb-2">Resolve Conflict</h3>
            <p className="text-sm text-secondary mb-3">{conflict.conflict_description}</p>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Resolution notes..."
              className="w-full border border-slate-300 rounded-md p-2 h-24"
            />
            <div className="flex justify-end gap-2 mt-4">
              <button onClick={() => setOpen(false)} className="text-secondary text-sm">
                Cancel
              </button>
              <button
                onClick={async () => {
                  await onResolve(conflict.conflict_id, notes);
                  setOpen(false);
                }}
                disabled={!notes.trim()}
                className="bg-primary text-white px-3 py-1.5 rounded-md text-sm disabled:opacity-50"
              >
                Mark Resolved
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
