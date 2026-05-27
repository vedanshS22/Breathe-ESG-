import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  approveRecord,
  createCompany,
  deleteAllIngestionData,
  exportUrl,
  fetchAuditLogs,
  fetchCompanies,
  fetchDashboard,
  fetchIngestionIssues,
  fetchRecords,
  fetchUploads,
  rejectRecord,
  uploadSource,
} from "../services/api.js";

export { exportUrl };

export function useCompanies() {
  return useQuery({ queryKey: ["companies"], queryFn: fetchCompanies });
}

export function useCreateCompany() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createCompany,
    onSuccess: (company) => {
      queryClient.setQueryData(["companies"], (companies = []) => {
        const existingCompanies = Array.isArray(companies) ? companies : [];
        if (existingCompanies.some((existingCompany) => existingCompany.id === company.id)) {
          return existingCompanies;
        }
        return [...existingCompanies, company].sort((firstCompany, secondCompany) =>
          firstCompany.name.localeCompare(secondCompany.name),
        );
      });
      return queryClient.invalidateQueries({ queryKey: ["companies"] });
    },
  });
}

export function useDashboard() {
  return useQuery({ queryKey: ["dashboard"], queryFn: fetchDashboard });
}

export function useUploads() {
  return useQuery({ queryKey: ["uploads"], queryFn: fetchUploads });
}

export function useUploadSource() {
  const queryClient = useQueryClient();
  const refreshIngestionViews = () => {
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    queryClient.invalidateQueries({ queryKey: ["records"] });
    queryClient.invalidateQueries({ queryKey: ["uploads"] });
    queryClient.invalidateQueries({ queryKey: ["issues"] });
  };
  return useMutation({
    mutationFn: uploadSource,
    onSuccess: refreshIngestionViews,
    onError: refreshIngestionViews,
  });
}

export function useRecords(params) {
  return useQuery({ queryKey: ["records", params], queryFn: () => fetchRecords(params) });
}

export function useApproveRecord() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: approveRecord,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      queryClient.invalidateQueries({ queryKey: ["records"] });
      queryClient.invalidateQueries({ queryKey: ["audit"] });
    },
  });
}

export function useRejectRecord() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: rejectRecord,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      queryClient.invalidateQueries({ queryKey: ["records"] });
      queryClient.invalidateQueries({ queryKey: ["audit"] });
    },
  });
}

export function useAuditLogs() {
  return useQuery({ queryKey: ["audit"], queryFn: fetchAuditLogs });
}

export function useIngestionIssues() {
  return useQuery({ queryKey: ["issues"], queryFn: fetchIngestionIssues });
}

export function useDeleteAllIngestionData() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteAllIngestionData,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
      queryClient.invalidateQueries({ queryKey: ["records"] });
      queryClient.invalidateQueries({ queryKey: ["uploads"] });
      queryClient.invalidateQueries({ queryKey: ["audit"] });
      queryClient.invalidateQueries({ queryKey: ["issues"] });
    },
  });
}
