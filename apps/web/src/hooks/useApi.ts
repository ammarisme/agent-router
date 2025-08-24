import { useState, useEffect, useCallback } from 'react';
import { apiClient, type Agent, type Feature, type Route, type Role, type AnalyticsOverview } from '@/lib/api';

// Generic API hook with loading and error states
export function useApiCall<T>(
  apiCall: () => Promise<T>,
  dependencies: any[] = []
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiCall();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [apiCall]);

  useEffect(() => {
    execute();
  }, dependencies);

  return { data, loading, error, refetch: execute };
}

// Agent hooks
export function useAgents(page: number = 1, size: number = 10) {
  return useApiCall(
    () => apiClient.getAgents(page, size),
    [page, size]
  );
}

export function useAgent(id: string) {
  return useApiCall(
    () => apiClient.getAgent(id),
    [id]
  );
}

export function useCreateAgent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createAgent = useCallback(async (data: Omit<Agent, 'id' | 'status' | 'health'>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.createAgent(data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create agent');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createAgent, loading, error };
}

export function useUpdateAgent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateAgent = useCallback(async (id: string, data: Partial<Agent>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.updateAgent(id, data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update agent');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { updateAgent, loading, error };
}

export function useDeleteAgent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deleteAgent = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await apiClient.deleteAgent(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete agent');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { deleteAgent, loading, error };
}

export function useDiscoverAgents() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const discoverAgents = useCallback(async (sourceType: string, endpoint?: string) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.discoverAgents(sourceType, endpoint);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to discover agents');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { discoverAgents, loading, error };
}

// Feature hooks
export function useFeatures(page: number = 1, size: number = 10) {
  return useApiCall(
    () => apiClient.getFeatures(page, size),
    [page, size]
  );
}

export function useFeature(id: string) {
  return useApiCall(
    () => apiClient.getFeature(id),
    [id]
  );
}

export function useCreateFeature() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createFeature = useCallback(async (data: Omit<Feature, 'id' | 'status'>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.createFeature(data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create feature');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createFeature, loading, error };
}

export function useUpdateFeature() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateFeature = useCallback(async (id: string, data: Partial<Feature>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.updateFeature(id, data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update feature');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { updateFeature, loading, error };
}

export function useDeleteFeature() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deleteFeature = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await apiClient.deleteFeature(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete feature');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { deleteFeature, loading, error };
}

export function useDiscoverFeatures() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const discoverFeatures = useCallback(async (storeType: string, url?: string) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.discoverFeatures(storeType, url);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to discover features');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { discoverFeatures, loading, error };
}

// Route hooks
export function useRoutes(page: number = 1, size: number = 10) {
  return useApiCall(
    () => apiClient.getRoutes(page, size),
    [page, size]
  );
}

export function useRoute(id: string) {
  return useApiCall(
    () => apiClient.getRoute(id),
    [id]
  );
}

export function useCreateRoute() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createRoute = useCallback(async (data: Omit<Route, 'id' | 'status'>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.createRoute(data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create route');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createRoute, loading, error };
}

export function useUpdateRoute() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateRoute = useCallback(async (id: string, data: Partial<Route>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.updateRoute(id, data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update route');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { updateRoute, loading, error };
}

export function useDeleteRoute() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deleteRoute = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await apiClient.deleteRoute(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete route');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { deleteRoute, loading, error };
}

// Role hooks
export function useRoles(page: number = 1, size: number = 10) {
  return useApiCall(
    () => apiClient.getRoles(page, size),
    [page, size]
  );
}

export function useRole(id: string) {
  return useApiCall(
    () => apiClient.getRole(id),
    [id]
  );
}

export function useCreateRole() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createRole = useCallback(async (data: Omit<Role, 'id'>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.createRole(data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create role');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createRole, loading, error };
}

export function useUpdateRole() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateRole = useCallback(async (id: string, data: Partial<Role>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.updateRole(id, data);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update role');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { updateRole, loading, error };
}

export function useDeleteRole() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deleteRole = useCallback(async (id: string) => {
    try {
      setLoading(true);
      setError(null);
      await apiClient.deleteRole(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete role');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { deleteRole, loading, error };
}

export function useImportIAMRoles() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const importIAMRoles = useCallback(async (provider: string, credentials?: Record<string, any>) => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiClient.importIAMRoles(provider, credentials);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to import IAM roles');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { importIAMRoles, loading, error };
}

// Analytics hooks
export function useAnalyticsOverview() {
  return useApiCall(
    () => apiClient.getAnalyticsOverview(),
    []
  );
}

export function useRouteUsageStats() {
  return useApiCall(
    () => apiClient.getRouteUsageStats(),
    []
  );
}

export function useAgentHealthStats() {
  return useApiCall(
    () => apiClient.getAgentHealthStats(),
    []
  );
}

export function useFeatureUsageStats() {
  return useApiCall(
    () => apiClient.getFeatureUsageStats(),
    []
  );
}

// System hooks
export function useSystemHealth() {
  return useApiCall(
    () => apiClient.getSystemHealth(),
    []
  );
}

export function useSystemConfig() {
  return useApiCall(
    () => apiClient.getSystemConfig(),
    []
  );
}
