import { API_URL } from "../constants/config";

export async function scoreResume({ file, jobDescription, role }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("job_description", jobDescription.trim());
  formData.append("role", role);

  let response;
  try {
    response = await fetch(`${API_URL}/api/score-resume`, {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      "Cannot reach backend. Make sure the API is running on localhost:5000.",
    );
  }

  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Failed to score resume");
  }

  return payload;
}
