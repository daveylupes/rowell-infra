"""
Configuration settings for Rowell Infra API
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Rowell Infra API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True  # Enable debug mode for CORS and error details
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://rowell:rowell@localhost:5433/rowell_infra"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Stellar Configuration
    STELLAR_TESTNET_URL: str = "https://horizon-testnet.stellar.org"
    STELLAR_MAINNET_URL: str = "https://horizon.stellar.org"
    STELLAR_TESTNET_PASSPHRASE: str = "Test SDF Network ; September 2015"
    STELLAR_MAINNET_PASSPHRASE: str = "Public Global Stellar Network ; September 2015"
    
    # Hedera Configuration
    HEDERA_TESTNET_URL: str = "https://testnet.mirrornode.hedera.com"
    HEDERA_MAINNET_URL: str = "https://mainnet-public.mirrornode.hedera.com"
    HEDERA_TESTNET_NETWORK: str = "testnet"
    HEDERA_MAINNET_NETWORK: str = "mainnet"
    
    # Hedera Test Credentials (for MVP - use testnet operator)
    # These should be set as environment variables for security
    HEDERA_TESTNET_OPERATOR_ID: Optional[str] = None
    HEDERA_TESTNET_OPERATOR_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    # Key encryption key for storing private keys securely
    # Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    KEY_ENCRYPTION_KEY: Optional[str] = None
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",  # Allow Swagger UI to make requests
        "https://rowell-infra.com",
    ]
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Webhook Configuration
    WEBHOOK_SECRET: str = "your-webhook-secret"
    WEBHOOK_TIMEOUT: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_BURST: int = 200
    
    # Compliance
    KYC_PROVIDER: str = "mock"  # mock, jumio, onfido
    COMPLIANCE_WEBHOOK_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
