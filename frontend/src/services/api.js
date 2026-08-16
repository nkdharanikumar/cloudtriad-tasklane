// Central place for all HTTP calls to the Flask backend.
// Base URL is configurable via VITE_API_BASE_URL so it can be changed
// per-environment (local dev, Docker, Kubernetes, etc.) without code edits.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:5000";

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (networkError) {
    throw new ApiError(
      "Could not reach the server. Is the backend running?",
      0
    );
  }

  let body = null;
  const text = await response.text();
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = null;
    }
  }

  if (!response.ok) {
    const message = body?.error || `Request failed with status ${response.status}.`;
    throw new ApiError(message, response.status);
  }

  return body;
}

export const api = {
  // Tasks
  getTasks: (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    const query = params.toString();
    return request(`/api/tasks${query ? `?${query}` : ""}`);
  },
  getTask: (id) => request(`/api/tasks/${id}`),
  createTask: (data) =>
    request("/api/tasks", { method: "POST", body: JSON.stringify(data) }),
  updateTask: (id, data) =>
    request(`/api/tasks/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteTask: (id) => request(`/api/tasks/${id}`, { method: "DELETE" }),

  // Stats
  getStats: () => request("/api/stats"),

  // Health
  getHealth: () => request("/health"),
};

export { ApiError };
