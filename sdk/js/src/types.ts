/**
 * Type definitions for Rowell Infra SDK
 */

// Basic types
export type Network = 'stellar' | 'hedera';
export type Environment = 'testnet' | 'mainnet';
export type AccountType = 'user' | 'merchant' | 'anchor' | 'ngo';
export type TransactionType = 'payment' | 'transfer' | 'token_transfer';
export type TransactionStatus = 'pending' | 'success' | 'failed';
export type ComplianceStatus = 'pending' | 'approved' | 'flagged' | 'rejected';
export type KYCStatus = 'pending' | 'verified' | 'rejected' | 'expired';
export type FlagSeverity = 'low' | 'medium' | 'high' | 'critical';
export type FlagType = 'aml' | 'kyc' | 'sanctions' | 'risk';
export type VerificationType = 'individual' | 'business' | 'ngo';
export type DocumentType = 'passport' | 'national_id' | 'drivers_license' | 'bvn';
export type PeriodType = 'daily' | 'weekly' | 'monthly' | 'quarterly';

// Configuration
export interface RowellConfig {
  baseUrl: string;
  apiKey?: string;
  timeout?: number;
  headers?: Record<string, string>;
  retry?: {
    maxRetries?: number;
    baseDelay?: number;
    maxDelay?: number;
    backoffFactor?: number;
    retryCondition?: (error: any) => boolean;
  };
  enableLogging?: boolean;
}

// Account types
export interface Account {
  id: string;
  account_id: string;
  network: Network;
  environment: Environment;
  account_type: AccountType;
  country_code?: string;
  region?: string;
  is_active: boolean;
  is_verified: boolean;
  is_compliant: boolean;
  kyc_status: KYCStatus;
  created_at: string;
  updated_at: string;
  last_activity?: string;
  metadata?: Record<string, any>;
}

export interface AccountBalance {
  account_id: string;
  network: Network;
  asset_code: string;
  asset_issuer?: string;
  balance: string;
  balance_usd?: string;
  updated_at: string;
}

export interface CreateAccountRequest {
  network: Network;
  environment: Environment;
  account_type: AccountType;
  country_code?: string;
  region?: string;
  metadata?: Record<string, any>;
}

// Transfer types
export interface TransferRequest {
  from_account: string;
  to_account: string;
  asset_code: string;
  asset_issuer?: string;
  amount: string;
  network: Network;
  environment: Environment;
  memo?: string;
  from_country?: string;
  to_country?: string;
  metadata?: Record<string, any>;
}

export interface Transfer {
  id: string;
  transaction_hash: string;
  network: Network;
  environment: Environment;
  transaction_type: TransactionType;
  status: TransactionStatus;
  from_account?: string;
  to_account?: string;
  asset_code: string;
  asset_issuer?: string;
  amount: string;
  amount_usd?: string;
  from_country?: string;
  to_country?: string;
  from_region?: string;
  to_region?: string;
  memo?: string;
  fee?: string;
  fee_usd?: string;
  created_at: string;
  updated_at: string;
  ledger_time?: string;
  compliance_status: ComplianceStatus;
  risk_score?: number;
}

export interface TransferStatus {
  transaction_hash: string;
  status: TransactionStatus;
  compliance_status: ComplianceStatus;
  risk_score?: number;
  ledger_time?: string;
  events: Array<{
    event_type: string;
    timestamp: string;
    data?: Record<string, any>;
  }>;
}

// Analytics types
export interface RemittanceFlow {
  from_country: string;
  to_country: string;
  from_region?: string;
  to_region?: string;
  asset_code: string;
  network: Network;
  total_volume: string;
  total_volume_usd: string;
  transaction_count: number;
  unique_senders: number;
  unique_receivers: number;
  avg_transaction_size?: string;
  avg_transaction_size_usd?: string;
  avg_fee?: string;
  avg_fee_usd?: string;
  avg_settlement_time?: number;
  success_rate?: number;
  period_start: string;
  period_end: string;
  period_type: PeriodType;
}

export interface StablecoinAdoption {
  asset_code: string;
  network: Network;
  country_code?: string;
  region?: string;
  total_volume: string;
  total_volume_usd: string;
  transaction_count: number;
  unique_users: number;
  avg_transaction_size?: string;
  avg_transaction_size_usd?: string;
  volume_growth_rate?: number;
  user_growth_rate?: number;
  period_start: string;
  period_end: string;
  period_type: PeriodType;
}

export interface MerchantActivity {
  merchant_id: string;
  merchant_name?: string;
  merchant_type: string;
  country_code: string;
  region?: string;
  total_volume: string;
  total_volume_usd: string;
  transaction_count: number;
  unique_customers: number;
  avg_transaction_size?: string;
  avg_transaction_size_usd?: string;
  stellar_volume: string;
  hedera_volume: string;
  stellar_transactions: number;
  hedera_transactions: number;
  period_start: string;
  period_end: string;
  period_type: PeriodType;
}

export interface NetworkMetrics {
  network: Network;
  environment: Environment;
  total_transactions: number;
  total_volume: string;
  total_volume_usd: string;
  active_accounts: number;
  new_accounts: number;
  avg_transaction_fee?: string;
  avg_transaction_fee_usd?: string;
  avg_confirmation_time?: number;
  success_rate?: number;
  africa_transaction_count: number;
  africa_volume: string;
  africa_volume_usd: string;
  period_start: string;
  period_end: string;
  period_type: PeriodType;
}

// Compliance types
export interface KYCVerification {
  id: string;
  verification_id: string;
  account_id: string;
  network: Network;
  verification_type: VerificationType;
  verification_status: KYCStatus;
  provider: string;
  verification_score?: number;
  risk_level?: string;
  verification_notes?: string;
  created_at: string;
  updated_at: string;
  verified_at?: string;
  expires_at?: string;
}

export interface CreateKYCVerificationRequest {
  account_id: string;
  network: Network;
  verification_type: VerificationType;
  first_name?: string;
  last_name?: string;
  date_of_birth?: string;
  nationality?: string;
  document_type?: DocumentType;
  document_number?: string;
  document_country?: string;
  bvn?: string;
  nin?: string;
  sa_id_number?: string;
  ghana_card?: string;
}

export interface ComplianceFlag {
  id: string;
  entity_type: 'account' | 'transaction';
  entity_id: string;
  network: Network;
  flag_type: FlagType;
  flag_severity: FlagSeverity;
  flag_status: 'active' | 'resolved' | 'false_positive';
  flag_reason: string;
  risk_score?: number;
  country_code?: string;
  region?: string;
  resolved_by?: string;
  resolution_notes?: string;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
}

export interface CreateComplianceFlagRequest {
  entity_type: 'account' | 'transaction';
  entity_id: string;
  network: Network;
  flag_type: FlagType;
  flag_severity: FlagSeverity;
  flag_reason: string;
  flag_data?: Record<string, any>;
  country_code?: string;
  region?: string;
}

export interface ComplianceReport {
  id: string;
  report_type: string;
  report_period: PeriodType;
  country_code?: string;
  region?: string;
  total_verifications: number;
  successful_verifications: number;
  failed_verifications: number;
  pending_verifications: number;
  total_flags: number;
  active_flags: number;
  resolved_flags: number;
  false_positive_flags: number;
  avg_risk_score?: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  period_start: string;
  period_end: string;
  summary?: string;
  created_at: string;
}

// Query parameters
export interface ListAccountsParams {
  network?: Network;
  environment?: Environment;
  account_type?: AccountType;
  country_code?: string;
  limit?: number;
  offset?: number;
}

export interface ListTransfersParams {
  from_account?: string;
  to_account?: string;
  network?: Network;
  environment?: Environment;
  asset_code?: string;
  status?: TransactionStatus;
  from_country?: string;
  to_country?: string;
  limit?: number;
  offset?: number;
}

export interface ListTransactionsParams {
  from_account?: string;
  to_account?: string;
  network?: Network;
  environment?: Environment;
  transaction_type?: TransactionType;
  status?: TransactionStatus;
  asset_code?: string;
  from_country?: string;
  to_country?: string;
  from_region?: string;
  to_region?: string;
  compliance_status?: ComplianceStatus;
  limit?: number;
  offset?: number;
}

export interface GetRemittanceFlowsParams {
  from_country?: string;
  to_country?: string;
  from_region?: string;
  to_region?: string;
  asset_code?: string;
  network?: Network;
  period_type?: PeriodType;
  limit?: number;
  offset?: number;
}

export interface GetStablecoinAdoptionParams {
  asset?: string;
  country_code?: string;
  region?: string;
  network?: Network;
  period_type?: PeriodType;
  limit?: number;
  offset?: number;
}

export interface GetMerchantActivityParams {
  merchant_type?: string;
  country_code?: string;
  region?: string;
  period_type?: PeriodType;
  limit?: number;
  offset?: number;
}

export interface GetNetworkMetricsParams {
  network?: Network;
  environment?: Environment;
  period_type?: PeriodType;
  limit?: number;
  offset?: number;
}

export interface ListComplianceFlagsParams {
  entity_type?: 'account' | 'transaction';
  flag_type?: FlagType;
  flag_severity?: FlagSeverity;
  flag_status?: 'active' | 'resolved' | 'false_positive';
  network?: Network;
  country_code?: string;
  region?: string;
  limit?: number;
  offset?: number;
}

export interface GetComplianceReportsParams {
  report_type?: string;
  report_period?: PeriodType;
  country_code?: string;
  region?: string;
  limit?: number;
  offset?: number;
}

// Error types
export interface RowellError {
  message: string;
  code?: string;
  details?: Record<string, any>;
  timestamp: string;
}

// Response types
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}
