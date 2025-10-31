"""
Analytics models for tracking and reporting
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Numeric, Index
from sqlalchemy.sql import func
from api.core.database import Base
import uuid


class StablecoinAdoption(Base):
    """Track stablecoin adoption across Africa"""
    
    __tablename__ = "stablecoin_adoption"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Asset details
    asset_code = Column(String(12), nullable=False, index=True)  # USDC, USDT, etc.
    network = Column(String(20), nullable=False, index=True)  # stellar, hedera
    
    # Geographic context
    country_code = Column(String(2), nullable=True, index=True)
    region = Column(String(50), nullable=True, index=True)
    
    # Adoption metrics
    total_volume = Column(String(20), default="0", nullable=False)
    total_volume_usd = Column(String(20), default="0", nullable=False)
    transaction_count = Column(Numeric(10, 0), default=0, nullable=False)
    unique_users = Column(Numeric(10, 0), default=0, nullable=False)
    avg_transaction_size = Column(String(20), nullable=True)
    avg_transaction_size_usd = Column(String(20), nullable=True)
    
    # Growth metrics
    volume_growth_rate = Column(Numeric(5, 2), nullable=True)  # Percentage
    user_growth_rate = Column(Numeric(5, 2), nullable=True)  # Percentage
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    period_type = Column(String(10), nullable=False, index=True)  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_stablecoin_asset_country', 'asset_code', 'country_code'),
        Index('idx_stablecoin_asset_region', 'asset_code', 'region'),
        Index('idx_stablecoin_network_asset', 'network', 'asset_code'),
        Index('idx_stablecoin_period', 'period_type', 'period_start', 'period_end'),
    )


class MerchantActivity(Base):
    """Track merchant and anchor activity"""
    
    __tablename__ = "merchant_activity"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Merchant details
    merchant_id = Column(String(64), nullable=False, index=True)
    merchant_name = Column(String(200), nullable=True)
    merchant_type = Column(String(30), nullable=False, index=True)  # anchor, merchant, ngo, exchange
    
    # Geographic context
    country_code = Column(String(2), nullable=False, index=True)
    region = Column(String(50), nullable=True, index=True)
    
    # Activity metrics
    total_volume = Column(String(20), default="0", nullable=False)
    total_volume_usd = Column(String(20), default="0", nullable=False)
    transaction_count = Column(Numeric(10, 0), default=0, nullable=False)
    unique_customers = Column(Numeric(10, 0), default=0, nullable=False)
    avg_transaction_size = Column(String(20), nullable=True)
    avg_transaction_size_usd = Column(String(20), nullable=True)
    
    # Network activity
    stellar_volume = Column(String(20), default="0", nullable=False)
    hedera_volume = Column(String(20), default="0", nullable=False)
    stellar_transactions = Column(Numeric(10, 0), default=0, nullable=False)
    hedera_transactions = Column(Numeric(10, 0), default=0, nullable=False)
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    period_type = Column(String(10), nullable=False, index=True)  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_merchant_id_type', 'merchant_id', 'merchant_type'),
        Index('idx_merchant_country_region', 'country_code', 'region'),
        Index('idx_merchant_type_period', 'merchant_type', 'period_type'),
        Index('idx_merchant_period', 'period_type', 'period_start', 'period_end'),
    )


class NetworkMetrics(Base):
    """Track overall network metrics and health"""
    
    __tablename__ = "network_metrics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Network details
    network = Column(String(20), nullable=False, index=True)  # stellar, hedera
    environment = Column(String(10), nullable=False, index=True)  # testnet, mainnet
    
    # Network health metrics
    total_transactions = Column(Numeric(15, 0), default=0, nullable=False)
    total_volume = Column(String(20), default="0", nullable=False)
    total_volume_usd = Column(String(20), default="0", nullable=False)
    active_accounts = Column(Numeric(10, 0), default=0, nullable=False)
    new_accounts = Column(Numeric(10, 0), default=0, nullable=False)
    
    # Performance metrics
    avg_transaction_fee = Column(String(20), nullable=True)
    avg_transaction_fee_usd = Column(String(20), nullable=True)
    avg_confirmation_time = Column(Numeric(10, 2), nullable=True)  # seconds
    success_rate = Column(Numeric(5, 2), nullable=True)  # percentage
    
    # Geographic distribution
    africa_transaction_count = Column(Numeric(10, 0), default=0, nullable=False)
    africa_volume = Column(String(20), default="0", nullable=False)
    africa_volume_usd = Column(String(20), default="0", nullable=False)
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    period_type = Column(String(10), nullable=False, index=True)  # hourly, daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_network_env_period', 'network', 'environment', 'period_type'),
        Index('idx_network_period', 'period_type', 'period_start', 'period_end'),
    )


class RemittanceFlow(Base):
    """Track remittance flows between countries"""
    
    __tablename__ = "remittance_flows"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Flow definition
    from_country = Column(String(2), nullable=False, index=True)
    to_country = Column(String(2), nullable=False, index=True)
    from_region = Column(String(50), nullable=True, index=True)
    to_region = Column(String(50), nullable=True, index=True)
    
    # Asset and network
    asset_code = Column(String(12), nullable=False, index=True)
    network = Column(String(20), nullable=False, index=True)
    
    # Flow metrics
    total_volume = Column(String(20), default="0", nullable=False)
    total_volume_usd = Column(String(20), default="0", nullable=False)
    transaction_count = Column(Numeric(10, 0), default=0, nullable=False)
    unique_senders = Column(Numeric(10, 0), default=0, nullable=False)
    unique_receivers = Column(Numeric(10, 0), default=0, nullable=False)
    
    # Cost metrics
    avg_fee = Column(String(20), nullable=True)
    avg_fee_usd = Column(String(20), nullable=True)
    avg_fee_percentage = Column(Numeric(5, 2), nullable=True)
    
    # Time metrics
    avg_settlement_time = Column(Numeric(10, 2), nullable=True)  # minutes
    success_rate = Column(Numeric(5, 2), nullable=True)  # percentage
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    period_type = Column(String(10), nullable=False, index=True)  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_remittance_flow', 'from_country', 'to_country', 'asset_code'),
        Index('idx_remittance_region_flow', 'from_region', 'to_region', 'asset_code'),
        Index('idx_remittance_network_asset', 'network', 'asset_code'),
        Index('idx_remittance_period', 'period_type', 'period_start', 'period_end'),
    )
