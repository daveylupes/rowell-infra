/**
 * Custom hooks for API calls using React Query
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  apiClient, 
  Account, 
  Transfer, 
  Transaction, 
  RemittanceFlow, 
  StablecoinAdoption,
  AnalyticsDashboard,
  KeyRetrievalResponse,
  APIError,
  DeveloperDashboard,
  APIKeyWithSecret,
  APIKeyCreateRequest
} from '@/lib/api';
import { toast } from 'sonner';
import { useAuth } from '@/contexts/AuthContext';

// Query keys for React Query
export const queryKeys = {
  accounts: ['accounts'] as const,
  account: (id: string) => ['accounts', id] as const,
  accountBalances: (id: string) => ['accounts', id, 'balances'] as const,
  transfers: ['transfers'] as const,
  transfer: (id: string) => ['transfers', id] as const,
  transactions: ['transactions'] as const,
  transaction: (hash: string) => ['transactions', hash] as const,
  remittanceFlows: ['analytics', 'remittance-flows'] as const,
  stablecoinAdoption: ['analytics', 'stablecoin-adoption'] as const,
  health: ['health'] as const,
  developerDashboard: (developerId: string) => ['developer-dashboard', developerId] as const,
};

// Account hooks
export function useAccounts(params?: {
  network?: string;
  environment?: string;
  account_type?: string;
  country_code?: string;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: [...queryKeys.accounts, params],
    queryFn: () => apiClient.listAccounts(params),
    staleTime: 30000, // 30 seconds
    retry: (failureCount, error) => {
      if (error instanceof APIError && error.status >= 400 && error.status < 500) {
        return false; // Don't retry client errors
      }
      return failureCount < 3;
    },
  });
}

export function useAccount(accountId: string) {
  return useQuery({
    queryKey: queryKeys.account(accountId),
    queryFn: () => apiClient.getAccount(accountId),
    enabled: !!accountId,
    staleTime: 30000,
  });
}

export function useAccountBalances(accountId: string) {
  return useQuery({
    queryKey: queryKeys.accountBalances(accountId),
    queryFn: () => apiClient.getAccountBalances(accountId),
    enabled: !!accountId,
    staleTime: 10000, // 10 seconds for balances
  });
}

export function useCreateAccount() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data: {
      network: 'stellar' | 'hedera';
      environment: 'testnet' | 'mainnet';
      account_type: 'user' | 'merchant' | 'anchor' | 'ngo';
      country_code: string;
      region?: string;
      metadata?: Record<string, any>;
    }) => {
      return apiClient.createAccount(data);
    },
    onSuccess: (data) => {
      // Invalidate and refetch accounts list
      queryClient.invalidateQueries({ queryKey: queryKeys.accounts });
      toast.success('Account created successfully!', {
        description: `Account ${data.account_id} created on ${data.network}`,
      });
      // Note: Private key retrieval handled separately via secure modal
    },
    onError: (error: APIError) => {
      toast.error('Failed to create account', {
        description: error.message,
      });
    },
  });
}

export function useRetrieveAccountKey(accountId: string, token: string, enabled: boolean = false) {
  return useQuery({
    queryKey: ['accounts', accountId, 'key', token],
    queryFn: () => apiClient.retrieveAccountKey(accountId, token),
    enabled: enabled && !!token && !!accountId,
    retry: false, // Don't retry - one-time token
    staleTime: 0, // Always fetch fresh
  });
}

// Transfer hooks
export function useTransfers(params?: {
  from_account?: string;
  to_account?: string;
  network?: string;
  environment?: string;
  status?: string;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: [...queryKeys.transfers, params],
    queryFn: () => apiClient.listTransfers(params),
    staleTime: 15000, // 15 seconds
  });
}

export function useTransfer(transferId: string) {
  return useQuery({
    queryKey: queryKeys.transfer(transferId),
    queryFn: () => apiClient.getTransfer(transferId),
    enabled: !!transferId,
    staleTime: 10000,
  });
}

export function useCreateTransfer() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data: {
      from_account: string;
      to_account: string;
      asset_code: string;
      amount: string;
      network: 'stellar' | 'hedera';
      environment: 'testnet' | 'mainnet';
      asset_issuer?: string;
      memo?: string;
      from_country?: string;
      to_country?: string;
      metadata?: Record<string, any>;
    }) => {
      return apiClient.createTransfer(data);
    },
    onSuccess: (data) => {
      // Invalidate and refetch transfers list
      queryClient.invalidateQueries({ queryKey: queryKeys.transfers });
      toast.success('Transfer initiated successfully!', {
        description: `Transfer ${data.transaction_hash} is being processed`,
      });
    },
    onError: (error: APIError) => {
      toast.error('Failed to create transfer', {
        description: error.message,
      });
    },
  });
}

// Transaction hooks
export function useTransactions(params?: {
  from_account?: string;
  to_account?: string;
  network?: string;
  environment?: string;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: [...queryKeys.transactions, params],
    queryFn: () => apiClient.listTransactions(params),
    staleTime: 20000, // 20 seconds
  });
}

export function useTransaction(transactionHash: string) {
  return useQuery({
    queryKey: queryKeys.transaction(transactionHash),
    queryFn: () => apiClient.getTransaction(transactionHash),
    enabled: !!transactionHash,
    staleTime: 30000,
  });
}

// Analytics hooks
export function useRemittanceFlows(params?: {
  from_country?: string;
  to_country?: string;
  from_region?: string;
  to_region?: string;
  asset_code?: string;
  network?: string;
  period_type?: string;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: [...queryKeys.remittanceFlows, params],
    queryFn: () => apiClient.getRemittanceFlows(params),
    staleTime: 60000, // 1 minute
  });
}

export function useStablecoinAdoption(params?: {
  asset_code?: string;
  network?: string;
  country_code?: string;
  period_type?: string;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: [...queryKeys.stablecoinAdoption, params],
    queryFn: () => apiClient.getStablecoinAdoption(params),
    staleTime: 60000, // 1 minute
  });
}

// Analytics dashboard hook
export function useAnalyticsDashboard(params?: {
  country_code?: string;
  region?: string;
  period_type?: string;
}) {
  return useQuery({
    queryKey: ['analytics', 'dashboard', params],
    queryFn: () => apiClient.getAnalyticsDashboard(params),
    staleTime: 60000, // 1 minute
  });
}

// Health check hook
export function useHealthCheck() {
  return useQuery({
    queryKey: queryKeys.health,
    queryFn: apiClient.healthCheck,
    refetchInterval: 30000, // Check every 30 seconds
    retry: 3,
  });
}

// Dashboard data hook (combines multiple queries)
export function useDashboardData() {
  const accountsQuery = useAccounts({ limit: 10 });
  const transfersQuery = useTransfers({ limit: 10 });
  const remittanceFlowsQuery = useRemittanceFlows({ limit: 5 });
  const stablecoinAdoptionQuery = useStablecoinAdoption({ limit: 5 });
  const healthQuery = useHealthCheck();

  return {
    accounts: accountsQuery,
    transfers: transfersQuery,
    remittanceFlows: remittanceFlowsQuery,
    stablecoinAdoption: stablecoinAdoptionQuery,
    health: healthQuery,
    isLoading: accountsQuery.isLoading || transfersQuery.isLoading || 
               remittanceFlowsQuery.isLoading || stablecoinAdoptionQuery.isLoading,
    isError: accountsQuery.isError || transfersQuery.isError || 
             remittanceFlowsQuery.isError || stablecoinAdoptionQuery.isError,
  };
}

// Developer Dashboard hook - auto-creates developer if needed
export function useDeveloperDashboard(developerId?: string) {
  const { user } = useAuth();
  const actualDeveloperId = developerId || user?.id;

  return useQuery({
    queryKey: queryKeys.developerDashboard(actualDeveloperId || ''),
    queryFn: async () => {
      if (!user?.email) {
        throw new Error('User email is required');
      }

      // First, try to get developer by email (in case user registered via /auth/register)
      try {
        const developerByEmail = await apiClient.getDeveloperByEmail(user.email);
        if (developerByEmail) {
          return apiClient.getDeveloperDashboard(developerByEmail.id);
        }
      } catch (error: any) {
        // Developer not found by email - will create one below
        if (error.status !== 404) {
          throw error;
        }
      }

      // If no developer found, create one from user data
      try {
        const newDeveloper = await apiClient.createDeveloper({
          email: user.email,
          first_name: user.first_name,
          last_name: user.last_name,
          company: user.company,
          country_code: user.country_code,
          phone: user.phone,
        });
        
        // Now get the dashboard with the new developer ID
        return apiClient.getDeveloperDashboard(newDeveloper.id);
      } catch (createError: any) {
        // If creation fails (e.g., developer already exists), try to get by email again
        const developerByEmail = await apiClient.getDeveloperByEmail(user.email);
        if (developerByEmail) {
          return apiClient.getDeveloperDashboard(developerByEmail.id);
        }
        throw createError;
      }
    },
    enabled: !!user?.email,
    staleTime: 30000, // 30 seconds
    retry: 1,
  });
}

// Create Project mutation
export function useCreateProject() {
  const queryClient = useQueryClient();
  const { user } = useAuth();

  return useMutation({
    mutationFn: async (request: {
      name: string;
      description?: string;
      primary_network?: string;
      environment?: string;
      webhook_url?: string;
    }) => {
      if (!user?.email) {
        throw new Error('User must be logged in');
      }
      
      // Get developer ID by email first
      let developerId: string;
      try {
        const developer = await apiClient.getDeveloperByEmail(user.email);
        developerId = developer.id;
      } catch (error: any) {
        // Developer doesn't exist, create one
        if (error.status === 404) {
          const newDeveloper = await apiClient.createDeveloper({
            email: user.email,
            first_name: user.first_name,
            last_name: user.last_name,
            company: user.company,
            country_code: user.country_code,
            phone: user.phone,
          });
          developerId = newDeveloper.id;
        } else {
          throw error;
        }
      }
      
      return apiClient.createProject(developerId, request);
    },
    onSuccess: (data, variables) => {
      // Invalidate developer dashboard to refresh projects list
      if (user?.id) {
        queryClient.invalidateQueries({ queryKey: queryKeys.developerDashboard(user.id) });
      }
      toast.success('Project created successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to create project');
    },
  });
}

// Create API Key mutation
export function useCreateAPIKey() {
  const queryClient = useQueryClient();
  const { user } = useAuth();

  return useMutation({
    mutationFn: async ({ projectId, request }: { projectId: string; request: APIKeyCreateRequest }) => {
      if (!user?.email) {
        throw new Error('User must be logged in');
      }
      
      // Get developer ID by email first
      let developerId: string;
      try {
        const developer = await apiClient.getDeveloperByEmail(user.email);
        developerId = developer.id;
      } catch (error: any) {
        // Developer doesn't exist, create one
        if (error.status === 404) {
          const newDeveloper = await apiClient.createDeveloper({
            email: user.email,
            first_name: user.first_name,
            last_name: user.last_name,
            company: user.company,
            country_code: user.country_code,
            phone: user.phone,
          });
          developerId = newDeveloper.id;
        } else {
          throw error;
        }
      }
      
      return apiClient.createAPIKey(developerId, projectId, request);
    },
    onSuccess: (data, variables) => {
      // Invalidate developer dashboard to refresh API keys list
      if (user?.id) {
        queryClient.invalidateQueries({ queryKey: queryKeys.developerDashboard(user.id) });
      }
      toast.success('API key created successfully!');
    },
    onError: (error: Error) => {
      toast.error(error.message || 'Failed to create API key');
    },
  });
}
