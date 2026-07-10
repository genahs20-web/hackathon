import { useCallback, useEffect, useState } from "react";

import { type DocumentDto, documentsApi } from "../services/api";

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentDto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const response = await documentsApi.list();
      setDocuments(response.data.documents);
      setError(null);
    } catch {
      setError("Failed to load documents");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const upload = useCallback(
    async (file: File, title?: string) => {
      await documentsApi.upload(file, title);
      await refresh();
    },
    [refresh]
  );

  const remove = useCallback(
    async (documentId: string) => {
      await documentsApi.delete(documentId);
      await refresh();
    },
    [refresh]
  );

  const reindex = useCallback(
    async (documentId: string) => {
      await documentsApi.reindex(documentId);
      await refresh();
    },
    [refresh]
  );

  return { documents, loading, error, refresh, upload, remove, reindex };
}
