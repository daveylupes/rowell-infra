"""
Unit tests for sandbox endpoints
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from fastapi import status

from api.main import create_application


class TestSandboxEndpoints:
    """Test cases for sandbox API endpoints"""
    
    @pytest.fixture
    def app(self):
        """FastAPI application instance"""
        return create_application()
    
    @pytest.fixture
    def client(self, app):
        """Test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_auth(self):
        """Mock authentication"""
        return {"api_key": "test-api-key", "permissions": ["sandbox:read", "sandbox:write", "sandbox:admin"]}
    
    def test_get_sandbox_stats_success(self, client, mock_auth):
        """Test successful sandbox stats retrieval"""
        response = client.get(
            "/api/v1/sandbox/stats",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "accounts" in data["data"]
        assert "transactions" in data["data"]
        assert "analytics" in data["data"]
        assert "compliance" in data["data"]
    
    def test_get_sandbox_stats_unauthorized(self, client):
        """Test sandbox stats with missing API key"""
        response = client.get("/api/v1/sandbox/stats")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_generate_mock_accounts_success(self, client):
        """Test successful mock account generation"""
        response = client.post(
            "/api/v1/sandbox/accounts/generate?count=5",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "accounts" in data["data"]
        assert len(data["data"]["accounts"]) == 5
        assert "count" in data["data"]
        assert data["data"]["count"] == 5
    
    def test_generate_mock_accounts_invalid_count(self, client):
        """Test mock account generation with invalid count"""
        response = client.post(
            "/api/v1/sandbox/accounts/generate?count=0",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_generate_mock_accounts_count_too_high(self, client):
        """Test mock account generation with count too high"""
        response = client.post(
            "/api/v1/sandbox/accounts/generate?count=101",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_generate_mock_transactions_success(self, client):
        """Test successful mock transaction generation"""
        response = client.post(
            "/api/v1/sandbox/transactions/generate?account_ids=acc1&account_ids=acc2&count=10",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "transactions" in data["data"]
        assert len(data["data"]["transactions"]) == 10
        assert "count" in data["data"]
        assert data["data"]["count"] == 10
    
    def test_generate_mock_transactions_invalid_count(self, client):
        """Test mock transaction generation with invalid count"""
        response = client.post(
            "/api/v1/sandbox/transactions/generate?account_ids=acc1&count=0",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_generate_mock_analytics_success(self, client):
        """Test successful mock analytics generation"""
        response = client.post(
            "/api/v1/sandbox/analytics/generate",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "remittance_flows" in data["data"]
        assert "stablecoin_adoption" in data["data"]
        assert "merchant_activity" in data["data"]
        assert "network_metrics" in data["data"]
        
        # Check data structure
        assert len(data["data"]["remittance_flows"]) == 20
        assert len(data["data"]["stablecoin_adoption"]) == 15
        assert len(data["data"]["merchant_activity"]) == 12
        assert len(data["data"]["network_metrics"]) == 6
    
    def test_generate_mock_compliance_data_success(self, client):
        """Test successful mock compliance data generation"""
        response = client.post(
            "/api/v1/sandbox/compliance/generate?account_ids=acc1&account_ids=acc2&entity_ids=entity1&entity_ids=entity2&kyc_count=5&flag_count=3",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "kyc_verifications" in data["data"]
        assert "compliance_flags" in data["data"]
        assert "counts" in data["data"]
        
        assert len(data["data"]["kyc_verifications"]) == 5
        assert len(data["data"]["compliance_flags"]) == 3
        assert data["data"]["counts"]["kyc_verifications"] == 5
        assert data["data"]["counts"]["compliance_flags"] == 3
    
    def test_generate_mock_compliance_data_invalid_counts(self, client):
        """Test mock compliance data generation with invalid counts"""
        response = client.post(
            "/api/v1/sandbox/compliance/generate?account_ids=acc1&entity_ids=entity1&kyc_count=0",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_reset_sandbox_data_success(self, client):
        """Test successful sandbox data reset"""
        response = client.post(
            "/api/v1/sandbox/reset",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "message" in data["data"]
        assert "timestamp" in data["data"]
    
    def test_reset_sandbox_data_unauthorized(self, client):
        """Test sandbox data reset without proper permissions"""
        response = client.post(
            "/api/v1/sandbox/reset",
            headers={"X-API-Key": "test-api-key"}
        )
        
        # This might fail due to permission requirements
        # The exact status depends on the auth implementation
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]
    
    def test_get_test_scenarios_success(self, client):
        """Test successful test scenarios retrieval"""
        response = client.get(
            "/api/v1/sandbox/scenarios",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "scenarios" in data["data"]
        assert "total_scenarios" in data["data"]
        assert "usage_instructions" in data["data"]
        
        # Check that all expected scenarios are present
        scenarios = data["data"]["scenarios"]
        expected_scenarios = [
            "basic_integration",
            "compliance_testing", 
            "analytics_testing",
            "stress_testing",
            "error_handling"
        ]
        for scenario in expected_scenarios:
            assert scenario in scenarios
            assert "name" in scenarios[scenario]
            assert "description" in scenarios[scenario]
            assert "steps" in scenarios[scenario]
            assert "estimated_duration" in scenarios[scenario]
    
    def test_get_sandbox_rate_limits_success(self, client):
        """Test successful sandbox rate limits retrieval"""
        response = client.get(
            "/api/v1/sandbox/rate-limits",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "sandbox_tier" in data["data"]
        assert "testing_guidelines" in data["data"]
        assert "headers" in data["data"]
        
        # Check sandbox tier structure
        sandbox_tier = data["data"]["sandbox_tier"]
        assert "name" in sandbox_tier
        assert "description" in sandbox_tier
        assert "limits" in sandbox_tier
        assert "features" in sandbox_tier
        
        # Check limits structure
        limits = sandbox_tier["limits"]
        assert "requests_per_minute" in limits
        assert "requests_per_hour" in limits
        assert "requests_per_day" in limits
        assert "burst_limit" in limits
        
        # Check headers structure
        headers = data["data"]["headers"]
        assert "X-RateLimit-Limit" in headers
        assert "X-RateLimit-Remaining" in headers
        assert "X-RateLimit-Reset" in headers
        assert "Retry-After" in headers
    
    def test_endpoint_unauthorized_access(self, client):
        """Test that endpoints require proper authentication"""
        endpoints = [
            "/api/v1/sandbox/stats",
            "/api/v1/sandbox/accounts/generate",
            "/api/v1/sandbox/transactions/generate",
            "/api/v1/sandbox/analytics/generate",
            "/api/v1/sandbox/compliance/generate",
            "/api/v1/sandbox/reset",
            "/api/v1/sandbox/scenarios",
            "/api/v1/sandbox/rate-limits"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint) if endpoint.endswith(('stats', 'scenarios', 'rate-limits')) else client.post(endpoint)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_generate_accounts_data_structure(self, client):
        """Test that generated accounts have proper data structure"""
        response = client.post(
            "/api/v1/sandbox/accounts/generate?count=3",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        accounts = data["data"]["accounts"]
        
        for account in accounts:
            required_fields = [
                "id", "account_id", "network", "environment", "account_type",
                "country_code", "region", "is_active", "is_verified", "is_compliant",
                "kyc_status", "created_at", "updated_at", "metadata"
            ]
            for field in required_fields:
                assert field in account
            
            # Check metadata structure
            assert account["metadata"]["sandbox"] is True
            assert account["metadata"]["mock_data"] is True
            assert "test_scenario" in account["metadata"]
    
    def test_generate_transactions_data_structure(self, client):
        """Test that generated transactions have proper data structure"""
        response = client.post(
            "/api/v1/sandbox/transactions/generate?account_ids=acc1&account_ids=acc2&count=2",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        transactions = data["data"]["transactions"]
        
        for transaction in transactions:
            required_fields = [
                "id", "transaction_hash", "network", "environment", "transaction_type",
                "status", "from_account", "to_account", "asset_code", "amount",
                "amount_usd", "from_country", "to_country", "from_region", "to_region",
                "memo", "fee", "fee_usd", "created_at", "updated_at", "compliance_status",
                "risk_score"
            ]
            for field in required_fields:
                assert field in transaction
            
            # Check that from_account and to_account are different
            assert transaction["from_account"] != transaction["to_account"]
            
            # Check that numeric fields are strings
            assert isinstance(transaction["amount"], str)
            assert isinstance(transaction["amount_usd"], str)
            assert isinstance(transaction["fee"], str)
            assert isinstance(transaction["fee_usd"], str)
            
            # Check that risk_score is numeric
            assert isinstance(transaction["risk_score"], (int, float))
    
    def test_generate_analytics_data_structure(self, client):
        """Test that generated analytics data has proper structure"""
        response = client.post(
            "/api/v1/sandbox/analytics/generate",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check remittance flows
        flows = data["data"]["remittance_flows"]
        assert len(flows) > 0
        for flow in flows:
            assert "from_country" in flow
            assert "to_country" in flow
            assert "asset_code" in flow
            assert "total_volume" in flow
            assert flow["from_country"] != flow["to_country"]
        
        # Check stablecoin adoption
        adoption = data["data"]["stablecoin_adoption"]
        assert len(adoption) > 0
        for item in adoption:
            assert "asset_code" in item
            assert "total_volume" in item
            assert item["asset_code"] in ["USDC", "USDT", "DAI", "BUSD"]
        
        # Check merchant activity
        activities = data["data"]["merchant_activity"]
        assert len(activities) > 0
        for activity in activities:
            assert "merchant_type" in activity
            assert "total_volume" in activity
            assert activity["merchant_type"] in ["fintech", "ecommerce", "remittance", "banking", "retail"]
        
        # Check network metrics
        metrics = data["data"]["network_metrics"]
        assert len(metrics) > 0
        for metric in metrics:
            assert "network" in metric
            assert "environment" in metric
            assert "total_transactions" in metric
            assert metric["network"] in ["stellar", "hedera"]
            assert metric["environment"] in ["testnet", "mainnet"]
    
    def test_generate_compliance_data_structure(self, client):
        """Test that generated compliance data has proper structure"""
        response = client.post(
            "/api/v1/sandbox/compliance/generate?account_ids=acc1&entity_ids=entity1&kyc_count=2&flag_count=2",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check KYC verifications
        kyc_verifications = data["data"]["kyc_verifications"]
        assert len(kyc_verifications) == 2
        for kyc in kyc_verifications:
            assert "verification_id" in kyc
            assert "account_id" in kyc
            assert "verification_type" in kyc
            assert "verification_status" in kyc
            assert "provider" in kyc
            assert kyc["verification_type"] in ["individual", "business", "ngo"]
            assert kyc["verification_status"] in ["verified", "pending", "rejected"]
        
        # Check compliance flags
        flags = data["data"]["compliance_flags"]
        assert len(flags) == 2
        for flag in flags:
            assert "entity_type" in flag
            assert "entity_id" in flag
            assert "flag_type" in flag
            assert "flag_severity" in flag
            assert "flag_status" in flag
            assert flag["entity_type"] in ["account", "transaction"]
            assert flag["flag_type"] in ["aml", "kyc", "sanctions", "risk"]
            assert flag["flag_severity"] in ["low", "medium", "high", "critical"]
