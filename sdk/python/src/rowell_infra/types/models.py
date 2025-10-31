"""
Pydantic models for Rowell Infra Python SDK
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# Basic types
Network = Literal['stellar', 'hedera']
Environment = Literal['testnet', 'mainnet']
AccountType = Literal['user', 'merchant', 'anchor', 'ngo']
TransactionType = Literal['payment', 'transfer', 'token_transfer']
TransactionStatus = Literal['pending', 'success', 'failed']
ComplianceStatus = Literal['pending', 'approved', 'flagged', 'rejected']
KYCStatus = Literal['pending', 'verified', 'rejected', 'expired']
FlagSeverity = Literal['low', 'medium', 'high', 'critical']
FlagType = Literal['aml', 'kyc', 'sanctions', 'risk']
VerificationType = Literal['individual', 'business', 'ngo']
DocumentType = Literal['passport', 'national_id', 'drivers_license', 'bvn']
PeriodType = Literal['daily', 'weekly', 'monthly', 'quarterly']


# Configuration
class RowellConfig(BaseModel):
    """Configuration for Rowell client"""
    base_url: str
    api_key: Optional[str] = None
    timeout: int = 30
    headers: Optional[Dict[str, str]] = None


# Account models
class Account(BaseModel):
    """Account model"""
    id: str
    account_id: str
    network: Network
    environment: Environment
    account_type: AccountType
    country_code: Optional[str] = None
    region: Optional[str] = None
    is_active: bool
    is_verified: bool
    is_compliant: bool
    kyc_status: KYCStatus
    created_at: str
    updated_at: str
    last_activity: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AccountBalance(BaseModel):
    """Account balance model"""
    account_id: str
    network: Network
    asset_code: str
    asset_issuer: Optional[str] = None
    balance: str
    balance_usd: Optional[str] = None
    updated_at: str


class CreateAccountRequest(BaseModel):
    """Request model for creating an account"""
    network: Network
    environment: Environment
    account_type: AccountType
    country_code: Optional[str] = None
    region: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# Transfer models
class Transfer(BaseModel):
    """Transfer model"""
    id: str
    transaction_hash: str
    network: Network
    environment: Environment
    transaction_type: TransactionType
    status: TransactionStatus
    from_account: Optional[str] = None
    to_account: Optional[str] = None
    asset_code: str
    asset_issuer: Optional[str] = None
    amount: str
    amount_usd: Optional[str] = None
    from_country: Optional[str] = None
    to_country: Optional[str] = None
    from_region: Optional[str] = None
    to_region: Optional[str] = None
    memo: Optional[str] = None
    fee: Optional[str] = None
    fee_usd: Optional[str] = None
    created_at: str
    updated_at: str
    ledger_time: Optional[str] = None
    compliance_status: ComplianceStatus
    risk_score: Optional[float] = None


class TransferRequest(BaseModel):
    """Request model for creating a transfer"""
    from_account: str
    to_account: str
    asset_code: str
    asset_issuer: Optional[str] = None
    amount: str
    network: Network
    environment: Environment
    memo: Optional[str] = None
    from_country: Optional[str] = None
    to_country: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TransferStatus(BaseModel):
    """Transfer status model"""
    transaction_hash: str
    status: TransactionStatus
    compliance_status: ComplianceStatus
    risk_score: Optional[float] = None
    ledger_time: Optional[str] = None
    events: List[Dict[str, Any]]


# Analytics models
class RemittanceFlow(BaseModel):
    """Remittance flow analytics model"""
    from_country: str
    to_country: str
    from_region: Optional[str] = None
    to_region: Optional[str] = None
    asset_code: str
    network: Network
    total_volume: str
    total_volume_usd: str
    transaction_count: int
    unique_senders: int
    unique_receivers: int
    avg_transaction_size: Optional[str] = None
    avg_transaction_size_usd: Optional[str] = None
    avg_fee: Optional[str] = None
    avg_fee_usd: Optional[str] = None
    avg_settlement_time: Optional[float] = None
    success_rate: Optional[float] = None
    period_start: str
    period_end: str
    period_type: PeriodType


class StablecoinAdoption(BaseModel):
    """Stablecoin adoption analytics model"""
    asset_code: str
    network: Network
    country_code: Optional[str] = None
    region: Optional[str] = None
    total_volume: str
    total_volume_usd: str
    transaction_count: int
    unique_users: int
    avg_transaction_size: Optional[str] = None
    avg_transaction_size_usd: Optional[str] = None
    volume_growth_rate: Optional[float] = None
    user_growth_rate: Optional[float] = None
    period_start: str
    period_end: str
    period_type: PeriodType


class MerchantActivity(BaseModel):
    """Merchant activity analytics model"""
    merchant_id: str
    merchant_name: Optional[str] = None
    merchant_type: str
    country_code: str
    region: Optional[str] = None
    total_volume: str
    total_volume_usd: str
    transaction_count: int
    unique_customers: int
    avg_transaction_size: Optional[str] = None
    avg_transaction_size_usd: Optional[str] = None
    stellar_volume: str
    hedera_volume: str
    stellar_transactions: int
    hedera_transactions: int
    period_start: str
    period_end: str
    period_type: PeriodType


class NetworkMetrics(BaseModel):
    """Network metrics model"""
    network: Network
    environment: Environment
    total_transactions: int
    total_volume: str
    total_volume_usd: str
    active_accounts: int
    new_accounts: int
    avg_transaction_fee: Optional[str] = None
    avg_transaction_fee_usd: Optional[str] = None
    avg_confirmation_time: Optional[float] = None
    success_rate: Optional[float] = None
    africa_transaction_count: int
    africa_volume: str
    africa_volume_usd: str
    period_start: str
    period_end: str
    period_type: PeriodType


# Compliance models
class KYCVerification(BaseModel):
    """KYC verification model"""
    id: str
    verification_id: str
    account_id: str
    network: Network
    verification_type: VerificationType
    verification_status: KYCStatus
    provider: str
    verification_score: Optional[float] = None
    risk_level: Optional[str] = None
    verification_notes: Optional[str] = None
    created_at: str
    updated_at: str
    verified_at: Optional[str] = None
    expires_at: Optional[str] = None


class CreateKYCVerificationRequest(BaseModel):
    """Request model for KYC verification"""
    account_id: str
    network: Network
    verification_type: VerificationType
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    nationality: Optional[str] = None
    document_type: Optional[DocumentType] = None
    document_number: Optional[str] = None
    document_country: Optional[str] = None
    bvn: Optional[str] = None
    nin: Optional[str] = None
    sa_id_number: Optional[str] = None
    ghana_card: Optional[str] = None


class ComplianceFlag(BaseModel):
    """Compliance flag model"""
    id: str
    entity_type: Literal['account', 'transaction']
    entity_id: str
    network: Network
    flag_type: FlagType
    flag_severity: FlagSeverity
    flag_status: Literal['active', 'resolved', 'false_positive']
    flag_reason: str
    risk_score: Optional[float] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None
    created_at: str
    updated_at: str
    resolved_at: Optional[str] = None


class CreateComplianceFlagRequest(BaseModel):
    """Request model for creating a compliance flag"""
    entity_type: Literal['account', 'transaction']
    entity_id: str
    network: Network
    flag_type: FlagType
    flag_severity: FlagSeverity
    flag_reason: str
    flag_data: Optional[Dict[str, Any]] = None
    country_code: Optional[str] = None
    region: Optional[str] = None


class ComplianceReport(BaseModel):
    """Compliance report model"""
    id: str
    report_type: str
    report_period: PeriodType
    country_code: Optional[str] = None
    region: Optional[str] = None
    total_verifications: int
    successful_verifications: int
    failed_verifications: int
    pending_verifications: int
    total_flags: int
    active_flags: int
    resolved_flags: int
    false_positive_flags: int
    avg_risk_score: Optional[float] = None
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    period_start: str
    period_end: str
    summary: Optional[str] = None
    created_at: str
