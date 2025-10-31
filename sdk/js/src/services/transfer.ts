import { AxiosInstance } from 'axios';
import {
  Transfer,
  TransferRequest,
  TransferStatus,
  ListTransfersParams,
  PaginatedResponse,
  ApiResponse
} from '../types';

/**
 * Transfer service for managing blockchain transfers
 */
export class TransferService {
  constructor(private httpClient: AxiosInstance) {}

  /**
   * Create a new transfer
   */
  async create(request: TransferRequest): Promise<Transfer> {
    const response = await this.httpClient.post<ApiResponse<Transfer>>('/api/v1/transfers', request);
    return response.data.data;
  }

  /**
   * List transfers with optional filtering and pagination
   */
  async list(params: ListTransfersParams = {}): Promise<PaginatedResponse<Transfer>> {
    const response = await this.httpClient.get<PaginatedResponse<Transfer>>('/api/v1/transfers', {
      params
    });
    return response.data;
  }

  /**
   * Get transfer by ID
   */
  async getById(transferId: string): Promise<Transfer> {
    const response = await this.httpClient.get<ApiResponse<Transfer>>(`/api/v1/transfers/${transferId}`);
    return response.data.data;
  }

  /**
   * Get transfer status with optional additional information
   */
  async getStatus(
    transferId: string,
    options: {
      includeEvents?: boolean;
      includeFees?: boolean;
      includeCompliance?: boolean;
      refreshBlockchain?: boolean;
    } = {}
  ): Promise<TransferStatus & {
    events?: Array<{
      event_type: string;
      timestamp: string;
      data?: Record<string, any>;
    }>;
    fees?: {
      network_fee: string;
      service_fee: string;
      total_fee: string;
      fee_breakdown?: Record<string, string>;
    };
    compliance?: {
      status: string;
      risk_score?: number;
      flags?: Array<{
        type: string;
        severity: string;
        reason: string;
      }>;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>(
      `/api/v1/transfers/${transferId}/status`,
      { params: options }
    );
    return response.data.data;
  }

  /**
   * Get transfer by transaction hash
   */
  async getByTransactionHash(transactionHash: string): Promise<Transfer> {
    const response = await this.httpClient.get<ApiResponse<Transfer>>(
      `/api/v1/transfers/hash/${transactionHash}`
    );
    return response.data.data;
  }

  /**
   * Cancel a pending transfer
   */
  async cancel(transferId: string, reason?: string): Promise<Transfer> {
    const response = await this.httpClient.post<ApiResponse<Transfer>>(
      `/api/v1/transfers/${transferId}/cancel`,
      { reason }
    );
    return response.data.data;
  }

  /**
   * Retry a failed transfer
   */
  async retry(transferId: string): Promise<Transfer> {
    const response = await this.httpClient.post<ApiResponse<Transfer>>(
      `/api/v1/transfers/${transferId}/retry`
    );
    return response.data.data;
  }

  /**
   * Get transfer events/timeline
   */
  async getEvents(transferId: string): Promise<Array<{
    event_type: string;
    timestamp: string;
    data?: Record<string, any>;
    user?: string;
    notes?: string;
  }>> {
    const response = await this.httpClient.get<ApiResponse<any[]>>(
      `/api/v1/transfers/${transferId}/events`
    );
    return response.data.data;
  }

  /**
   * Get transfer fees breakdown
   */
  async getFees(transferId: string): Promise<{
    network_fee: string;
    service_fee: string;
    total_fee: string;
    fee_breakdown?: Record<string, string>;
    currency: string;
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>(
      `/api/v1/transfers/${transferId}/fees`
    );
    return response.data.data;
  }

  /**
   * Get transfer compliance information
   */
  async getCompliance(transferId: string): Promise<{
    status: string;
    risk_score?: number;
    flags?: Array<{
      type: string;
      severity: string;
      reason: string;
      created_at: string;
    }>;
    sanctions_check?: {
      passed: boolean;
      checked_at: string;
    };
    kyc_verification?: {
      required: boolean;
      verified: boolean;
      verified_at?: string;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>(
      `/api/v1/transfers/${transferId}/compliance`
    );
    return response.data.data;
  }

  /**
   * Search transfers by criteria
   */
  async search(criteria: {
    query?: string;
    from_account?: string;
    to_account?: string;
    network?: string;
    environment?: string;
    asset_code?: string;
    status?: string;
    from_date?: string;
    to_date?: string;
    limit?: number;
    offset?: number;
  }): Promise<PaginatedResponse<Transfer>> {
    const response = await this.httpClient.get<PaginatedResponse<Transfer>>(
      '/api/v1/transfers/search',
      { params: criteria }
    );
    return response.data;
  }

  /**
   * Get transfer statistics
   */
  async getStatistics(accountId?: string, params: {
    from_date?: string;
    to_date?: string;
    network?: string;
    environment?: string;
  } = {}): Promise<{
    total_transfers: number;
    total_volume: string;
    total_volume_usd: string;
    success_rate: number;
    avg_transaction_size: string;
    avg_processing_time: number;
    network_breakdown: Record<string, number>;
    asset_breakdown: Record<string, number>;
  }> {
    const url = accountId 
      ? `/api/v1/transfers/statistics/account/${accountId}`
      : '/api/v1/transfers/statistics';
    
    const response = await this.httpClient.get<ApiResponse<any>>(url, { params });
    return response.data.data;
  }

  /**
   * Estimate transfer fees
   */
  async estimateFees(request: {
    from_account: string;
    to_account: string;
    asset_code: string;
    amount: string;
    network: string;
    environment: string;
  }): Promise<{
    network_fee: string;
    service_fee: string;
    total_fee: string;
    currency: string;
    estimated_processing_time: number;
  }> {
    const response = await this.httpClient.post<ApiResponse<any>>(
      '/api/v1/transfers/estimate-fees',
      request
    );
    return response.data.data;
  }
}
