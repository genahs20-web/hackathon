import { DocumentTable } from "../components/DocumentManager/DocumentTable";
import { UploadArea } from "../components/DocumentManager/UploadArea";
import { useDocuments } from "../hooks/useDocuments";

export function DocumentsPage() {
  const { documents, loading, error, upload, remove, reindex } = useDocuments();

  return (
    <div className="p-6 space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Documents</h1>
          <p className="text-sm text-muted mt-0.5">{documents.length} document{documents.length !== 1 ? "s" : ""} in your knowledge base</p>
        </div>
      </div>

      <div className="bg-card border border-border rounded-2xl p-5">
        <h2 className="text-sm font-semibold text-secondary mb-3 flex items-center gap-2">
          <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Upload New Document
        </h2>
        <UploadArea onUpload={(file) => upload(file)} />
      </div>

      {loading && (
        <div className="flex items-center gap-2 text-muted text-sm">
          <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
          </svg>
          Loading documents...
        </div>
      )}
      {error && (
        <div className="bg-danger/10 border border-danger/30 text-danger text-sm rounded-xl px-4 py-3">{error}</div>
      )}

      <div className="bg-card border border-border rounded-2xl overflow-hidden">
        <div className="px-5 py-3 border-b border-border">
          <h2 className="text-sm font-semibold text-secondary">All Documents</h2>
        </div>
        <DocumentTable documents={documents} onDelete={remove} onReindex={reindex} />
      </div>
    </div>
  );
}
