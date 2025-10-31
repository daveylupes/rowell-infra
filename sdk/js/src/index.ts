/**
 * Rowell Infra JavaScript SDK
 * Alchemy for Africa: Stellar + Hedera APIs & Analytics
 */

export { RowellClient } from './client';
export { AccountService } from './services/account';
export { TransferService } from './services/transfer';
export { AnalyticsService } from './services/analytics';
export { ComplianceService } from './services/compliance';

// Types
export type {
  RowellConfig,
  Network,
  Environment,
  AccountType,
  Account,
  AccountBalance,
  TransferRequest,
  Transfer,
  TransferStatus,
  RemittanceFlow,
  StablecoinAdoption,
  MerchantActivity,
  NetworkMetrics,
  KYCVerification,
  ComplianceFlag,
  ComplianceReport
} from './types';

// Constants
export const NETWORKS = {
  STELLAR: 'stellar',
  HEDERA: 'hedera'
} as const;

export const ENVIRONMENTS = {
  TESTNET: 'testnet',
  MAINNET: 'mainnet'
} as const;

export const ACCOUNT_TYPES = {
  USER: 'user',
  MERCHANT: 'merchant',
  ANCHOR: 'anchor',
  NGO: 'ngo'
} as const;

export const TRANSACTION_TYPES = {
  PAYMENT: 'payment',
  TRANSFER: 'transfer',
  TOKEN_TRANSFER: 'token_transfer'
} as const;

export const TRANSACTION_STATUS = {
  PENDING: 'pending',
  SUCCESS: 'success',
  FAILED: 'failed'
} as const;

export const COMPLIANCE_STATUS = {
  PENDING: 'pending',
  APPROVED: 'approved',
  FLAGGED: 'flagged',
  REJECTED: 'rejected'
} as const;

export const KYC_STATUS = {
  PENDING: 'pending',
  VERIFIED: 'verified',
  REJECTED: 'rejected',
  EXPIRED: 'expired'
} as const;

export const FLAG_SEVERITY = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical'
} as const;

export const FLAG_TYPES = {
  AML: 'aml',
  KYC: 'kyc',
  SANCTIONS: 'sanctions',
  RISK: 'risk'
} as const;
