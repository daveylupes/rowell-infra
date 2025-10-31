import { AxiosInstance } from 'axios';
import {
  RemittanceFlow,
  StablecoinAdoption,
  MerchantActivity,
  NetworkMetrics,
  GetRemittanceFlowsParams,
  GetStablecoinAdoptionParams,
  GetMerchantActivityParams,
  GetNetworkMetricsParams,
  PaginatedResponse,
  ApiResponse
} from '../types';

/**
 * Analytics service for accessing analytics and reporting data
 */
export class AnalyticsService {
  constructor(private httpClient: AxiosInstance) {}

  /**
   * Get dashboard analytics data
   */
  async getDashboard(params: {
    period_type?: string;
    start_date?: string;
    end_date?: string;
    network?: string;
    environment?: string;
  } = {}): Promise<{
    total_accounts: number;
    total_transaction_volume: string;
    total_transaction_volume_usd: string;
    success_rate: number;
    active_networks: Array<{
      network: string;
      transaction_count: number;
      volume_usd: string;
    }>;
    recent_activity: Array<{
      type: string;
      description: string;
      timestamp: string;
      amount?: string;
      status: string;
    }>;
    top_countries: Array<{
      country_code: string;
      country_name: string;
      transaction_count: number;
      volume_usd: string;
    }>;
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/analytics/dashboard', {
      params
    });
    return response.data.data;
  }

  /**
   * Get remittance flows analytics
   */
  async getRemittanceFlows(params: GetRemittanceFlowsParams = {}): Promise<{
    flows: PaginatedResponse<RemittanceFlow>;
    analytics: {
      summary: {
        total_flows: number;
        total_volume: string;
        total_volume_usd: string;
        avg_flow_size: string;
        top_corridor: string;
      };
      top_corridors: Array<{
        from_country: string;
        to_country: string;
        volume: string;
        volume_usd: string;
        transaction_count: number;
      }>;
      asset_breakdown: Array<{
        asset_code: string;
        volume: string;
        volume_usd: string;
        percentage: number;
      }>;
      regional_breakdown: Array<{
        from_region: string;
        to_region: string;
        volume: string;
        volume_usd: string;
        transaction_count: number;
      }>;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/analytics/remittance-flows', {
      params
    });
    return response.data.data;
  }

  /**
   * Get stablecoin adoption analytics
   */
  async getStablecoinAdoption(params: GetStablecoinAdoptionParams = {}): Promise<{
    adoption_data: PaginatedResponse<StablecoinAdoption>;
    analytics: {
      summary: {
        total_volume: string;
        total_volume_usd: string;
        total_transactions: number;
        unique_users: number;
        avg_transaction_size: string;
      };
      adoption_trends: Array<{
        period: string;
        volume: string;
        volume_usd: string;
        transaction_count: number;
        unique_users: number;
      }>;
      country_breakdown: Array<{
        country_code: string;
        country_name: string;
        volume: string;
        volume_usd: string;
        transaction_count: number;
        unique_users: number;
        adoption_rate: number;
      }>;
      network_comparison: Array<{
        network: string;
        volume: string;
        volume_usd: string;
        transaction_count: number;
        unique_users: number;
      }>;
      volume_analysis: {
        daily_volume: Array<{
          date: string;
          volume: string;
          volume_usd: string;
        }>;
        growth_rate: number;
        volatility: number;
      };
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/analytics/stablecoin-adoption', {
      params
    });
    return response.data.data;
  }

  /**
   * Get merchant activity analytics
   */
  async getMerchantActivity(params: GetMerchantActivityParams = {}): Promise<{
    activity_data: PaginatedResponse<MerchantActivity>;
    analytics: {
      summary: {
        total_merchants: number;
        total_volume: string;
        total_volume_usd: string;
        total_transactions: number;
        unique_customers: number;
        avg_transaction_size: string;
      };
      merchant_type_breakdown: Array<{
        merchant_type: string;
        merchant_count: number;
        volume: string;
        volume_usd: string;
        transaction_count: number;
        avg_transaction_size: string;
      }>;
      network_breakdown: Array<{
        network: string;
        volume: string;
        volume_usd: string;
        transaction_count: number;
        merchant_count: number;
      }>;
      country_breakdown: Array<{
        country_code: string;
        country_name: string;
        merchant_count: number;
        volume: string;
        volume_usd: string;
        transaction_count: number;
      }>;
      regional_breakdown: Array<{
        region: string;
        merchant_count: number;
        volume: string;
        volume_usd: string;
        transaction_count: number;
      }>;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/analytics/merchant-activity', {
      params
    });
    return response.data.data;
  }

  /**
   * Get network metrics analytics
   */
  async getNetworkMetrics(params: GetNetworkMetricsParams = {}): Promise<{
    metrics_data: PaginatedResponse<NetworkMetrics>;
    analytics: {
      summary: {
        total_transactions: number;
        total_volume: string;
        total_volume_usd: string;
        active_accounts: number;
        new_accounts: number;
        avg_transaction_fee: string;
        avg_confirmation_time: number;
        success_rate: number;
        throughput_tps: number;
      };
      network_breakdown: Array<{
        network: string;
        environment: string;
        transaction_count: number;
        volume: string;
        volume_usd: string;
        active_accounts: number;
        new_accounts: number;
        success_rate: number;
      }>;
      period_breakdown: Array<{
        period: string;
        transaction_count: number;
        volume: string;
        volume_usd: string;
        active_accounts: number;
        success_rate: number;
      }>;
      regional_metrics: Array<{
        region: string;
        transaction_count: number;
        volume: string;
        volume_usd: string;
        active_accounts: number;
      }>;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/analytics/network-metrics', {
      params
    });
    return response.data.data;
  }

  /**
   * Get custom analytics report
   */
  async getCustomReport(params: {
    report_type: string;
    dimensions: string[];
    metrics: string[];
    filters?: Record<string, any>;
    start_date?: string;
    end_date?: string;
    group_by?: string[];
    order_by?: string[];
    limit?: number;
    offset?: number;
  }): Promise<{
    report_data: any[];
    summary: Record<string, any>;
    metadata: {
      generated_at: string;
      period: {
        start_date: string;
        end_date: string;
      };
      dimensions: string[];
      metrics: string[];
      filters: Record<string, any>;
    };
  }> {
    const response = await this.httpClient.post<ApiResponse<any>>('/api/v1/analytics/custom-report', params);
    return response.data.data;
  }

  /**
   * Export analytics data
   */
  async exportData(params: {
    data_type: 'remittance_flows' | 'stablecoin_adoption' | 'merchant_activity' | 'network_metrics';
    format: 'csv' | 'json' | 'xlsx';
    filters?: Record<string, any>;
    start_date?: string;
    end_date?: string;
    limit?: number;
  }): Promise<{
    download_url: string;
    expires_at: string;
    file_size: number;
    record_count: number;
  }> {
    const response = await this.httpClient.post<ApiResponse<any>>('/api/v1/analytics/export', params);
    return response.data.data;
  }

  /**
   * Get analytics health status
   */
  async getHealth(): Promise<{
    status: string;
    last_updated: string;
    data_sources: Array<{
      name: string;
      status: string;
      last_sync: string;
      record_count: number;
    }>;
    performance_metrics: {
      avg_query_time: number;
      cache_hit_rate: number;
      data_freshness: number;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/analytics/health');
    return response.data.data;
  }
}
