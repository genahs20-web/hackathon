export const API_BASE_URL = "/api";

export const MAX_FILE_SIZE_BYTES = 52_428_800; // 50MB
export const ALLOWED_FILE_EXTENSIONS = [".pdf", ".docx", ".pptx", ".xlsx", ".eml"];
export const MAX_MESSAGE_LENGTH = 2000;

export const DOCUMENT_STATUS_COLORS: Record<string, string> = {
  uploaded: "bg-slate-100 text-slate-700",
  processing: "bg-amber-100 text-amber-700",
  indexed: "bg-green-100 text-green-700",
  failed: "bg-red-100 text-red-700",
};

export const SEVERITY_COLORS: Record<string, string> = {
  low: "bg-slate-100 text-slate-700",
  medium: "bg-amber-100 text-amber-700",
  high: "bg-red-100 text-red-700",
};

export const RECOMMENDATION_STATUS_COLORS: Record<string, string> = {
  pending: "bg-slate-100 text-slate-700",
  approved: "bg-green-100 text-green-700",
  rejected: "bg-red-100 text-red-700",
};
