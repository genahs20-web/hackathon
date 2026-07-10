import type { DocumentDto } from "../../services/api";
import { DOCUMENT_STATUS_COLORS } from "../../utils/constants";
import { formatDate, formatFileSize } from "../../utils/formatters";

interface DocumentTableProps {
  documents: DocumentDto[];
  onDelete: (documentId: string) => void;
  onReindex: (documentId: string) => void;
}

export function DocumentTable({ documents, onDelete, onReindex }: DocumentTableProps) {
  return (
    <table className="w-full text-sm">
      <thead className="bg-slate-100 text-left">
        <tr>
          <th className="p-3">Name</th>
          <th className="p-3">Format</th>
          <th className="p-3">Status</th>
          <th className="p-3">Size</th>
          <th className="p-3">Uploaded</th>
          <th className="p-3">Actions</th>
        </tr>
      </thead>
      <tbody>
        {documents.map((doc) => (
          <tr key={doc.document_id} className="border-t border-slate-200">
            <td className="p-3">{doc.file_name}</td>
            <td className="p-3 uppercase">{doc.file_type}</td>
            <td className="p-3">
              <span className={`px-2 py-1 rounded text-xs ${DOCUMENT_STATUS_COLORS[doc.status]}`}>
                {doc.status}
              </span>
            </td>
            <td className="p-3">{formatFileSize(doc.file_size)}</td>
            <td className="p-3">{formatDate(doc.upload_date)}</td>
            <td className="p-3 flex gap-3">
              <button
                onClick={() => onReindex(doc.document_id)}
                disabled={doc.status === "processing"}
                className="text-accent disabled:opacity-40"
              >
                Reindex
              </button>
              <button onClick={() => onDelete(doc.document_id)} className="text-danger">
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
