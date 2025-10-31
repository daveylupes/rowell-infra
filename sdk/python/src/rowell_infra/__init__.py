"""
Rowell Infra Python SDK
Alchemy for Africa: Stellar + Hedera APIs & Analytics
"""

from .client import RowellClient
from .services import AccountService, TransferService, AnalyticsService, ComplianceService
from .types import (
    Network,
    Environment,
    AccountType,
    TransactionType,
    TransactionStatus,
    ComplianceStatus,
    KYCStatus,
    FlagSeverity,
    FlagType,
    VerificationType,
    DocumentType,
    PeriodType,
    Account,
    AccountBalance,
    Transfer,
    TransferRequest,
    RemittanceFlow,
    StablecoinAdoption,
    MerchantActivity,
    NetworkMetrics,
    KYCVerification,
    ComplianceFlag,
    ComplianceReport,
)

__version__ = "1.0.0"
__author__ = "Rowell Infra Team"
__email__ = "sdk@rowell-infra.com"

# Constants
NETWORKS = {
    "STELLAR": "stellar",
    "HEDERA": "hedera"
}

ENVIRONMENTS = {
    "TESTNET": "testnet",
    "MAINNET": "mainnet"
}

ACCOUNT_TYPES = {
    "USER": "user",
    "MERCHANT": "merchant",
    "ANCHOR": "anchor",
    "NGO": "ngo"
}

TRANSACTION_TYPES = {
    "PAYMENT": "payment",
    "TRANSFER": "transfer",
    "TOKEN_TRANSFER": "token_transfer"
}

TRANSACTION_STATUS = {
    "PENDING": "pending",
    "SUCCESS": "success",
    "FAILED": "failed"
}

COMPLIANCE_STATUS = {
    "PENDING": "pending",
    "APPROVED": "approved",
    "FLAGGED": "flagged",
    "REJECTED": "rejected"
}

KYC_STATUS = {
    "PENDING": "pending",
    "VERIFIED": "verified",
    "REJECTED": "rejected",
    "EXPIRED": "expired"
}

FLAG_SEVERITY = {
    "LOW": "low",
    "MEDIUM": "medium",
    "HIGH": "high",
    "CRITICAL": "critical"
}

FLAG_TYPES = {
    "AML": "aml",
    "KYC": "kyc",
    "SANCTIONS": "sanctions",
    "RISK": "risk"
}

__all__ = [
    "RowellClient",
    "AccountService",
    "TransferService",
    "AnalyticsService",
    "ComplianceService",
    "Network",
    "Environment",
    "AccountType",
    "TransactionType",
    "TransactionStatus",
    "ComplianceStatus",
    "KYCStatus",
    "FlagSeverity",
    "FlagType",
    "VerificationType",
    "DocumentType",
    "PeriodType",
    "Account",
    "AccountBalance",
    "Transfer",
    "TransferRequest",
    "RemittanceFlow",
    "StablecoinAdoption",
    "MerchantActivity",
    "NetworkMetrics",
    "KYCVerification",
    "ComplianceFlag",
    "ComplianceReport",
    "NETWORKS",
    "ENVIRONMENTS",
    "ACCOUNT_TYPES",
    "TRANSACTION_TYPES",
    "TRANSACTION_STATUS",
    "COMPLIANCE_STATUS",
    "KYC_STATUS",
    "FLAG_SEVERITY",
    "FLAG_TYPES",
]
