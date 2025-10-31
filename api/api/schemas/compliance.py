"""
Compliance schemas for API requests and responses
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class ComplianceRequest(BaseModel):
    """Schema for compliance requests"""
    entity_type: str = Field(..., description="Type of entity: account or transaction")
    entity_id: str = Field(..., description="ID of the entity to check")
    verification_type: Optional[str] = Field(None, description="Type of verification")
    country_code: Optional[str] = Field(None, description="Country code for compliance check")


class KYCVerification(BaseModel):
    """KYC verification data"""
    id: str
    verification_id: str
    account_id: str
    network: str
    verification_type: str
    verification_status: str
    provider: str
    verification_score: Optional[float] = None
    risk_level: Optional[str] = None
    verification_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    verified_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class ComplianceFlag(BaseModel):
    """Compliance flag data"""
    id: str
    entity_type: str
    entity_id: str
    network: str
    flag_type: str
    flag_severity: str
    flag_status: str
    flag_reason: str
    risk_score: Optional[float] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    resolved_by: Optional[str] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None


class ComplianceResponse(BaseModel):
    """Schema for compliance responses"""
    kyc_verifications: List[KYCVerification] = Field(default_factory=list)
    compliance_flags: List[ComplianceFlag] = Field(default_factory=list)
    total_verifications: Optional[int] = None
    total_flags: Optional[int] = None
    compliance_score: Optional[float] = None
