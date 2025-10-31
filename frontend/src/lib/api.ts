/**
 * Rowell Infra API Client
 * Handles all API communication for the frontend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
// API key should be set via VITE_API_KEY environment variable
// For public repos, never use hardcoded keys - even test keys
const API_KEY = import.meta.env.VITE_API_KEY || '';

// Get auth token from localStorage
const getAuthToken = (): string | null => {
  return localStorage.getItem('rowell_access_token');
};

// Types for API responses
export interface Account {
  id: string;
  account_id: string;
  network: 'stellar' | 'hedera';
  environment: 'testnet' | 'mainnet';
  account_type: 'user' | 'merchant' | 'anchor' | 'ngo';
  country_code: string;
  region?: string;
  is_active: boolean;
  is_verified: boolean;
  is_compliant: boolean;
  kyc_status: 'pending' | 'verified' | 'rejected';
  created_at: string;
  updated_at: string;
  last_activity?: string;
  metadata?: Record<string, any>;
  // Security: Private key is NOT included
  key_retrieval_token?: string; // Only present on account creation
  key_retrieval_url?: string; // Only present on account creation
  security_warning?: string; // Only present on account creation
}

export interface KeyRetrievalResponse {
  account_id: string;
  private_key: string;
  network: string;
  warning: string;
}

export interface AccountBalance {
  asset_code: string;
  asset_issuer?: string;
  balance: string;
  balance_usd?: string;
  updated_at: string;
}

export interface Transfer {
  id: string;
  transaction_hash: string;
  from_account: string;
  to_account: string;
  asset_code: string;
  amount: string;
  status: 'pending' | 'success' | 'failed';
  network: 'stellar' | 'hedera';
  environment: 'testnet' | 'mainnet';
  from_country?: string;
  to_country?: string;
  memo?: string;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: string;
  transaction_hash: string;
  network: 'stellar' | 'hedera';
  environment: 'testnet' | 'mainnet';
  transaction_type: string;
  status: 'pending' | 'success' | 'failed';
  from_account?: string;
  to_account?: string;
  asset_code: string;
  amount: string;
  from_country?: string;
  to_country?: string;
  created_at: string;
}

export interface RemittanceFlow {
  from_country: string;
  to_country: string;
  volume: string;
  volume_usd: string;
  transaction_count: number;
  period_start: string;
  period_end: string;
}

export interface StablecoinAdoption {
  asset_code: string;
  network: 'stellar' | 'hedera';
  country_code?: string;
  total_volume: string;
  total_volume_usd: string;
  transaction_count: number;
  unique_users: number;
  period_start: string;
  period_end: string;
}

export interface AnalyticsDashboard {
  total_volume_usd?: string;
  total_transactions?: number;
  total_accounts?: number;
  success_rate?: number;
  avg_fee_usd?: string;
  top_countries?: Array<{ country_code: string; volume_usd: string; transaction_count: number }>;
  remittance_flows?: RemittanceFlow[];
  stablecoin_adoption?: StablecoinAdoption[];
  period_start?: string;
  period_end?: string;
}

export interface APIKey {
  id: string;
  key_name: string;
  key_prefix: string;
  permissions: string[];
  rate_limit: number;
  is_active: boolean;
  last_used?: string;
  usage_count: number;
  created_at: string;
  expires_at?: string;
}

export interface APIKeyWithSecret {
  id: string;
  key_name: string;
  api_key: string;
  key_prefix: string;
  permissions: string[];
  rate_limit: number;
  is_active: boolean;
  created_at: string;
  expires_at?: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  primary_network: string;
  environment: string;
  webhook_url?: string;
  is_active: boolean;
  is_public: boolean;
  created_at: string;
  updated_at?: string;
}

export interface DeveloperDashboard {
  developer: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
    company?: string;
    role?: string;
    country_code?: string;
    phone?: string;
    is_active: boolean;
    is_verified: boolean;
    created_at: string;
  };
  projects: Project[];
  api_keys: APIKey[];
  stats: {
    total_projects: number;
    total_api_keys: number;
    active_api_keys: number;
    total_usage: number;
  };
}

export interface APIKeyCreateRequest {
  key_name: string;
  permissions: string[];
  rate_limit: number;
  expires_at?: string;
}

export interface APIUsageLog {
  id: string;
  api_key_id: string;
  endpoint: string;
  method: string;
  status_code: number;
  response_time_ms: number;
  timestamp: string;
  error_message?: string;
}

// API Error class
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Base API client class
class APIClient {
  private baseURL: string;
  private apiKey: string;

  constructor(baseURL: string, apiKey: string) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
  }

  private async refreshToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem('rowell_refresh_token');
    if (!refreshToken) {
      return false;
    }

    try {
      // Call refresh endpoint directly without going through request() to avoid recursion
      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.ok) {
        const tokens = await response.json();
        localStorage.setItem('rowell_access_token', tokens.access_token);
        localStorage.setItem('rowell_refresh_token', tokens.refresh_token);
        return true;
      } else {
        // If refresh fails, clear tokens to trigger re-login
        if (response.status === 401) {
          localStorage.removeItem('rowell_access_token');
          localStorage.removeItem('rowell_refresh_token');
        }
        return false;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      return false;
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    retryOn401: boolean = true
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    // Get auth token if available
    let authToken = getAuthToken();
    
    // Build headers - prefer JWT token, only use API key if it's valid format (ri_*)
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    
    // Add authentication header
    if (authToken) {
      // Use JWT token (preferred for logged-in users)
      headers['Authorization'] = `Bearer ${authToken}`;
    } else if (this.apiKey && this.apiKey.startsWith('ri_')) {
      // Only use API key if it's in correct format (starts with 'ri_')
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }
    // If no valid auth, don't send Authorization header (some endpoints may be public)
    
    const config: RequestInit = {
      ...options,
      headers,
    };

    try {
      let response = await fetch(url, config);
      
      // Handle 401 Unauthorized - try to refresh token once
      if (response.status === 401 && retryOn401 && authToken && !this.apiKey?.startsWith('ri_')) {
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Retry the request with new token
          const newToken = getAuthToken();
          if (newToken) {
            headers['Authorization'] = `Bearer ${newToken}`;
            const retryConfig: RequestInit = {
              ...options,
              headers,
            };
            response = await fetch(url, retryConfig);
          }
        }
      }
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new APIError(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData
        );
      }

      return await response.json();
    } catch (error) {
      if (error instanceof APIError) {
        throw error;
      }
      throw new APIError(
        `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        0
      );
    }
  }

  // Account endpoints
  async createAccount(data: {
    network: 'stellar' | 'hedera';
    environment: 'testnet' | 'mainnet';
    account_type: 'user' | 'merchant' | 'anchor' | 'ngo';
    country_code: string;
    region?: string;
    metadata?: Record<string, any>;
  }): Promise<Account> {
    return this.request<Account>('/accounts/create', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getAccount(accountId: string): Promise<Account> {
    return this.request<Account>(`/accounts/${accountId}`);
  }

  async listAccounts(params?: {
    network?: string;
    environment?: string;
    account_type?: string;
    country_code?: string;
    limit?: number;
    offset?: number;
  }): Promise<Account[]> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/accounts/?${queryString}` : '/accounts/';
    
    // Backend returns {accounts: Account[], pagination: {...}} or Account[] (legacy)
    const response = await this.request<{accounts?: Account[], pagination?: any} | Account[]>(endpoint);
    
    // Handle both response formats
    if (Array.isArray(response)) {
      return response;
    }
    if (response && typeof response === 'object' && 'accounts' in response) {
      return (response as {accounts: Account[]}).accounts || [];
    }
    return [];
  }

  async getAccountBalances(accountId: string): Promise<AccountBalance[]> {
    return this.request<AccountBalance[]>(`/accounts/${accountId}/balances`);
  }

  // Secure key retrieval
  async retrieveAccountKey(accountId: string, token: string): Promise<KeyRetrievalResponse> {
    return this.request<KeyRetrievalResponse>(`/accounts/${accountId}/key`, {
      method: 'POST',
      body: JSON.stringify({ token }),
    });
  }

  // Transfer endpoints
  async createTransfer(data: {
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
  }): Promise<Transfer> {
    return this.request<Transfer>('/transfers/create', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getTransfer(transferId: string): Promise<Transfer> {
    return this.request<Transfer>(`/transfers/${transferId}`);
  }

  async listTransfers(params?: {
    from_account?: string;
    to_account?: string;
    network?: string;
    environment?: string;
    status?: string;
    limit?: number;
    offset?: number;
  }): Promise<Transfer[]> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/transfers/?${queryString}` : '/transfers/';
    
    return this.request<Transfer[]>(endpoint);
  }

  // Transaction endpoints
  async getTransaction(transactionHash: string): Promise<Transaction> {
    return this.request<Transaction>(`/transactions/${transactionHash}`);
  }

  async listTransactions(params?: {
    from_account?: string;
    to_account?: string;
    network?: string;
    environment?: string;
    limit?: number;
    offset?: number;
  }): Promise<Transaction[]> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/transactions/?${queryString}` : '/transactions/';
    
    return this.request<Transaction[]>(endpoint);
  }

  // Analytics endpoints
  async getRemittanceFlows(params?: {
    from_country?: string;
    to_country?: string;
    from_region?: string;
    to_region?: string;
    asset_code?: string;
    network?: string;
    period_type?: string;
    limit?: number;
    offset?: number;
  }): Promise<{ flows: RemittanceFlow[]; pagination?: any; filters?: any; sorting?: any; analytics?: any } | RemittanceFlow[]> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/analytics/remittance?${queryString}` : '/analytics/remittance';
    
    // API returns {flows: [...], pagination: {...}, ...} structure
    return this.request<{ flows: RemittanceFlow[]; pagination?: any; filters?: any; sorting?: any; analytics?: any }>(endpoint);
  }

  async getStablecoinAdoption(params?: {
    asset_code?: string;
    network?: string;
    country_code?: string;
    period_type?: string;
    limit?: number;
    offset?: number;
  }): Promise<StablecoinAdoption[]> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/analytics/stablecoin?${queryString}` : '/analytics/stablecoin';
    
    return this.request<StablecoinAdoption[]>(endpoint);
  }

  // Analytics dashboard
  async getAnalyticsDashboard(params?: {
    country_code?: string;
    region?: string;
    period_type?: string;
  }): Promise<AnalyticsDashboard> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/analytics/dashboard?${queryString}` : '/analytics/dashboard';
    
    return this.request<AnalyticsDashboard>(endpoint);
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string; timestamp: string }> {
    return this.request<{ status: string; version: string; timestamp: string }>('/health');
  }

  // Developer endpoints
  async getDeveloperByEmail(email: string): Promise<{ id: string; email: string; [key: string]: any }> {
    return this.request<{ id: string; email: string; [key: string]: any }>(`/developers/by-email/${encodeURIComponent(email)}`);
  }

  async createDeveloper(request: {
    email: string;
    first_name: string;
    last_name: string;
    company?: string;
    country_code?: string;
    phone?: string;
  }): Promise<{ id: string; email: string; [key: string]: any }> {
    return this.request<{ id: string; email: string; [key: string]: any }>(`/developers/register`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getDeveloperDashboard(developerId: string): Promise<DeveloperDashboard> {
    return this.request<DeveloperDashboard>(`/developers/${developerId}/dashboard`);
  }

  async createProject(
    developerId: string,
    request: {
      name: string;
      description?: string;
      primary_network?: string;
      environment?: string;
      webhook_url?: string;
    }
  ): Promise<Project> {
    return this.request<Project>(`/developers/${developerId}/projects`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async createAPIKey(
    developerId: string,
    projectId: string,
    request: APIKeyCreateRequest
  ): Promise<APIKeyWithSecret> {
    return this.request<APIKeyWithSecret>(`/developers/${developerId}/projects/${projectId}/api-keys`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getProjectAPIKeys(developerId: string, projectId: string): Promise<APIKey[]> {
    // This endpoint doesn't exist yet, but we can get it from dashboard
    // For now, return empty array - the dashboard endpoint provides this
    return [];
  }
}

// Create and export the API client instance
export const apiClient = new APIClient(API_BASE_URL, API_KEY);

// Export individual methods for convenience
export const {
  createAccount,
  getAccount,
  listAccounts,
  getAccountBalances,
  createTransfer,
  getTransfer,
  listTransfers,
  getTransaction,
  listTransactions,
  getRemittanceFlows,
  getStablecoinAdoption,
  getAnalyticsDashboard,
  healthCheck,
  retrieveAccountKey,
} = apiClient;
