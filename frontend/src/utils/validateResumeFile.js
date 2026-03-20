import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE_BYTES } from "../constants/config";

export function validateResumeFile(file) {
  if (!file) {
    return "Please choose a file.";
  }

  if (!ALLOWED_FILE_TYPES.includes(file.type)) {
    return "Invalid file type. Please upload PDF, DOCX, or TXT files.";
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    return "File size exceeds 16MB limit.";
  }

  return null;
}
