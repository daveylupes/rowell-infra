import { AxiosInstance } from 'axios';
import {
  KYCVerification,
  ComplianceFlag,
  ComplianceReport,
  CreateKYCVerificationRequest,
  CreateComplianceFlagRequest,
  ListComplianceFlagsParams,
  GetComplianceReportsParams,
  PaginatedResponse,
  ApiResponse
} from '../types';

/**
 * Compliance service for KYC and compliance operations
 */
export class ComplianceService {
  constructor(private httpClient: AxiosInstance) {}

  /**
   * Initiate KYC verification
   */
  async initiateKYC(request: CreateKYCVerificationRequest): Promise<KYCVerification> {
    const response = await this.httpClient.post<ApiResponse<KYCVerification>>(
      '/api/v1/compliance/verify-id',
      request
    );
    return response.data.data;
  }

  /**
   * Get KYC verification status
   */
  async getKYCStatus(verificationId: string): Promise<KYCVerification> {
    const response = await this.httpClient.get<ApiResponse<KYCVerification>>(
      `/api/v1/compliance/verify-id/${verificationId}`
    );
    return response.data.data;
  }

  /**
   * List KYC verifications
   */
  async listKYCVerifications(params: {
    account_id?: string;
    verification_status?: string;
    verification_type?: string;
    network?: string;
    limit?: number;
    offset?: number;
  } = {}): Promise<PaginatedResponse<KYCVerification>> {
    const response = await this.httpClient.get<PaginatedResponse<KYCVerification>>(
      '/api/v1/compliance/verifications',
      { params }
    );
    return response.data;
  }

  /**
   * Update KYC verification
   */
  async updateKYC(
    verificationId: string,
    updates: {
      verification_status?: string;
      verification_notes?: string;
      risk_level?: string;
    }
  ): Promise<KYCVerification> {
    const response = await this.httpClient.patch<ApiResponse<KYCVerification>>(
      `/api/v1/compliance/verify-id/${verificationId}`,
      updates
    );
    return response.data.data;
  }

  /**
   * Create compliance flag
   */
  async createFlag(request: CreateComplianceFlagRequest): Promise<ComplianceFlag> {
    const response = await this.httpClient.post<ApiResponse<ComplianceFlag>>(
      '/api/v1/compliance/flag-transaction',
      request
    );
    return response.data.data;
  }

  /**
   * List compliance flags
   */
  async listFlags(params: ListComplianceFlagsParams = {}): Promise<{
    flags: PaginatedResponse<ComplianceFlag>;
    summary: {
      total_flags: number;
      active_flags: number;
      resolved_flags: number;
      false_positive_flags: number;
      high_risk_flags: number;
      medium_risk_flags: number;
      low_risk_flags: number;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/compliance/flags', {
      params
    });
    return response.data.data;
  }

  /**
   * Get compliance flag details
   */
  async getFlagDetails(flagId: string): Promise<ComplianceFlag & {
    history: Array<{
      action: string;
      timestamp: string;
      user?: string;
      notes?: string;
    }>;
    entity_info: {
      entity_type: string;
      entity_id: string;
      name?: string;
      network: string;
      created_at: string;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>(
      `/api/v1/compliance/flags/${flagId}`
    );
    return response.data.data;
  }

  /**
   * Update compliance flag status
   */
  async updateFlagStatus(
    flagId: string,
    updates: {
      flag_status: 'active' | 'resolved' | 'false_positive';
      resolution_notes?: string;
      resolved_by?: string;
    }
  ): Promise<ComplianceFlag> {
    const response = await this.httpClient.patch<ApiResponse<ComplianceFlag>>(
      `/api/v1/compliance/flags/${flagId}/status`,
      updates
    );
    return response.data.data;
  }

  /**
   * Get compliance flag analytics
   */
  async getFlagAnalytics(params: {
    start_date?: string;
    end_date?: string;
    network?: string;
    country_code?: string;
    region?: string;
  } = {}): Promise<{
    summary: {
      total_flags: number;
      active_flags: number;
      resolved_flags: number;
      false_positive_flags: number;
      avg_resolution_time: number;
    };
    severity_breakdown: Array<{
      severity: string;
      count: number;
      percentage: number;
    }>;
    type_breakdown: Array<{
      flag_type: string;
      count: number;
      percentage: number;
    }>;
    network_breakdown: Array<{
      network: string;
      flag_count: number;
      resolution_rate: number;
    }>;
    top_countries: Array<{
      country_code: string;
      country_name: string;
      flag_count: number;
      resolution_rate: number;
    }>;
    trend_analysis: Array<{
      period: string;
      flag_count: number;
      resolution_count: number;
      avg_resolution_time: number;
    }>;
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/compliance/flags/analytics', {
      params
    });
    return response.data.data;
  }

  /**
   * Get compliance reports
   */
  async getComplianceReports(params: GetComplianceReportsParams = {}): Promise<
    PaginatedResponse<ComplianceReport>
  > {
    const response = await this.httpClient.get<PaginatedResponse<ComplianceReport>>(
      '/api/v1/compliance/reports',
      { params }
    );
    return response.data;
  }

  /**
   * Generate compliance report
   */
  async generateReport(params: {
    report_type: string;
    report_period: string;
    country_code?: string;
    region?: string;
    include_details?: boolean;
  }): Promise<{
    report_id: string;
    status: string;
    generated_at: string;
    download_url?: string;
    expires_at?: string;
  }> {
    const response = await this.httpClient.post<ApiResponse<any>>(
      '/api/v1/compliance/reports/generate',
      params
    );
    return response.data.data;
  }

  /**
   * Get compliance health status
   */
  async getHealth(): Promise<{
    status: string;
    kyc_provider_status: string;
    sanctions_list_status: string;
    risk_engine_status: string;
    last_updated: string;
    performance_metrics: {
      avg_kyc_processing_time: number;
      sanctions_check_success_rate: number;
      risk_score_accuracy: number;
    };
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/compliance/health');
    return response.data.data;
  }

  /**
   * Search compliance entities
   */
  async searchEntities(params: {
    query: string;
    entity_type?: 'account' | 'transaction' | 'verification' | 'flag';
    network?: string;
    limit?: number;
    offset?: number;
  }): Promise<{
    accounts: Array<{
      id: string;
      account_id: string;
      network: string;
      kyc_status: string;
      compliance_status: string;
      risk_score?: number;
    }>;
    transactions: Array<{
      id: string;
      transaction_hash: string;
      network: string;
      compliance_status: string;
      risk_score?: number;
      amount: string;
      asset_code: string;
    }>;
    verifications: Array<{
      id: string;
      verification_id: string;
      account_id: string;
      verification_status: string;
      verification_type: string;
    }>;
    flags: Array<{
      id: string;
      entity_type: string;
      entity_id: string;
      flag_type: string;
      flag_severity: string;
      flag_status: string;
    }>;
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>('/api/v1/compliance/search', {
      params
    });
    return response.data.data;
  }

  /**
   * Get risk assessment for an entity
   */
  async getRiskAssessment(entityType: 'account' | 'transaction', entityId: string): Promise<{
    entity_type: string;
    entity_id: string;
    risk_score: number;
    risk_level: string;
    risk_factors: Array<{
      factor: string;
      weight: number;
      impact: string;
      description: string;
    }>;
    recommendations: Array<{
      action: string;
      priority: string;
      description: string;
    }>;
    last_assessed: string;
  }> {
    const response = await this.httpClient.get<ApiResponse<any>>(
      `/api/v1/compliance/risk-assessment/${entityType}/${entityId}`
    );
    return response.data.data;
  }
}
