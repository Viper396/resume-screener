export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

export const MAX_FILE_SIZE_BYTES = 16 * 1024 * 1024;

export const ALLOWED_FILE_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "text/plain",
];
