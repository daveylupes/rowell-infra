"""
Integration tests for API endpoints
"""

import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


class TestAPIEndpoints:
    """Integration tests for API endpoints"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, async_client: AsyncClient):
        """Test health check endpoint"""
        response = await async_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_client: AsyncClient):
        """Test root endpoint"""
        response = await async_client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["name"] == "Rowell Infra API"
    
    @pytest.mark.asyncio
    async def test_developer_registration(self, async_client: AsyncClient, test_developer_data):
        """Test developer registration endpoint"""
        response = await async_client.post(
            "/api/v1/developers/register",
            json=test_developer_data
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert data["email"] == test_developer_data["email"]
        assert data["first_name"] == test_developer_data["first_name"]
        assert data["last_name"] == test_developer_data["last_name"]
    
    @pytest.mark.asyncio
    async def test_developer_quickstart(self, async_client: AsyncClient):
        """Test developer quickstart endpoint"""
        quickstart_data = {
            "email": "quickstart@rowell-infra.com",
            "first_name": "Quickstart",
            "last_name": "User",
            "company": "Test Company",
            "role": "Developer",
            "country_code": "NG"
        }
        
        response = await async_client.post(
            "/api/v1/developers/quickstart",
            json=quickstart_data
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "developer" in data
        assert "api_key" in data
        assert "project" in data
        assert "example_code" in data
        
        # Verify developer data
        developer = data["developer"]
        assert developer["email"] == quickstart_data["email"]
        assert developer["first_name"] == quickstart_data["first_name"]
        
        # Verify API key
        api_key = data["api_key"]
        assert "api_key" in api_key
        assert api_key["api_key"].startswith("sk_")
        
        # Verify project
        project = data["project"]
        assert "id" in project
        assert "name" in project
    
    @pytest.mark.asyncio
    async def test_create_account_without_auth(self, async_client: AsyncClient, test_account_data):
        """Test account creation without authentication (should fail)"""
        response = await async_client.post(
            "/api/v1/accounts/create",
            json=test_account_data
        )
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_create_account_with_auth(self, async_client: AsyncClient, test_account_data, test_api_key):
        """Test account creation with authentication"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        # Mock the account service
        with patch('api.api.v1.endpoints.accounts.AccountService') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.create_account.return_value = {
                "id": "1",
                "account_id": "GABC1234567890",
                "secret_key": "SABC1234567890",
                "network": "stellar",
                "environment": "testnet",
                "account_type": "user",
                "country_code": "NG",
                "is_active": True,
                "is_verified": False,
                "is_compliant": False,
                "kyc_status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
                "last_activity": None,
                "metadata": {}
            }
            mock_service.return_value = mock_instance
            
            response = await async_client.post(
                "/api/v1/accounts/create",
                json=test_account_data,
                headers=headers
            )
            assert response.status_code == 201
            
            data = response.json()
            assert data["account_id"] == "GABC1234567890"
            assert data["network"] == "stellar"
            assert data["environment"] == "testnet"
            assert data["account_type"] == "user"
            assert data["country_code"] == "NG"
    
    @pytest.mark.asyncio
    async def test_list_accounts_with_auth(self, async_client: AsyncClient, test_api_key):
        """Test listing accounts with authentication"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        # Mock the account service
        with patch('api.api.v1.endpoints.accounts.AccountService') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.list_accounts.return_value = [
                {
                    "id": "1",
                    "account_id": "GABC1234567890",
                    "network": "stellar",
                    "environment": "testnet",
                    "account_type": "user",
                    "country_code": "NG",
                    "is_active": True,
                    "is_verified": False,
                    "is_compliant": False,
                    "kyc_status": "pending",
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-01T00:00:00Z",
                    "last_activity": None,
                    "metadata": {}
                }
            ]
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                "/api/v1/accounts/",
                headers=headers
            )
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 1
            assert data[0]["account_id"] == "GABC1234567890"
            assert data[0]["network"] == "stellar"
    
    @pytest.mark.asyncio
    async def test_get_account_with_auth(self, async_client: AsyncClient, test_api_key):
        """Test getting account by ID with authentication"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        # Mock the account service
        with patch('api.api.v1.endpoints.accounts.AccountService') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_account.return_value = {
                "id": "1",
                "account_id": "GABC1234567890",
                "network": "stellar",
                "environment": "testnet",
                "account_type": "user",
                "country_code": "NG",
                "is_active": True,
                "is_verified": False,
                "is_compliant": False,
                "kyc_status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
                "last_activity": None,
                "metadata": {}
            }
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                "/api/v1/accounts/GABC1234567890",
                headers=headers
            )
            assert response.status_code == 200
            
            data = response.json()
            assert data["account_id"] == "GABC1234567890"
            assert data["network"] == "stellar"
    
    @pytest.mark.asyncio
    async def test_create_transfer_with_auth(self, async_client: AsyncClient, test_transfer_data, test_api_key):
        """Test transfer creation with authentication"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        # Mock the transfer service
        with patch('api.api.v1.endpoints.transfers.TransferService') as mock_service:
            mock_instance = AsyncMock()
            mock_transaction = AsyncMock()
            mock_transaction.id = "1"
            mock_transaction.transaction_hash = "mock_stellar_tx_123456"
            mock_transaction.from_account = "GABC1234567890"
            mock_transaction.to_account = "GXYZ0987654321"
            mock_transaction.asset_code = "XLM"
            mock_transaction.amount = "10.0"
            mock_transaction.network = "stellar"
            mock_transaction.environment = "testnet"
            mock_transaction.status = "pending"
            mock_transaction.from_country = "NG"
            mock_transaction.to_country = "KE"
            mock_transaction.memo = None
            mock_transaction.compliance_status = "pending"
            mock_transaction.risk_score = 0.0
            mock_transaction.created_at = "2025-01-01T00:00:00Z"
            mock_transaction.updated_at = "2025-01-01T00:00:00Z"
            mock_transaction.ledger_time = None
            mock_transaction.transaction_metadata = {}
            
            mock_instance.create_transfer.return_value = mock_transaction
            mock_service.return_value = mock_instance
            
            response = await async_client.post(
                "/api/v1/transfers/create",
                json=test_transfer_data,
                headers=headers
            )
            assert response.status_code == 201
            
            data = response.json()
            assert data["transaction_hash"] == "mock_stellar_tx_123456"
            assert data["from_account"] == "GABC1234567890"
            assert data["to_account"] == "GXYZ0987654321"
            assert data["asset_code"] == "XLM"
            assert data["amount"] == "10.0"
    
    @pytest.mark.asyncio
    async def test_get_transfer_with_auth(self, async_client: AsyncClient, test_api_key):
        """Test getting transfer by ID with authentication"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        # Mock the transfer service
        with patch('api.api.v1.endpoints.transfers.TransferService') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_transfer.return_value = {
                "id": "1",
                "transaction_hash": "mock_stellar_tx_123456",
                "from_account": "GABC1234567890",
                "to_account": "GXYZ0987654321",
                "asset_code": "XLM",
                "amount": "10.0",
                "asset_issuer": None,
                "network": "stellar",
                "environment": "testnet",
                "status": "pending",
                "from_country": "NG",
                "to_country": "KE",
                "memo": None,
                "compliance_status": "pending",
                "risk_score": 0.0,
                "created_at": "2025-01-01T00:00:00Z",
                "updated_at": "2025-01-01T00:00:00Z",
                "ledger_time": None,
                "metadata": {}
            }
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                "/api/v1/transfers/1",
                headers=headers
            )
            assert response.status_code == 200
            
            data = response.json()
            assert data["id"] == "1"
            assert data["transaction_hash"] == "mock_stellar_tx_123456"
            assert data["from_account"] == "GABC1234567890"
            assert data["to_account"] == "GXYZ0987654321"
    
    @pytest.mark.asyncio
    async def test_list_transfers_with_auth(self, async_client: AsyncClient, test_api_key):
        """Test listing transfers with authentication"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        # Mock the transfer service
        with patch('api.api.v1.endpoints.transfers.TransferService') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.list_transfers.return_value = [
                {
                    "id": "1",
                    "transaction_hash": "mock_stellar_tx_123456",
                    "from_account": "GABC1234567890",
                    "to_account": "GXYZ0987654321",
                    "asset_code": "XLM",
                    "amount": "10.0",
                    "asset_issuer": None,
                    "network": "stellar",
                    "environment": "testnet",
                    "transaction_type": "payment",
                    "status": "pending",
                    "from_country": "NG",
                    "to_country": "KE",
                    "from_region": None,
                    "to_region": None,
                    "memo": None,
                    "amount_usd": None,
                    "fee": None,
                    "fee_usd": None,
                    "compliance_status": "pending",
                    "risk_score": 0.0,
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-01T00:00:00Z",
                    "ledger_time": None,
                    "transaction_metadata": {}
                }
            ]
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                "/api/v1/transfers/",
                headers=headers
            )
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) == 1
            assert data[0]["transaction_hash"] == "mock_stellar_tx_123456"
            assert data[0]["from_account"] == "GABC1234567890"
    
    @pytest.mark.asyncio
    async def test_analytics_dashboard_with_auth(self, async_client: AsyncClient, test_api_key):
        """Test analytics dashboard with authentication"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        # Mock the analytics service
        with patch('api.api.v1.endpoints.analytics.AnalyticsService') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_dashboard_data.return_value = {
                "total_accounts": 100,
                "total_transactions": 500,
                "total_volume": "10000.00",
                "success_rate": 99.5,
                "active_networks": ["stellar", "hedera"],
                "recent_activity": [
                    {
                        "type": "account_created",
                        "timestamp": "2025-01-01T00:00:00Z",
                        "details": "New account created"
                    }
                ]
            }
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                "/api/v1/analytics/dashboard",
                headers=headers
            )
            assert response.status_code == 200
            
            data = response.json()
            assert data["total_accounts"] == 100
            assert data["total_transactions"] == 500
            assert data["total_volume"] == "10000.00"
            assert data["success_rate"] == 99.5
            assert "stellar" in data["active_networks"]
    
    @pytest.mark.asyncio
    async def test_invalid_endpoint(self, async_client: AsyncClient):
        """Test invalid endpoint returns 404"""
        response = await async_client.get("/api/v1/invalid-endpoint")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_invalid_json_payload(self, async_client: AsyncClient, test_api_key):
        """Test invalid JSON payload returns 422"""
        headers = {"Authorization": f"Bearer {test_api_key}"}
        
        response = await async_client.post(
            "/api/v1/accounts/create",
            json={"invalid": "data"},
            headers=headers
        )
        assert response.status_code == 422
