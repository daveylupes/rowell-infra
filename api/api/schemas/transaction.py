"""
Transaction schemas for API requests and responses
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class TransactionBase(BaseModel):
    """Base transaction schema"""
    from_account: str = Field(..., description="Source account ID")
    to_account: str = Field(..., description="Destination account ID")
    asset_code: str = Field(..., description="Asset code (XLM, USDC, HBAR, etc.)")
    amount: str = Field(..., description="Transaction amount")
    memo: Optional[str] = Field(None, description="Transaction memo")
    from_country: Optional[str] = Field(None, description="Source country code")
    to_country: Optional[str] = Field(None, description="Destination country code")


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction"""
    network: str = Field(..., description="Blockchain network: stellar or hedera")
    environment: str = Field(..., description="Environment: testnet or mainnet")
    asset_issuer: Optional[str] = Field(None, description="Asset issuer for Stellar assets")
    transaction_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional transaction data")


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    status: Optional[str] = None
    memo: Optional[str] = None
    transaction_metadata: Optional[Dict[str, Any]] = None


class TransactionResponse(TransactionBase):
    """Schema for transaction responses"""
    id: str
    transaction_hash: str
    network: str
    environment: str
    status: str
    asset_issuer: Optional[str] = None
    amount_usd: Optional[str] = None
    from_region: Optional[str] = None
    to_region: Optional[str] = None
    transaction_metadata: Optional[Dict[str, Any]] = None
    fee: Optional[str] = None
    fee_usd: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    ledger_time: Optional[datetime] = None
    compliance_status: str
    risk_score: Optional[float] = None

    class Config:
        from_attributes = True
