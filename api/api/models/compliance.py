"""
Compliance and KYC models
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, Numeric, Index
from sqlalchemy.sql import func
from api.core.database import Base
import uuid


class KYCVerification(Base):
    """KYC verification records"""
    
    __tablename__ = "kyc_verifications"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Account reference
    account_id = Column(String(64), nullable=False, index=True)
    network = Column(String(20), nullable=False, index=True)
    
    # Verification details
    verification_id = Column(String(100), unique=True, nullable=False, index=True)
    verification_type = Column(String(30), nullable=False, index=True)  # individual, business, ngo
    verification_status = Column(String(20), nullable=False, index=True)  # pending, verified, rejected, expired
    
    # Personal information (encrypted in production)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(DateTime(timezone=True), nullable=True)
    nationality = Column(String(2), nullable=True, index=True)  # ISO country code
    
    # Document information
    document_type = Column(String(30), nullable=True)  # passport, national_id, drivers_license, bvn
    document_number = Column(String(50), nullable=True)
    document_country = Column(String(2), nullable=True, index=True)
    
    # Africa-specific fields
    bvn = Column(String(11), nullable=True)  # Nigeria Bank Verification Number
    nin = Column(String(11), nullable=True)  # Nigeria National Identification Number
    sa_id_number = Column(String(13), nullable=True)  # South Africa ID Number
    ghana_card = Column(String(20), nullable=True)  # Ghana Card Number
    
    # Verification provider
    provider = Column(String(50), nullable=False, index=True)  # mock, jumio, onfido, etc.
    provider_reference = Column(String(100), nullable=True)
    provider_data = Column(JSON, nullable=True)
    
    # Verification results
    verification_score = Column(Numeric(5, 2), nullable=True)  # 0.00 to 100.00
    risk_level = Column(String(10), nullable=True, index=True)  # low, medium, high
    verification_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_kyc_account_network', 'account_id', 'network'),
        Index('idx_kyc_status_type', 'verification_status', 'verification_type'),
        Index('idx_kyc_provider_status', 'provider', 'verification_status'),
        Index('idx_kyc_country_doc', 'document_country', 'document_type'),
        Index('idx_kyc_risk_level', 'risk_level', 'verification_score'),
    )


class ComplianceFlag(Base):
    """Compliance flags for transactions and accounts"""
    
    __tablename__ = "compliance_flags"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Reference to flagged entity
    entity_type = Column(String(20), nullable=False, index=True)  # account, transaction
    entity_id = Column(String(128), nullable=False, index=True)  # account_id or transaction_hash
    network = Column(String(20), nullable=False, index=True)
    
    # Flag details
    flag_type = Column(String(30), nullable=False, index=True)  # aml, kyc, sanctions, risk, etc.
    flag_severity = Column(String(10), nullable=False, index=True)  # low, medium, high, critical
    flag_status = Column(String(20), nullable=False, index=True)  # active, resolved, false_positive
    
    # Flag information
    flag_reason = Column(Text, nullable=False)
    flag_data = Column(JSON, nullable=True)
    risk_score = Column(Numeric(5, 2), nullable=True)  # 0.00 to 100.00
    
    # Geographic context
    country_code = Column(String(2), nullable=True, index=True)
    region = Column(String(50), nullable=True, index=True)
    
    # Resolution
    resolved_by = Column(String(100), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    resolution_data = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_flag_entity_type_id', 'entity_type', 'entity_id'),
        Index('idx_flag_type_severity', 'flag_type', 'flag_severity'),
        Index('idx_flag_status_network', 'flag_status', 'network'),
        Index('idx_flag_country_region', 'country_code', 'region'),
        Index('idx_flag_risk_score', 'risk_score'),
    )


class SanctionsList(Base):
    """Sanctions and watchlist data"""
    
    __tablename__ = "sanctions_list"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Entity details
    entity_name = Column(String(200), nullable=False, index=True)
    entity_type = Column(String(20), nullable=False, index=True)  # individual, organization, vessel
    entity_category = Column(String(30), nullable=False, index=True)  # sanctions, pep, aml, etc.
    
    # Geographic information
    country_code = Column(String(2), nullable=True, index=True)
    region = Column(String(50), nullable=True, index=True)
    
    # Additional identifiers
    aliases = Column(JSON, nullable=True)  # Alternative names
    document_numbers = Column(JSON, nullable=True)  # Passport, ID numbers
    addresses = Column(JSON, nullable=True)
    
    # List information
    list_source = Column(String(50), nullable=False, index=True)  # un, eu, us, ofac, etc.
    list_reference = Column(String(100), nullable=True)
    list_url = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    effective_date = Column(DateTime(timezone=True), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_sanctions_name_type', 'entity_name', 'entity_type'),
        Index('idx_sanctions_category_source', 'entity_category', 'list_source'),
        Index('idx_sanctions_country_region', 'country_code', 'region'),
        Index('idx_sanctions_active_effective', 'is_active', 'effective_date'),
    )


class ComplianceReport(Base):
    """Compliance reports and analytics"""
    
    __tablename__ = "compliance_reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Report details
    report_type = Column(String(30), nullable=False, index=True)  # aml, kyc, sanctions, risk
    report_period = Column(String(10), nullable=False, index=True)  # daily, weekly, monthly, quarterly
    
    # Geographic scope
    country_code = Column(String(2), nullable=True, index=True)
    region = Column(String(50), nullable=True, index=True)
    
    # Report metrics
    total_verifications = Column(Numeric(10, 0), default=0, nullable=False)
    successful_verifications = Column(Numeric(10, 0), default=0, nullable=False)
    failed_verifications = Column(Numeric(10, 0), default=0, nullable=False)
    pending_verifications = Column(Numeric(10, 0), default=0, nullable=False)
    
    total_flags = Column(Numeric(10, 0), default=0, nullable=False)
    active_flags = Column(Numeric(10, 0), default=0, nullable=False)
    resolved_flags = Column(Numeric(10, 0), default=0, nullable=False)
    false_positive_flags = Column(Numeric(10, 0), default=0, nullable=False)
    
    # Risk metrics
    avg_risk_score = Column(Numeric(5, 2), nullable=True)
    high_risk_count = Column(Numeric(10, 0), default=0, nullable=False)
    medium_risk_count = Column(Numeric(10, 0), default=0, nullable=False)
    low_risk_count = Column(Numeric(10, 0), default=0, nullable=False)
    
    # Time period
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Report data
    report_data = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_report_type_period', 'report_type', 'report_period'),
        Index('idx_report_country_region', 'country_code', 'region'),
        Index('idx_report_period_dates', 'period_start', 'period_end'),
    )
