import { ALLOWED_FILE_EXTENSIONS, MAX_FILE_SIZE_BYTES, MAX_MESSAGE_LENGTH } from "./constants";

export function validateEmail(email: string): string | null {
  const pattern = /^[\w.-]+@[\w.-]+\.\w+$/;
  if (!email) return "Email is required";
  if (!pattern.test(email)) return "Invalid email format";
  return null;
}

export function validatePassword(password: string): string | null {
  if (password.length < 8) return "Password must be at least 8 characters";
  if (!/[A-Z]/.test(password) || !/[a-z]/.test(password) || !/\d/.test(password)) {
    return "Password must contain upper, lower, and a digit";
  }
  return null;
}

export function validateFile(file: File): string | null {
  const extension = "." + (file.name.split(".").pop() ?? "").toLowerCase();
  if (!ALLOWED_FILE_EXTENSIONS.includes(extension)) {
    return "Only PDF, DOCX, PPTX, XLSX, and EML files are supported";
  }
  if (file.size <= 0 || file.size > MAX_FILE_SIZE_BYTES) {
    return "File must be 50MB or smaller";
  }
  return null;
}

export function validateMessage(message: string): string | null {
  const trimmed = message.trim();
  if (trimmed.length === 0) return "Message is required";
  if (trimmed.length > MAX_MESSAGE_LENGTH) return `Message must be ${MAX_MESSAGE_LENGTH} characters or fewer`;
  return null;
}
