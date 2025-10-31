import { AxiosInstance } from 'axios';
import {
  Account,
  AccountBalance,
  CreateAccountRequest,
  ListAccountsParams,
  PaginatedResponse,
  ApiResponse
} from '../types';

/**
 * Account service for managing blockchain accounts
 */
export class AccountService {
  constructor(private httpClient: AxiosInstance) {}

  /**
   * Create a new account
   */
  async create(request: CreateAccountRequest): Promise<Account> {
    const response = await this.httpClient.post<ApiResponse<Account>>('/api/v1/accounts', request);
    return response.data.data;
  }

  /**
   * List accounts with optional filtering and pagination
   */
  async list(params: ListAccountsParams = {}): Promise<PaginatedResponse<Account>> {
    const response = await this.httpClient.get<PaginatedResponse<Account>>('/api/v1/accounts', {
      params
    });
    return response.data;
  }

  /**
   * Get account by ID
   */
  async getById(accountId: string): Promise<Account> {
    const response = await this.httpClient.get<ApiResponse<Account>>(`/api/v1/accounts/${accountId}`);
    return response.data.data;
  }

  /**
   * Get account details with optional additional information
   */
  async getDetails(
    accountId: string,
    options: {
      includeBalances?: boolean;
      includeTransactions?: boolean;
      includeCompliance?: boolean;
      transactionLimit?: number;
    } = {}
  ): Promise<Account & {
    balances?: AccountBalance[];
    transactions?: any[];
    compliance?: any;
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>(
      `/api/v1/accounts/${accountId}/details`,
      { params: options }
    );
    return response.data.data;
  }

  /**
   * Get account balances
   */
  async getBalances(accountId: string): Promise<AccountBalance[]> {
    const response = await this.httpClient.get<ApiResponse<AccountBalance[]>>(
      `/api/v1/accounts/${accountId}/balances`
    );
    return response.data.data;
  }

  /**
   * Get account transactions
   */
  async getTransactions(
    accountId: string,
    params: {
      limit?: number;
      offset?: number;
      asset_code?: string;
      from_date?: string;
      to_date?: string;
    } = {}
  ): Promise<PaginatedResponse<any>> {
    const response = await this.httpClient.get<PaginatedResponse<any>>(
      `/api/v1/accounts/${accountId}/transactions`,
      { params }
    );
    return response.data;
  }

  /**
   * Update account metadata
   */
  async updateMetadata(accountId: string, metadata: Record<string, any>): Promise<Account> {
    const response = await this.httpClient.patch<ApiResponse<Account>>(
      `/api/v1/accounts/${accountId}/metadata`,
      { metadata }
    );
    return response.data.data;
  }

  /**
   * Update account status
   */
  async updateStatus(
    accountId: string,
    status: {
      is_active?: boolean;
      is_verified?: boolean;
      is_compliant?: boolean;
    }
  ): Promise<Account> {
    const response = await this.httpClient.patch<ApiResponse<Account>>(
      `/api/v1/accounts/${accountId}/status`,
      status
    );
    return response.data.data;
  }

  /**
   * Delete an account
   */
  async delete(accountId: string): Promise<void> {
    await this.httpClient.delete(`/api/v1/accounts/${accountId}`);
  }

  /**
   * Search accounts by criteria
   */
  async search(criteria: {
    query?: string;
    network?: string;
    environment?: string;
    account_type?: string;
    country_code?: string;
    limit?: number;
    offset?: number;
  }): Promise<PaginatedResponse<Account>> {
    const response = await this.httpClient.get<PaginatedResponse<Account>>(
      '/api/v1/accounts/search',
      { params: criteria }
    );
    return response.data;
  }

  /**
   * Get account statistics
   */
  async getStatistics(accountId: string): Promise<{
    total_transactions: number;
    total_volume: string;
    total_volume_usd: string;
    avg_transaction_size: string;
    last_transaction_date?: string;
    created_at: string;
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>(
      `/api/v1/accounts/${accountId}/statistics`
    );
    return response.data.data;
  }
}
