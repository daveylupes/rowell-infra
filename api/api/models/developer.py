"""
Developer and user management models
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from api.core.database import Base


class Developer(Base):
    """Developer user model"""
    __tablename__ = "developers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    company = Column(String(255), nullable=True)
    role = Column(String(100), nullable=True)  # CTO, Developer, etc.
    country_code = Column(String(2), nullable=True)  # ISO country code
    phone = Column(String(20), nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    projects = relationship("Project", back_populates="developer", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="developer", cascade="all, delete-orphan")


class Project(Base):
    """Developer project model"""
    __tablename__ = "projects"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    developer_id = Column(String(36), ForeignKey("developers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Project settings
    primary_network = Column(String(20), default="stellar")  # stellar, hedera
    environment = Column(String(20), default="testnet")  # testnet, mainnet
    webhook_url = Column(String(500), nullable=True)
    
    # Project status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    developer = relationship("Developer", back_populates="projects")
    api_keys = relationship("APIKey", back_populates="project", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="project", cascade="all, delete-orphan")


class APIKey(Base):
    """API key model for authentication"""
    __tablename__ = "api_keys"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    developer_id = Column(String(36), ForeignKey("developers.id"), nullable=False)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    
    # API key details
    key_name = Column(String(255), nullable=False)  # User-friendly name
    key_hash = Column(String(255), nullable=False, unique=True, index=True)  # Hashed key
    key_prefix = Column(String(20), nullable=False)  # First 8 chars for identification
    
    # Permissions
    permissions = Column(JSON, nullable=False, default=list)  # ["accounts:read", "transfers:write"]
    rate_limit = Column(Integer, default=1000)  # Requests per hour
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime(timezone=True), nullable=True)
    usage_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    developer = relationship("Developer", back_populates="api_keys")
    project = relationship("Project", back_populates="api_keys")


class DeveloperSession(Base):
    """Developer session management"""
    __tablename__ = "developer_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    developer_id = Column(String(36), ForeignKey("developers.id"), nullable=False)
    session_token = Column(String(255), nullable=False, unique=True, index=True)
    
    # Session details
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    developer = relationship("Developer")
