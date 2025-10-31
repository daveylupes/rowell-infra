"""
Analytics schemas for API requests and responses
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class AnalyticsRequest(BaseModel):
    """Schema for analytics requests"""
    from_country: Optional[str] = Field(None, description="Source country code")
    to_country: Optional[str] = Field(None, description="Destination country code")
    asset_code: Optional[str] = Field(None, description="Asset code filter")
    network: Optional[str] = Field(None, description="Network filter")
    period_type: Optional[str] = Field("monthly", description="Period type: daily, weekly, monthly, quarterly")
    start_date: Optional[datetime] = Field(None, description="Start date for analysis")
    end_date: Optional[datetime] = Field(None, description="End date for analysis")


class RemittanceFlow(BaseModel):
    """Remittance flow analytics data"""
    from_country: str
    to_country: str
    from_region: Optional[str] = None
    to_region: Optional[str] = None
    asset_code: str
    network: str
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
    period_start: datetime
    period_end: datetime
    period_type: str


class StablecoinAdoption(BaseModel):
    """Stablecoin adoption analytics data"""
    asset_code: str
    network: str
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
    period_start: datetime
    period_end: datetime
    period_type: str


class AnalyticsResponse(BaseModel):
    """Schema for analytics responses"""
    remittance_flows: List[RemittanceFlow] = Field(default_factory=list)
    stablecoin_adoption: List[StablecoinAdoption] = Field(default_factory=list)
    total_volume_usd: Optional[str] = None
    total_transactions: Optional[int] = None
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
