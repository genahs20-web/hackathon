import { useEffect, useState } from "react";

import { api } from "../services/api";
import { formatDate } from "../utils/formatters";

interface AuditLogEntry {
  log_id: string;
  action: string;
  entity_type: string;
  customer_id: string | null;
  created_at: string;
}

interface UserRow {
  customer_id: string;
  email: string;
  name: string;
  role: string;
}

export function AdminPage() {
  const [users, setUsers] = useState<UserRow[]>([]);
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [documentTotal, setDocumentTotal] = useState(0);

  useEffect(() => {
    api.get<UserRow[]>("/admin/users").then((res) => setUsers(res.data));
    api.get("/admin/documents").then((res) => setDocumentTotal(res.data.length));
    api.get<{ logs: AuditLogEntry[] }>("/admin/audit-logs").then((res) => setLogs(res.data.logs));
  }, []);

  async function handleReindexAll() {
    await api.post("/admin/reindex-all");
  }

  return (
    <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div className="bg-card border border-slate-200 rounded-lg p-4">
        <h2 className="font-bold text-primary mb-2">Users</h2>
        <table className="w-full text-sm">
          <tbody>
            {users.map((u) => (
              <tr key={u.customer_id} className="border-t border-slate-100">
                <td className="py-1">{u.name}</td>
                <td className="py-1 text-secondary">{u.role}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-card border border-slate-200 rounded-lg p-4">
        <h2 className="font-bold text-primary mb-2">Documents</h2>
        <p className="text-2xl font-bold">{documentTotal}</p>
        <button onClick={handleReindexAll} className="mt-2 text-sm bg-primary text-white px-3 py-1.5 rounded-md">
          Reindex All
        </button>
      </div>

      <div className="bg-card border border-slate-200 rounded-lg p-4 lg:col-span-1">
        <h2 className="font-bold text-primary mb-2">Audit Logs</h2>
        <ul className="text-sm space-y-1 max-h-64 overflow-y-auto">
          {logs.map((log) => (
            <li key={log.log_id} className="border-b border-slate-100 pb-1">
              <span className="font-medium">{log.action}</span> on {log.entity_type} — {formatDate(log.created_at)}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
