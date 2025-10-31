"""
Account schemas for API requests and responses
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AccountBase(BaseModel):
    """Base account schema"""
    account_type: str = Field(..., description="Type of account: user, merchant, anchor, ngo")
    country_code: Optional[str] = Field(None, description="ISO country code")
    region: Optional[str] = Field(None, description="Geographic region")
    account_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional account data")


class AccountCreate(AccountBase):
    """Schema for creating a new account"""
    network: str = Field(..., description="Blockchain network: stellar or hedera")
    environment: str = Field(..., description="Environment: testnet or mainnet")


class AccountUpdate(BaseModel):
    """Schema for updating an account"""
    account_type: Optional[str] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    account_metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_compliant: Optional[bool] = None
    kyc_status: Optional[str] = None


class AccountResponse(AccountBase):
    """Schema for account responses"""
    id: str
    account_id: str
    network: str
    environment: str
    is_active: bool
    is_verified: bool
    is_compliant: bool
    kyc_status: str
    kyc_provider: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_activity: Optional[datetime] = None

    class Config:
        from_attributes = True
