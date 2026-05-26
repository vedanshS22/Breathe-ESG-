import axios from "axios";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  timeout: 20000,
});

export async function fetchCompanies() {
  const { data } = await apiClient.get("/companies/");
  return data.data.results;
}

export async function createCompany(name) {
  const { data } = await apiClient.post("/companies/", { name });
  return data.data;
}

export async function fetchDashboard() {
  const { data } = await apiClient.get("/dashboard/");
  return data.data;
}

export async function fetchUploads() {
  const { data } = await apiClient.get("/uploads/");
  return data.data.results;
}

export async function uploadSource({ companyId, sourceType, file }) {
  const form = new FormData();
  form.append("company_id", companyId);
  form.append("source_type", sourceType);
  form.append("file", file);
  const { data } = await apiClient.post("/uploads/", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data.data;
}

export async function fetchRecords(params = {}) {
  const { data } = await apiClient.get("/records/", { params });
  return data.data;
}

export async function approveRecord(recordId) {
  const { data } = await apiClient.post(`/records/${recordId}/approve/`, {
    actor: "analyst@breathe.local",
  });
  return data.data;
}

export async function rejectRecord(recordId) {
  const { data } = await apiClient.post(`/records/${recordId}/reject/`, {
    actor: "analyst@breathe.local",
    reason: "Rejected during analyst review",
  });
  return data.data;
}

export async function fetchAuditLogs() {
  const { data } = await apiClient.get("/audit-logs/");
  return data.data.results;
}

export async function fetchIngestionIssues() {
  const { data } = await apiClient.get("/ingestion-issues/");
  return data.data.results;
}

export async function deleteAllIngestionData() {
  const { data } = await apiClient.post("/delete-all-ingestion-data/", {
    confirm: true,
  });
  return data.data;
}
