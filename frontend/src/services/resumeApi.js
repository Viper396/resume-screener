import { API_URL } from "../constants/config";

export async function scoreResume({ file, jobDescription }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_description", jobDescription.trim());

  const response = await fetch(`${API_URL}/api/score-resume`, {
    method: "POST",
    body: formData,
  });

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Failed to score resume");
  }

  return payload;
}
