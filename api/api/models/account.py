"""
Account models for Stellar and Hedera accounts
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.core.database import Base
import uuid


class Account(Base):
    """Unified account model for both Stellar and Hedera"""
    
    __tablename__ = "accounts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Account identifiers
    account_id = Column(String(64), unique=True, nullable=False, index=True)  # Stellar public key or Hedera account ID
    network = Column(String(20), nullable=False, index=True)  # "stellar" or "hedera"
    environment = Column(String(10), nullable=False, index=True)  # "testnet" or "mainnet"
    
    # Project relationship
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True, index=True)
    
    # Account details
    account_type = Column(String(20), nullable=False)  # "user", "merchant", "anchor", "ngo"
    country_code = Column(String(2), nullable=True, index=True)  # ISO country code
    region = Column(String(50), nullable=True, index=True)  # "east_africa", "west_africa", etc.
    
    # Metadata
    account_metadata = Column(JSON, nullable=True)  # Additional account-specific data
    tags = Column(JSON, nullable=True)  # Tags for categorization
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_compliant = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    # Compliance
    kyc_status = Column(String(20), default="pending", nullable=False)  # pending, verified, rejected
    kyc_provider = Column(String(50), nullable=True)
    kyc_data = Column(JSON, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="accounts")
    
    # Indexes for analytics queries
    __table_args__ = (
        Index('idx_account_network_env', 'network', 'environment'),
        Index('idx_account_country_region', 'country_code', 'region'),
        Index('idx_account_type_status', 'account_type', 'is_active'),
        Index('idx_account_kyc_status', 'kyc_status', 'is_verified'),
        Index('idx_account_project', 'project_id'),
    )


class AccountBalance(Base):
    """Account balance tracking for different assets"""
    
    __tablename__ = "account_balances"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = Column(String(64), nullable=False, index=True)
    network = Column(String(20), nullable=False, index=True)
    
    # Asset details
    asset_code = Column(String(12), nullable=False)  # XLM, USDC, HBAR, etc.
    asset_issuer = Column(String(64), nullable=True)  # For Stellar assets
    asset_type = Column(String(20), nullable=False)  # native, credit_alphanum4, credit_alphanum12
    
    # Balance
    balance = Column(String(20), nullable=False)  # Store as string to preserve precision
    balance_usd = Column(String(20), nullable=True)  # USD equivalent
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_balance_account_asset', 'account_id', 'asset_code'),
        Index('idx_balance_network_asset', 'network', 'asset_code'),
    )


class AccountActivity(Base):
    """Track account activity for analytics"""
    
    __tablename__ = "account_activity"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = Column(String(64), nullable=False, index=True)
    network = Column(String(20), nullable=False, index=True)
    
    # Activity details
    activity_type = Column(String(30), nullable=False)  # transaction_sent, transaction_received, account_created, etc.
    activity_data = Column(JSON, nullable=True)
    
    # Geographic context
    country_code = Column(String(2), nullable=True, index=True)
    region = Column(String(50), nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Indexes for analytics
    __table_args__ = (
        Index('idx_activity_account_type', 'account_id', 'activity_type'),
        Index('idx_activity_network_type', 'network', 'activity_type'),
        Index('idx_activity_country_region', 'country_code', 'region'),
        Index('idx_activity_created_at', 'created_at'),
    )
