"""
Pytest configuration and fixtures for Rowell Infra tests
"""

import pytest
import asyncio
import sys
import os
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Add the api directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

try:
    from api.main import app
    from api.core.database import get_db, Base
    from api.core.config import settings
except ImportError:
    # Fallback for when running tests without the full API setup
    app = None
    get_db = None
    Base = None
    settings = None


# Test database URL (using SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    if Base is None:
        pytest.skip("API modules not available")
    
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=True,
        future=True
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session"""
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def override_get_db(db_session: AsyncSession):
    """Override the database dependency"""
    if app is None or get_db is None:
        pytest.skip("API modules not available")
    
    async def _override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(override_get_db):
    """Create an async HTTP client for testing"""
    if app is None:
        pytest.skip("API modules not available")
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def sync_client(override_get_db) -> TestClient:
    """Create a sync HTTP client for testing"""
    if app is None:
        pytest.skip("API modules not available")
    
    return TestClient(app)


@pytest.fixture
def test_api_key() -> str:
    """Test API key for authenticated requests"""
    return "sk_test_1234567890abcdef"


@pytest.fixture
def test_developer_data() -> dict:
    """Test developer data"""
    return {
        "email": "test@rowell-infra.com",
        "first_name": "Test",
        "last_name": "Developer",
        "company": "Test Company",
        "role": "Developer",
        "country_code": "NG",
        "phone": "+2341234567890"
    }


@pytest.fixture
def test_account_data() -> dict:
    """Test account creation data"""
    return {
        "network": "stellar",
        "environment": "testnet",
        "account_type": "user",
        "country_code": "NG"
    }


@pytest.fixture
def test_transfer_data() -> dict:
    """Test transfer data"""
    return {
        "from_account": "GABC1234567890",
        "to_account": "GXYZ0987654321",
        "asset_code": "XLM",
        "amount": "10.0",
        "network": "stellar",
        "environment": "testnet",
        "from_country": "NG",
        "to_country": "KE"
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
