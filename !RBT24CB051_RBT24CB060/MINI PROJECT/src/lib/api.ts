// API client — calls the Python FastAPI backend

const API_BASE = import.meta.env.VITE_API_URL ?? "/api";

export async function analyzeCSV(file: File): Promise<AnalysisResults> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `Server error: ${response.status}`);
  }

  return response.json();
}

// Re-export the type so components can import from here
export type { AnalysisResults } from "./types";