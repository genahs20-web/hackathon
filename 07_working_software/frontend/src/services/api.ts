import axios from "axios";

import { API_BASE_URL } from "../utils/constants";
import { clearTokens, getAccessToken } from "./storage";

export const api = axios.create({ baseURL: API_BASE_URL });

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearTokens();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export interface DocumentDto {
  document_id: string;
  file_name: string;
  file_size: number;
  file_type: string;
  status: string;
  upload_date: string;
  indexed_date: string | null;
  total_chunks: number;
}

export interface SourceCitation {
  document_id: string;
  document_name: string;
  snippet: string;
  relevance_score: number;
}

export interface ChatResponseDto {
  message_id: string;
  response: string;
  sources: SourceCitation[];
  confidence: number;
  processing_time_ms: number;
}

export interface ConversationDto {
  conversation_id: string;
  title: string;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface ConflictDto {
  conflict_id: string;
  conflict_description: string;
  source_documents: string[];
  severity: string;
  resolved: boolean;
  resolution_notes: string | null;
  created_at: string;
}

export interface RecommendationDto {
  recommendation_id: string;
  recommendation_text: string;
  confidence_score: number;
  supporting_documents: string[];
  status: string;
  created_at: string;
}

export const documentsApi = {
  list: (statusFilter?: string) =>
    api.get<{ documents: DocumentDto[]; total: number }>("/documents", { params: { status_filter: statusFilter } }),
  upload: (file: File, title?: string) => {
    const formData = new FormData();
    formData.append("file", file);
    if (title) formData.append("title", title);
    return api.post("/documents/upload", formData, { headers: { "Content-Type": "multipart/form-data" } });
  },
  delete: (documentId: string) => api.delete(`/documents/${documentId}`),
  reindex: (documentId: string) => api.post(`/documents/${documentId}/reindex`),
};

export const chatApi = {
  sendMessage: (conversationId: string, message: string) =>
    api.post<ChatResponseDto>("/chat", { conversation_id: conversationId, message }),
  listConversations: () => api.get<ConversationDto[]>("/conversations"),
  createConversation: (title?: string) => api.post<ConversationDto>("/conversations", { title }),
  getConversation: (conversationId: string) => api.get(`/conversations/${conversationId}`),
  deleteConversation: (conversationId: string) => api.delete(`/conversations/${conversationId}`),
};

export const conflictsApi = {
  list: (severity?: string, resolved?: boolean) =>
    api.get<ConflictDto[]>("/conflicts", { params: { severity, resolved } }),
  resolve: (conflictId: string, resolutionNotes: string) =>
    api.post(`/conflicts/${conflictId}/resolve`, { resolution_notes: resolutionNotes }),
};

export const recommendationsApi = {
  list: (statusFilter?: string) =>
    api.get<RecommendationDto[]>("/recommendations", { params: { status_filter: statusFilter } }),
  patch: (recommendationId: string, status: "approved" | "rejected", notes?: string) =>
    api.patch(`/recommendations/${recommendationId}`, { status, notes }),
};
