# 🔧 Backend Architecture - Rowell Infra

> **FastAPI-based backend architecture for African fintech infrastructure**

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Application Structure](#application-structure)
- [Service Layer Design](#service-layer-design)
- [Database Architecture](#database-architecture)
- [API Design](#api-design)
- [Authentication & Security](#authentication--security)
- [Error Handling](#error-handling)
- [Logging & Monitoring](#logging--monitoring)
- [Testing Strategy](#testing-strategy)
- [Performance Optimization](#performance-optimization)
- [Deployment Considerations](#deployment-considerations)

## 🎯 Overview

The Rowell Infra backend is built using **FastAPI** with a focus on high performance, scalability, and developer experience. It provides a unified API for blockchain operations across Stellar and Hedera networks, with comprehensive analytics and compliance features.

### Core Principles

- **Async-First**: Built on Python async/await for high concurrency
- **Type Safety**: Full type hints with Pydantic validation
- **Service-Oriented**: Clean separation between API, service, and data layers
- **Blockchain Agnostic**: Unified interface for multiple blockchain networks
- **Compliance-Ready**: Built-in KYC/AML and regulatory compliance features

## 🛠️ Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.12+**: Latest Python features and performance improvements
- **Uvicorn**: ASGI server for production deployment

### Database & Storage
- **PostgreSQL**: Primary relational database
- **SQLAlchemy 2.0**: Modern async ORM
- **Alembic**: Database migration management
- **Redis**: Caching and session storage

### Task Processing
- **Celery**: Distributed task queue
- **Redis**: Message broker for Celery
- **Flower**: Celery monitoring tool

### Validation & Serialization
- **Pydantic**: Data validation and serialization
- **Pydantic V2**: Latest version with improved performance

### Blockchain Integration
- **Stellar SDK**: Stellar network integration
- **Hedera SDK**: Hedera network integration
- **Web3.py**: Ethereum compatibility (future)

### Monitoring & Observability
- **structlog**: Structured logging
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization

## 🏗️ Application Structure

```
api/
├── main.py                 # Application entry point
├── core/                   # Core configuration and utilities
│   ├── config.py          # Application settings
│   ├── database.py        # Database configuration
│   ├── auth.py            # Authentication logic
│   └── middleware.py      # Custom middleware
├── api/                    # API layer
│   └── v1/                # API version 1
│       ├── api.py         # Main API router
│       └── endpoints/     # API endpoints
│           ├── accounts.py
│           ├── transfers.py
│           ├── analytics.py
│           ├── compliance.py
│           └── developers.py
├── services/               # Business logic layer
│   ├── account_service.py
│   ├── transfer_service.py
│   ├── analytics_service.py
│   ├── compliance_service.py
│   ├── stellar_service.py
│   └── hedera_service.py
├── models/                 # Database models
│   ├── account.py
│   ├── transaction.py
│   ├── analytics.py
│   └── compliance.py
├── schemas/                # Pydantic schemas
│   ├── account.py
│   ├── transaction.py
│   ├── analytics.py
│   └── compliance.py
└── utils/                  # Utility functions
    ├── blockchain.py
    ├── validation.py
    └── helpers.py
```

## 🔧 Service Layer Design

### Service Layer Pattern

The service layer acts as an intermediary between the API endpoints and the data layer, containing all business logic and orchestrating operations across different components.

```python
# Example: AccountService
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.account import Account
from api.schemas.account import AccountCreate, AccountUpdate
from api.services.stellar_service import StellarService
from api.services.hedera_service import HederaService

class AccountService:
    def __init__(
        self,
        db: AsyncSession,
        stellar_service: StellarService,
        hedera_service: HederaService
    ):
        self.db = db
        self.stellar_service = stellar_service
        self.hedera_service = hedera_service
    
    async def create_account(self, account_data: AccountCreate) -> Account:
        """Create a new account on the specified blockchain network"""
        # Validate input data
        validated_data = await self._validate_account_data(account_data)
        
        # Create account on blockchain
        blockchain_account = await self._create_blockchain_account(
            validated_data.network,
            validated_data.environment
        )
        
        # Create database record
        db_account = Account(
            account_id=blockchain_account.account_id,
            network=validated_data.network,
            environment=validated_data.environment,
            account_type=validated_data.account_type,
            country_code=validated_data.country_code,
            metadata=validated_data.metadata
        )
        
        self.db.add(db_account)
        await self.db.commit()
        await self.db.refresh(db_account)
        
        return db_account
    
    async def get_account(self, account_id: str) -> Optional[Account]:
        """Retrieve account information"""
        result = await self.db.execute(
            select(Account).where(Account.account_id == account_id)
        )
        return result.scalar_one_or_none()
    
    async def list_accounts(
        self,
        skip: int = 0,
        limit: int = 100,
        network: Optional[str] = None,
        account_type: Optional[str] = None
    ) -> List[Account]:
        """List accounts with filtering and pagination"""
        query = select(Account)
        
        if network:
            query = query.where(Account.network == network)
        if account_type:
            query = query.where(Account.account_type == account_type)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_account(
        self,
        account_id: str,
        update_data: AccountUpdate
    ) -> Optional[Account]:
        """Update account information"""
        account = await self.get_account(account_id)
        if not account:
            return None
        
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(account, field, value)
        
        await self.db.commit()
        await self.db.refresh(account)
        return account
    
    async def delete_account(self, account_id: str) -> bool:
        """Delete account (soft delete)"""
        account = await self.get_account(account_id)
        if not account:
            return False
        
        account.is_active = False
        account.deleted_at = datetime.utcnow()
        
        await self.db.commit()
        return True
    
    async def _validate_account_data(self, data: AccountCreate) -> AccountCreate:
        """Validate account creation data"""
        # Country code validation
        if not self._is_valid_country_code(data.country_code):
            raise ValueError(f"Invalid country code: {data.country_code}")
        
        # Account type validation
        if data.account_type not in ["user", "merchant", "anchor", "ngo"]:
            raise ValueError(f"Invalid account type: {data.account_type}")
        
        return data
    
    async def _create_blockchain_account(
        self,
        network: str,
        environment: str
    ) -> BlockchainAccount:
        """Create account on blockchain network"""
        if network == "stellar":
            return await self.stellar_service.create_account(environment)
        elif network == "hedera":
            return await self.hedera_service.create_account(environment)
        else:
            raise ValueError(f"Unsupported network: {network}")
    
    def _is_valid_country_code(self, country_code: str) -> bool:
        """Validate African country code"""
        african_countries = [
            "NG", "KE", "ZA", "GH", "UG", "TZ", "ET", "MA", "EG", "TN",
            "DZ", "LY", "SD", "SS", "TD", "NE", "ML", "BF", "CI", "GN",
            "SL", "LR", "SN", "GM", "GW", "GN", "CV", "MR", "MA", "EH"
        ]
        return country_code in african_countries
```

### Service Dependencies

```python
# Dependency injection for services
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.core.database import get_db
from api.services.stellar_service import get_stellar_service
from api.services.hedera_service import get_hedera_service

async def get_account_service(
    db: AsyncSession = Depends(get_db),
    stellar_service: StellarService = Depends(get_stellar_service),
    hedera_service: HederaService = Depends(get_hedera_service)
) -> AccountService:
    return AccountService(db, stellar_service, hedera_service)
```

## 🗄️ Database Architecture

### Database Models

#### Account Model
```python
from sqlalchemy import Column, String, DateTime, JSON, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from api.core.database import Base

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(String(56), unique=True, nullable=False, index=True)
    network = Column(Enum(Network), nullable=False, index=True)
    environment = Column(Enum(Environment), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False, index=True)
    country_code = Column(String(2), nullable=False, index=True)
    region = Column(String(50), index=True)
    metadata = Column(JSON)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="account")
    compliance_records = relationship("ComplianceRecord", back_populates="account")
```

#### Transaction Model
```python
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_hash = Column(String(64), unique=True, nullable=False, index=True)
    from_account_id = Column(String(56), nullable=False, index=True)
    to_account_id = Column(String(56), nullable=False, index=True)
    asset_code = Column(String(12), nullable=False, index=True)
    asset_issuer = Column(String(56), nullable=True)
    amount = Column(Numeric(20, 7), nullable=False)
    network = Column(Enum(Network), nullable=False, index=True)
    environment = Column(Enum(Environment), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False, index=True)
    memo = Column(String(28), nullable=True)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    account = relationship("Account", back_populates="transactions")
```

### Database Configuration

```python
# api/core/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from api.core.config import settings

class Base(DeclarativeBase):
    pass

# Create async engine with connection pooling
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Database Migrations

```python
# alembic/env.py
from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from api.core.database import Base
from api.core.config import settings

# Import all models
from api.models import account, transaction, analytics, compliance

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()
```

## 🔌 API Design

### RESTful API Structure

```python
# api/api/v1/endpoints/accounts.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from api.services.account_service import AccountService, get_account_service
from api.schemas.account import Account, AccountCreate, AccountUpdate

router = APIRouter()

@router.post("/", response_model=Account, status_code=201)
async def create_account(
    account_data: AccountCreate,
    account_service: AccountService = Depends(get_account_service)
) -> Account:
    """Create a new account"""
    try:
        account = await account_service.create_account(account_data)
        return account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Account creation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[Account])
async def list_accounts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    network: Optional[str] = Query(None, description="Filter by network"),
    account_type: Optional[str] = Query(None, description="Filter by account type"),
    country_code: Optional[str] = Query(None, description="Filter by country code"),
    account_service: AccountService = Depends(get_account_service)
) -> List[Account]:
    """List accounts with filtering and pagination"""
    accounts = await account_service.list_accounts(
        skip=skip,
        limit=limit,
        network=network,
        account_type=account_type,
        country_code=country_code
    )
    return accounts

@router.get("/{account_id}", response_model=Account)
async def get_account(
    account_id: str,
    account_service: AccountService = Depends(get_account_service)
) -> Account:
    """Get account by ID"""
    account = await account_service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{account_id}", response_model=Account)
async def update_account(
    account_id: str,
    update_data: AccountUpdate,
    account_service: AccountService = Depends(get_account_service)
) -> Account:
    """Update account information"""
    account = await account_service.update_account(account_id, update_data)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.delete("/{account_id}", status_code=204)
async def delete_account(
    account_id: str,
    account_service: AccountService = Depends(get_account_service)
):
    """Delete account (soft delete)"""
    success = await account_service.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
```

### API Response Format

```python
# Standardized API responses
from typing import Any, Dict, Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    meta: Optional[Dict[str, Any]] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int
```

## 🔐 Authentication & Security

### API Key Authentication

```python
# api/core/auth.py
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.models.developer import Developer
from api.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

security = HTTPBearer()

async def get_current_developer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Developer:
    """Get current developer from API key"""
    api_key = credentials.credentials
    
    # Validate API key format
    if not api_key.startswith("sk_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key format"
        )
    
    # Query database for developer
    result = await db.execute(
        select(Developer).where(
            Developer.api_key == api_key,
            Developer.is_active == True
        )
    )
    developer = result.scalar_one_or_none()
    
    if not developer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    # Check rate limits
    if not await _check_rate_limit(developer, api_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    return developer

async def _check_rate_limit(developer: Developer, api_key: str) -> bool:
    """Check API rate limits"""
    # Implementation would check Redis for rate limiting
    # Return True if within limits, False if exceeded
    pass
```

### Input Validation

```python
# api/schemas/account.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from enum import Enum

class Network(str, Enum):
    STELLAR = "stellar"
    HEDERA = "hedera"

class Environment(str, Enum):
    TESTNET = "testnet"
    MAINNET = "mainnet"

class AccountType(str, Enum):
    USER = "user"
    MERCHANT = "merchant"
    ANCHOR = "anchor"
    NGO = "ngo"

class AccountCreate(BaseModel):
    network: Network
    environment: Environment = Environment.TESTNET
    account_type: AccountType
    country_code: str = Field(..., min_length=2, max_length=2)
    region: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @validator('country_code')
    def validate_country_code(cls, v):
        african_countries = [
            "NG", "KE", "ZA", "GH", "UG", "TZ", "ET", "MA", "EG", "TN"
        ]
        if v.upper() not in african_countries:
            raise ValueError('Country code must be a valid African country')
        return v.upper()
    
    @validator('metadata')
    def validate_metadata(cls, v):
        if v and len(str(v)) > 10000:  # 10KB limit
            raise ValueError('Metadata too large')
        return v

class AccountUpdate(BaseModel):
    region: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @validator('metadata')
    def validate_metadata(cls, v):
        if v and len(str(v)) > 10000:  # 10KB limit
            raise ValueError('Metadata too large')
        return v

class Account(BaseModel):
    id: str
    account_id: str
    network: Network
    environment: Environment
    account_type: AccountType
    country_code: str
    region: Optional[str]
    metadata: Optional[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
```

## ⚠️ Error Handling

### Global Exception Handler

```python
# api/core/exceptions.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog

logger = structlog.get_logger()

class RowellException(Exception):
    """Base exception for Rowell Infra"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class ValidationError(RowellException):
    """Validation error"""
    pass

class BlockchainError(RowellException):
    """Blockchain operation error"""
    pass

class ComplianceError(RowellException):
    """Compliance check error"""
    pass

# Global exception handlers
async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors"""
    logger.warning(
        "Validation error",
        path=request.url.path,
        errors=exc.errors()
    )
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "errors": exc.errors()
        }
    )

async def rowell_exception_handler(
    request: Request, 
    exc: RowellException
) -> JSONResponse:
    """Handle Rowell-specific exceptions"""
    logger.error(
        "Rowell exception",
        path=request.url.path,
        message=exc.message,
        code=exc.code
    )
    
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message,
            "code": exc.code
        }
    )

async def general_exception_handler(
    request: Request, 
    exc: Exception
) -> JSONResponse:
    """Handle general exceptions"""
    logger.error(
        "Unexpected error",
        path=request.url.path,
        error=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error"
        }
    )
```

### Service Layer Error Handling

```python
# In service methods
async def create_account(self, account_data: AccountCreate) -> Account:
    try:
        # Business logic
        validated_data = await self._validate_account_data(account_data)
        blockchain_account = await self._create_blockchain_account(
            validated_data.network,
            validated_data.environment
        )
        
        # Database operations
        db_account = Account(**validated_data.dict())
        self.db.add(db_account)
        await self.db.commit()
        
        return db_account
        
    except ValidationError as e:
        logger.warning("Validation failed", error=str(e))
        raise
    except BlockchainError as e:
        logger.error("Blockchain operation failed", error=str(e))
        await self.db.rollback()
        raise
    except Exception as e:
        logger.error("Unexpected error in account creation", error=str(e))
        await self.db.rollback()
        raise RowellException("Account creation failed")
```

## 📊 Logging & Monitoring

### Structured Logging

```python
# api/core/logging.py
import structlog
from pythonjsonlogger import jsonlogger
import logging

def setup_logging():
    """Setup structured logging"""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure JSON logging for production
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

# Usage in services
logger = structlog.get_logger()

async def create_account(self, account_data: AccountCreate) -> Account:
    logger.info(
        "Creating account",
        network=account_data.network,
        account_type=account_data.account_type,
        country_code=account_data.country_code
    )
    
    try:
        # Business logic
        account = await self._create_account_logic(account_data)
        
        logger.info(
            "Account created successfully",
            account_id=account.account_id,
            network=account.network
        )
        
        return account
        
    except Exception as e:
        logger.error(
            "Account creation failed",
            error=str(e),
            network=account_data.network
        )
        raise
```

### Metrics Collection

```python
# api/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Response

# Define metrics
REQUEST_COUNT = Counter(
    'rowell_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'rowell_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_ACCOUNTS = Gauge(
    'rowell_active_accounts',
    'Number of active accounts'
)

BLOCKCHAIN_TRANSACTIONS = Counter(
    'rowell_blockchain_transactions_total',
    'Total blockchain transactions',
    ['network', 'status']
)

# Middleware for metrics collection
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type="text/plain")
```

## 🧪 Testing Strategy

### Unit Testing

```python
# tests/unit/test_account_service.py
import pytest
from unittest.mock import AsyncMock, Mock
from api.services.account_service import AccountService
from api.schemas.account import AccountCreate
from api.models.account import Account

@pytest.fixture
async def mock_db():
    return AsyncMock()

@pytest.fixture
async def mock_stellar_service():
    return AsyncMock()

@pytest.fixture
async def mock_hedera_service():
    return AsyncMock()

@pytest.fixture
async def account_service(mock_db, mock_stellar_service, mock_hedera_service):
    return AccountService(mock_db, mock_stellar_service, mock_hedera_service)

@pytest.mark.asyncio
async def test_create_account_stellar_success(account_service, mock_stellar_service):
    """Test successful Stellar account creation"""
    # Arrange
    account_data = AccountCreate(
        network="stellar",
        environment="testnet",
        account_type="user",
        country_code="NG"
    )
    
    mock_stellar_account = Mock()
    mock_stellar_account.account_id = "GABC123..."
    mock_stellar_service.create_account.return_value = mock_stellar_account
    
    # Act
    result = await account_service.create_account(account_data)
    
    # Assert
    assert result.account_id == "GABC123..."
    assert result.network == "stellar"
    assert result.account_type == "user"
    mock_stellar_service.create_account.assert_called_once_with("testnet")

@pytest.mark.asyncio
async def test_create_account_invalid_country(account_service):
    """Test account creation with invalid country code"""
    # Arrange
    account_data = AccountCreate(
        network="stellar",
        environment="testnet",
        account_type="user",
        country_code="XX"  # Invalid country
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid country code"):
        await account_service.create_account(account_data)
```

### Integration Testing

```python
# tests/integration/test_account_endpoints.py
import pytest
from httpx import AsyncClient
from api.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_headers():
    return {"Authorization": "Bearer sk_test_1234567890"}

@pytest.mark.asyncio
async def test_create_account_endpoint(client, auth_headers):
    """Test account creation endpoint"""
    account_data = {
        "network": "stellar",
        "environment": "testnet",
        "account_type": "user",
        "country_code": "NG"
    }
    
    response = await client.post(
        "/api/v1/accounts/",
        json=account_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["network"] == "stellar"
    assert data["account_type"] == "user"
    assert "account_id" in data

@pytest.mark.asyncio
async def test_list_accounts_endpoint(client, auth_headers):
    """Test account listing endpoint"""
    response = await client.get(
        "/api/v1/accounts/",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
```

### Performance Testing

```python
# tests/performance/test_api_performance.py
import asyncio
import time
import statistics
from httpx import AsyncClient

async def test_api_response_times():
    """Test API response time performance"""
    async with AsyncClient() as client:
        response_times = []
        
        # Test 100 concurrent requests
        tasks = []
        for _ in range(100):
            task = client.get("http://localhost:8000/health")
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        # Calculate response times
        for response in responses:
            response_times.append(response.elapsed.total_seconds())
        
        # Assert performance requirements
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        
        assert avg_response_time < 0.2  # 200ms average
        assert p95_response_time < 0.5  # 500ms 95th percentile
```

## ⚡ Performance Optimization

### Database Optimization

```python
# Database query optimization
async def list_accounts_optimized(
    self,
    skip: int = 0,
    limit: int = 100,
    network: Optional[str] = None,
    account_type: Optional[str] = None
) -> List[Account]:
    """Optimized account listing with proper indexing"""
    
    # Use select_related for joins
    query = select(Account).options(
        selectinload(Account.transactions),
        selectinload(Account.compliance_records)
    )
    
    # Apply filters with indexed columns
    if network:
        query = query.where(Account.network == network)
    if account_type:
        query = query.where(Account.account_type == account_type)
    
    # Use proper ordering and pagination
    query = query.order_by(Account.created_at.desc()).offset(skip).limit(limit)
    
    result = await self.db.execute(query)
    return result.scalars().all()
```

### Caching Strategy

```python
# Redis caching implementation
from redis import asyncio as aioredis
from api.core.config import settings

class CacheService:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        return await self.redis.get(key)
    
    async def set(
        self, 
        key: str, 
        value: str, 
        expire: int = 3600
    ) -> bool:
        """Set value in cache with expiration"""
        return await self.redis.set(key, value, ex=expire)
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        return await self.redis.delete(key)

# Usage in services
async def get_account_cached(self, account_id: str) -> Optional[Account]:
    """Get account with caching"""
    cache_key = f"account:{account_id}"
    
    # Try cache first
    cached_data = await self.cache_service.get(cache_key)
    if cached_data:
        return Account.parse_raw(cached_data)
    
    # Fallback to database
    account = await self.get_account(account_id)
    if account:
        # Cache for 1 hour
        await self.cache_service.set(
            cache_key,
            account.json(),
            expire=3600
        )
    
    return account
```

### Connection Pooling

```python
# Optimized database configuration
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,  # Increased pool size
    max_overflow=30,  # Allow overflow connections
    pool_pre_ping=True,  # Verify connections
    pool_recycle=3600,  # Recycle connections every hour
    echo=settings.DEBUG,
    connect_args={
        "server_settings": {
            "application_name": "rowell_infra_api",
            "jit": "off",  # Disable JIT for consistent performance
        }
    }
)
```

## 🚀 Deployment Considerations

### Production Configuration

```python
# Production settings
class ProductionSettings(Settings):
    DEBUG: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 1000
    RATE_LIMIT_BURST: int = 2000
    
    # Monitoring
    ENABLE_METRICS: bool = True
    
    class Config:
        env_file = ".env.production"
```

### Health Checks

```python
# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with dependencies"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "dependencies": {}
    }
    
    # Check database
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        health_status["dependencies"]["database"] = "healthy"
    except Exception as e:
        health_status["dependencies"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Redis
    try:
        await redis.ping()
        health_status["dependencies"]["redis"] = "healthy"
    except Exception as e:
        health_status["dependencies"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    return health_status
```

### Docker Configuration

```dockerfile
# Dockerfile for production
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬

*Rowell Infra - Alchemy for Africa*
