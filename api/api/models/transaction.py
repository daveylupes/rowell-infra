"""
Transaction models for indexing and analytics
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Numeric, Index
from sqlalchemy.sql import func
from api.core.database import Base
import uuid


class Transaction(Base):
    """Unified transaction model for both Stellar and Hedera"""
    
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Transaction identifiers
    transaction_hash = Column(String(128), unique=True, nullable=False, index=True)
    network = Column(String(20), nullable=False, index=True)  # "stellar" or "hedera"
    environment = Column(String(10), nullable=False, index=True)  # "testnet" or "mainnet"
    
    # Transaction details
    transaction_type = Column(String(30), nullable=False, index=True)  # payment, transfer, token_transfer, etc.
    status = Column(String(20), nullable=False, index=True)  # pending, success, failed
    
    # Participants
    from_account = Column(String(64), nullable=True, index=True)
    to_account = Column(String(64), nullable=True, index=True)
    
    # Asset and amount
    asset_code = Column(String(12), nullable=False, index=True)
    asset_issuer = Column(String(64), nullable=True)
    amount = Column(String(20), nullable=False)  # Store as string to preserve precision
    amount_usd = Column(String(20), nullable=True)  # USD equivalent
    
    # Geographic context
    from_country = Column(String(2), nullable=True, index=True)
    to_country = Column(String(2), nullable=True, index=True)
    from_region = Column(String(50), nullable=True, index=True)
    to_region = Column(String(50), nullable=True, index=True)
    
    # Transaction metadata
    memo = Column(Text, nullable=True)
    transaction_metadata = Column(JSON, nullable=True)
    
    # Fees
    fee = Column(String(20), nullable=True)
    fee_usd = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    ledger_time = Column(DateTime(timezone=True), nullable=True)  # Blockchain timestamp
    
    # Compliance
    compliance_status = Column(String(20), default="pending", nullable=False)  # pending, approved, flagged, rejected
    compliance_flags = Column(JSON, nullable=True)
    risk_score = Column(Numeric(5, 2), nullable=True)  # 0.00 to 100.00
    
    # Indexes for analytics queries
    __table_args__ = (
        Index('idx_tx_network_env', 'network', 'environment'),
        Index('idx_tx_type_status', 'transaction_type', 'status'),
        Index('idx_tx_asset_amount', 'asset_code', 'amount'),
        Index('idx_tx_corridor', 'from_country', 'to_country'),
        Index('idx_tx_region_flow', 'from_region', 'to_region'),
        Index('idx_tx_ledger_time', 'ledger_time'),
        Index('idx_tx_compliance_status', 'compliance_status', 'risk_score'),
    )


class TransactionEvent(Base):
    """Transaction events for real-time tracking"""
    
    __tablename__ = "transaction_events"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String(36), nullable=False, index=True)
    transaction_hash = Column(String(128), nullable=False, index=True)
    
    # Event details
    event_type = Column(String(30), nullable=False, index=True)  # created, submitted, confirmed, failed
    event_data = Column(JSON, nullable=True)
    
    # Network context
    network = Column(String(20), nullable=False, index=True)
    environment = Column(String(10), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    blockchain_timestamp = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_event_tx_hash', 'transaction_hash'),
        Index('idx_event_type_time', 'event_type', 'created_at'),
        Index('idx_event_network_env', 'network', 'environment'),
    )


class PaymentCorridor(Base):
    """Track payment corridors for analytics"""
    
    __tablename__ = "payment_corridors"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Corridor definition
    from_country = Column(String(2), nullable=False, index=True)
    to_country = Column(String(2), nullable=False, index=True)
    from_region = Column(String(50), nullable=True, index=True)
    to_region = Column(String(50), nullable=True, index=True)
    
    # Asset and network
    asset_code = Column(String(12), nullable=False, index=True)
    network = Column(String(20), nullable=False, index=True)
    
    # Aggregated metrics (updated periodically)
    total_volume = Column(String(20), default="0", nullable=False)
    total_volume_usd = Column(String(20), default="0", nullable=False)
    transaction_count = Column(Numeric(10, 0), default=0, nullable=False)
    avg_transaction_size = Column(String(20), nullable=True)
    avg_transaction_size_usd = Column(String(20), nullable=True)
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    period_type = Column(String(10), nullable=False, index=True)  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_corridor_flow', 'from_country', 'to_country', 'asset_code'),
        Index('idx_corridor_region_flow', 'from_region', 'to_region', 'asset_code'),
        Index('idx_corridor_period', 'period_type', 'period_start', 'period_end'),
        Index('idx_corridor_network_asset', 'network', 'asset_code'),
    )
