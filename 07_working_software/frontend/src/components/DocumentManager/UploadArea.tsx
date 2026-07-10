import { useRef, useState } from "react";

import { validateFile } from "../../utils/validators";

interface UploadAreaProps {
  onUpload: (file: File) => Promise<void>;
}

export function UploadArea({ onUpload }: UploadAreaProps) {
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleFile(file: File) {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }
    setError(null);
    setUploading(true);
    try {
      await onUpload(file);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
      }}
      onClick={() => inputRef.current?.click()}
      className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer ${
        dragging ? "border-accent bg-blue-50" : "border-slate-300"
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.pptx,.xlsx,.eml"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
        }}
      />
      <p className="text-sm text-secondary">
        {uploading ? "Uploading..." : "Drag & drop a document, or click to browse"}
      </p>
      <p className="text-xs text-secondary mt-1">PDF, DOCX, PPTX, XLSX, EML — up to 50MB</p>
      {error && <p className="text-danger text-sm mt-2">{error}</p>}
    </div>
  );
}
