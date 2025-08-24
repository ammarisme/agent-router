'use client'

import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { apiClient, type Agent, type Feature, type Route, type Role } from '@/lib/api';

// API State Interface
interface ApiState {
  agents: Agent[];
  features: Feature[];
  routes: Route[];
  roles: Role[];
  loading: {
    agents: boolean;
    features: boolean;
    routes: boolean;
    roles: boolean;
  };
  error: {
    agents: string | null;
    features: string | null;
    routes: string | null;
    roles: string | null;
  };
}

// API Context Interface
interface ApiContextType extends ApiState {
  // Agent actions
  fetchAgents: () => Promise<void>;
  createAgent: (data: Omit<Agent, 'id' | 'status' | 'health'>) => Promise<Agent>;
  updateAgent: (id: string, data: Partial<Agent>) => Promise<Agent>;
  deleteAgent: (id: string) => Promise<void>;
  discoverAgents: (sourceType: string, endpoint?: string) => Promise<Agent[]>;
  
  // Feature actions
  fetchFeatures: () => Promise<void>;
  createFeature: (data: Omit<Feature, 'id' | 'status'>) => Promise<Feature>;
  updateFeature: (id: string, data: Partial<Feature>) => Promise<Feature>;
  deleteFeature: (id: string) => Promise<void>;
  discoverFeatures: (storeType: string, url?: string) => Promise<Feature[]>;
  
  // Route actions
  fetchRoutes: () => Promise<void>;
  createRoute: (data: Omit<Route, 'id' | 'status'>) => Promise<Route>;
  updateRoute: (id: string, data: Partial<Route>) => Promise<Route>;
  deleteRoute: (id: string) => Promise<void>;
  
  // Role actions
  fetchRoles: () => Promise<void>;
  createRole: (data: Omit<Role, 'id'>) => Promise<Role>;
  updateRole: (id: string, data: Partial<Role>) => Promise<Role>;
  deleteRole: (id: string) => Promise<void>;
  importIAMRoles: (provider: string, credentials?: Record<string, any>) => Promise<{
    imported_roles: Role[];
    failed_roles: Record<string, any>[];
    total_imported: number;
    total_failed: number;
  }>;
  
  // Utility functions
  refreshAll: () => Promise<void>;
  clearErrors: () => void;
}

// Create context
const ApiContext = createContext<ApiContextType | undefined>(undefined);

// Initial state
const initialState: ApiState = {
  agents: [],
  features: [],
  routes: [],
  roles: [],
  loading: {
    agents: false,
    features: false,
    routes: false,
    roles: false,
  },
  error: {
    agents: null,
    features: null,
    routes: null,
    roles: null,
  },
};

// Provider component
export function ApiProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<ApiState>(initialState);

  // Helper function to update loading state
  const setLoading = (key: keyof ApiState['loading'], value: boolean) => {
    setState(prev => ({
      ...prev,
      loading: { ...prev.loading, [key]: value }
    }));
  };

  // Helper function to update error state
  const setError = (key: keyof ApiState['error'], value: string | null) => {
    setState(prev => ({
      ...prev,
      error: { ...prev.error, [key]: value }
    }));
  };

  // Helper function to update data state
  const setData = <K extends keyof Pick<ApiState, 'agents' | 'features' | 'routes' | 'roles'>>(
    key: K,
    value: ApiState[K]
  ) => {
    setState(prev => ({ ...prev, [key]: value }));
  };

  // Agent actions
  const fetchAgents = useCallback(async () => {
    try {
      setLoading('agents', true);
      setError('agents', null);
      const response = await apiClient.getAgents();
      setData('agents', response.agents);
    } catch (error) {
      setError('agents', error instanceof Error ? error.message : 'Failed to fetch agents');
    } finally {
      setLoading('agents', false);
    }
  }, []);

  const createAgent = async (data: Omit<Agent, 'id' | 'status' | 'health'>): Promise<Agent> => {
    try {
      setLoading('agents', true);
      setError('agents', null);
      const newAgent = await apiClient.createAgent(data);
      setData('agents', [...state.agents, newAgent]);
      return newAgent;
    } catch (error) {
      setError('agents', error instanceof Error ? error.message : 'Failed to create agent');
      throw error;
    } finally {
      setLoading('agents', false);
    }
  };

  const updateAgent = async (id: string, data: Partial<Agent>): Promise<Agent> => {
    try {
      setLoading('agents', true);
      setError('agents', null);
      const updatedAgent = await apiClient.updateAgent(id, data);
      setData('agents', state.agents.map(agent => 
        agent.id === id ? updatedAgent : agent
      ));
      return updatedAgent;
    } catch (error) {
      setError('agents', error instanceof Error ? error.message : 'Failed to update agent');
      throw error;
    } finally {
      setLoading('agents', false);
    }
  };

  const deleteAgent = async (id: string): Promise<void> => {
    try {
      setLoading('agents', true);
      setError('agents', null);
      await apiClient.deleteAgent(id);
      setData('agents', state.agents.filter(agent => agent.id !== id));
    } catch (error) {
      setError('agents', error instanceof Error ? error.message : 'Failed to delete agent');
      throw error;
    } finally {
      setLoading('agents', false);
    }
  };

  const discoverAgents = async (sourceType: string, endpoint?: string): Promise<Agent[]> => {
    try {
      setLoading('agents', true);
      setError('agents', null);
      const discoveredAgents = await apiClient.discoverAgents(sourceType, endpoint);
      return discoveredAgents;
    } catch (error) {
      setError('agents', error instanceof Error ? error.message : 'Failed to discover agents');
      throw error;
    } finally {
      setLoading('agents', false);
    }
  };

  // Feature actions
  const fetchFeatures = useCallback(async () => {
    try {
      setLoading('features', true);
      setError('features', null);
      const response = await apiClient.getFeatures();
      setData('features', response.features);
    } catch (error) {
      setError('features', error instanceof Error ? error.message : 'Failed to fetch features');
    } finally {
      setLoading('features', false);
    }
  }, []);

  const createFeature = async (data: Omit<Feature, 'id' | 'status'>): Promise<Feature> => {
    try {
      setLoading('features', true);
      setError('features', null);
      const newFeature = await apiClient.createFeature(data);
      setData('features', [...state.features, newFeature]);
      return newFeature;
    } catch (error) {
      setError('features', error instanceof Error ? error.message : 'Failed to create feature');
      throw error;
    } finally {
      setLoading('features', false);
    }
  };

  const updateFeature = async (id: string, data: Partial<Feature>): Promise<Feature> => {
    try {
      setLoading('features', true);
      setError('features', null);
      const updatedFeature = await apiClient.updateFeature(id, data);
      setData('features', state.features.map(feature => 
        feature.id === id ? updatedFeature : feature
      ));
      return updatedFeature;
    } catch (error) {
      setError('features', error instanceof Error ? error.message : 'Failed to update feature');
      throw error;
    } finally {
      setLoading('features', false);
    }
  };

  const deleteFeature = async (id: string): Promise<void> => {
    try {
      setLoading('features', true);
      setError('features', null);
      await apiClient.deleteFeature(id);
      setData('features', state.features.filter(feature => feature.id !== id));
    } catch (error) {
      setError('features', error instanceof Error ? error.message : 'Failed to delete feature');
      throw error;
    } finally {
      setLoading('features', false);
    }
  };

  const discoverFeatures = async (storeType: string, url?: string): Promise<Feature[]> => {
    try {
      setLoading('features', true);
      setError('features', null);
      const discoveredFeatures = await apiClient.discoverFeatures(storeType, url);
      return discoveredFeatures;
    } catch (error) {
      setError('features', error instanceof Error ? error.message : 'Failed to discover features');
      throw error;
    } finally {
      setLoading('features', false);
    }
  };

  // Route actions
  const fetchRoutes = useCallback(async () => {
    try {
      setLoading('routes', true);
      setError('routes', null);
      const response = await apiClient.getRoutes();
      setData('routes', response.routes);
    } catch (error) {
      setError('routes', error instanceof Error ? error.message : 'Failed to fetch routes');
    } finally {
      setLoading('routes', false);
    }
  }, []);

  const createRoute = async (data: Omit<Route, 'id' | 'status'>): Promise<Route> => {
    try {
      setLoading('routes', true);
      setError('routes', null);
      const newRoute = await apiClient.createRoute(data);
      setData('routes', [...state.routes, newRoute]);
      return newRoute;
    } catch (error) {
      setError('routes', error instanceof Error ? error.message : 'Failed to create route');
      throw error;
    } finally {
      setLoading('routes', false);
    }
  };

  const updateRoute = async (id: string, data: Partial<Route>): Promise<Route> => {
    try {
      setLoading('routes', true);
      setError('routes', null);
      const updatedRoute = await apiClient.updateRoute(id, data);
      setData('routes', state.routes.map(route => 
        route.id === id ? updatedRoute : route
      ));
      return updatedRoute;
    } catch (error) {
      setError('routes', error instanceof Error ? error.message : 'Failed to update route');
      throw error;
    } finally {
      setLoading('routes', false);
    }
  };

  const deleteRoute = async (id: string): Promise<void> => {
    try {
      setLoading('routes', true);
      setError('routes', null);
      await apiClient.deleteRoute(id);
      setData('routes', state.routes.filter(route => route.id !== id));
    } catch (error) {
      setError('routes', error instanceof Error ? error.message : 'Failed to delete route');
      throw error;
    } finally {
      setLoading('routes', false);
    }
  };

  // Role actions
  const fetchRoles = useCallback(async () => {
    try {
      setLoading('roles', true);
      setError('roles', null);
      const response = await apiClient.getRoles();
      setData('roles', response.roles);
    } catch (error) {
      setError('roles', error instanceof Error ? error.message : 'Failed to fetch roles');
    } finally {
      setLoading('roles', false);
    }
  }, []);

  const createRole = async (data: Omit<Role, 'id'>): Promise<Role> => {
    try {
      setLoading('roles', true);
      setError('roles', null);
      const newRole = await apiClient.createRole(data);
      setData('roles', [...state.roles, newRole]);
      return newRole;
    } catch (error) {
      setError('roles', error instanceof Error ? error.message : 'Failed to create role');
      throw error;
    } finally {
      setLoading('roles', false);
    }
  };

  const updateRole = async (id: string, data: Partial<Role>): Promise<Role> => {
    try {
      setLoading('roles', true);
      setError('roles', null);
      const updatedRole = await apiClient.updateRole(id, data);
      setData('roles', state.roles.map(role => 
        role.id === id ? updatedRole : role
      ));
      return updatedRole;
    } catch (error) {
      setError('roles', error instanceof Error ? error.message : 'Failed to update role');
      throw error;
    } finally {
      setLoading('roles', false);
    }
  };

  const deleteRole = async (id: string): Promise<void> => {
    try {
      setLoading('roles', true);
      setError('roles', null);
      await apiClient.deleteRole(id);
      setData('roles', state.roles.filter(role => role.id !== id));
    } catch (error) {
      setError('roles', error instanceof Error ? error.message : 'Failed to delete role');
      throw error;
    } finally {
      setLoading('roles', false);
    }
  };

  const importIAMRoles = async (provider: string, credentials?: Record<string, any>) => {
    try {
      setLoading('roles', true);
      setError('roles', null);
      const result = await apiClient.importIAMRoles(provider, credentials);
      // Add imported roles to the state
      setData('roles', [...state.roles, ...result.imported_roles]);
      return result;
    } catch (error) {
      setError('roles', error instanceof Error ? error.message : 'Failed to import IAM roles');
      throw error;
    } finally {
      setLoading('roles', false);
    }
  };

  // Utility functions
  const refreshAll = useCallback(async () => {
    await Promise.all([
      fetchAgents(),
      fetchFeatures(),
      fetchRoutes(),
      fetchRoles(),
    ]);
  }, [fetchAgents, fetchFeatures, fetchRoutes, fetchRoles]);

  const clearErrors = () => {
    setState(prev => ({
      ...prev,
      error: {
        agents: null,
        features: null,
        routes: null,
        roles: null,
      }
    }));
  };

  // Load initial data - removed to prevent double fetching
  // The components will call fetchAgents/fetchFeatures as needed

  const contextValue: ApiContextType = {
    ...state,
    fetchAgents,
    createAgent,
    updateAgent,
    deleteAgent,
    discoverAgents,
    fetchFeatures,
    createFeature,
    updateFeature,
    deleteFeature,
    discoverFeatures,
    fetchRoutes,
    createRoute,
    updateRoute,
    deleteRoute,
    fetchRoles,
    createRole,
    updateRole,
    deleteRole,
    importIAMRoles,
    refreshAll,
    clearErrors,
  };

  return (
    <ApiContext.Provider value={contextValue}>
      {children}
    </ApiContext.Provider>
  );
}

// Custom hook to use the API context
export function useApi() {
  const context = useContext(ApiContext);
  if (context === undefined) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
}
