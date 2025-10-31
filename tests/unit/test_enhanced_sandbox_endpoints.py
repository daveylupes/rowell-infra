"""
Unit tests for enhanced sandbox endpoints
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from fastapi import status

from api.main import create_application


class TestEnhancedSandboxEndpoints:
    """Test cases for enhanced sandbox API endpoints"""
    
    @pytest.fixture
    def app(self):
        """FastAPI application instance"""
        return create_application()
    
    @pytest.fixture
    def client(self, app):
        """Test client"""
        return TestClient(app)
    
    def test_initialize_sandbox_environment_success(self, client):
        """Test successful sandbox environment initialization"""
        response = client.post(
            "/api/v1/sandbox/initialize?environment=sandbox",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        init_data = data["data"]
        assert init_data["environment"] == "sandbox"
        assert init_data["status"] == "initialized"
        assert "mock_data" in init_data
        assert "test_scenarios" in init_data
        assert "analytics_initialized" in init_data
        assert "initialized_at" in init_data
        assert "config" in init_data
    
    def test_initialize_sandbox_environment_testnet(self, client):
        """Test sandbox environment initialization with testnet"""
        response = client.post(
            "/api/v1/sandbox/initialize?environment=testnet",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["environment"] == "testnet"
    
    def test_initialize_sandbox_environment_mock(self, client):
        """Test sandbox environment initialization with mock"""
        response = client.post(
            "/api/v1/sandbox/initialize?environment=mock",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["environment"] == "mock"
    
    def test_initialize_sandbox_environment_invalid(self, client):
        """Test sandbox environment initialization with invalid environment"""
        response = client.post(
            "/api/v1/sandbox/initialize?environment=invalid",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "Invalid environment" in data["detail"]
    
    def test_initialize_sandbox_environment_unauthorized(self, client):
        """Test sandbox environment initialization without API key"""
        response = client.post("/api/v1/sandbox/initialize")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_test_scenario_success(self, client):
        """Test getting specific test scenario"""
        response = client.get(
            "/api/v1/sandbox/scenarios/basic_integration",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        scenario = data["data"]
        assert scenario["id"] == "basic_integration"
        assert scenario["name"] == "Basic Integration Test"
        assert "description" in scenario
        assert "estimated_duration" in scenario
        assert "steps" in scenario
        assert "required_data" in scenario
        assert "expected_outcomes" in scenario
    
    def test_get_test_scenario_not_found(self, client):
        """Test getting non-existent test scenario"""
        response = client.get(
            "/api/v1/sandbox/scenarios/nonexistent_scenario",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "not found" in data["detail"]
    
    def test_get_test_scenario_unauthorized(self, client):
        """Test getting test scenario without API key"""
        response = client.get("/api/v1/sandbox/scenarios/basic_integration")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_execute_test_scenario_success(self, client):
        """Test successful test scenario execution"""
        response = client.post(
            "/api/v1/sandbox/scenarios/basic_integration/execute",
            headers={"X-API-Key": "test-api-key"},
            json={}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        execution_data = data["data"]
        assert execution_data["scenario_id"] == "basic_integration"
        assert execution_data["status"] == "completed"
        assert execution_data["steps_completed"] > 0
        assert execution_data["expected_outcomes_met"] is True
        assert "execution_log" in execution_data
        assert "started_at" in execution_data
        assert "completed_at" in execution_data
    
    def test_execute_test_scenario_with_params(self, client):
        """Test test scenario execution with parameters"""
        params = {"test_param": "test_value"}
        response = client.post(
            "/api/v1/sandbox/scenarios/compliance_testing/execute",
            headers={"X-API-Key": "test-api-key"},
            json=params
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["scenario_id"] == "compliance_testing"
    
    def test_execute_test_scenario_not_found(self, client):
        """Test executing non-existent test scenario"""
        response = client.post(
            "/api/v1/sandbox/scenarios/nonexistent_scenario/execute",
            headers={"X-API-Key": "test-api-key"},
            json={}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "not found" in data["detail"]
    
    def test_execute_test_scenario_unauthorized(self, client):
        """Test executing test scenario without API key"""
        response = client.post(
            "/api/v1/sandbox/scenarios/basic_integration/execute",
            json={}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_sandbox_usage_analytics_success(self, client):
        """Test getting sandbox usage analytics"""
        response = client.get(
            "/api/v1/sandbox/analytics",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        analytics_data = data["data"]
        assert "usage_stats" in analytics_data
        assert "environment_config" in analytics_data
        assert "rate_limits" in analytics_data
        assert "current_status" in analytics_data
        assert "generated_at" in analytics_data
        
        # Check usage stats structure
        usage_stats = analytics_data["usage_stats"]
        assert "initialized_at" in usage_stats
        assert "total_requests" in usage_stats
        assert "mock_data_generated" in usage_stats
        assert "test_scenarios_run" in usage_stats
        assert "last_reset" in usage_stats
        
        # Check environment config structure
        env_config = analytics_data["environment_config"]
        assert "default_account_count" in env_config
        assert "default_transaction_count" in env_config
        assert "default_compliance_count" in env_config
        assert "countries" in env_config
        assert "networks" in env_config
    
    def test_get_sandbox_usage_analytics_unauthorized(self, client):
        """Test getting sandbox analytics without API key"""
        response = client.get("/api/v1/sandbox/analytics")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_sandbox_config_success(self, client):
        """Test successful sandbox configuration update"""
        config_updates = {
            "default_account_count": 200,
            "default_transaction_count": 1000
        }
        
        response = client.patch(
            "/api/v1/sandbox/config",
            headers={"X-API-Key": "test-api-key"},
            json=config_updates
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        update_data = data["data"]
        assert "updated_config" in update_data
        assert "updated_at" in update_data
        assert update_data["updated_config"]["default_account_count"] == 200
        assert update_data["updated_config"]["default_transaction_count"] == 1000
    
    def test_update_sandbox_config_invalid_data(self, client):
        """Test sandbox configuration update with invalid data"""
        config_updates = {
            "invalid_key": "invalid_value"
        }
        
        response = client.patch(
            "/api/v1/sandbox/config",
            headers={"X-API-Key": "test-api-key"},
            json=config_updates
        )
        
        # Should still succeed but not update invalid keys
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
    
    def test_update_sandbox_config_unauthorized(self, client):
        """Test updating sandbox config without API key"""
        response = client.patch(
            "/api/v1/sandbox/config",
            json={"default_account_count": 200}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_sandbox_health_success(self, client):
        """Test getting sandbox health status"""
        response = client.get(
            "/api/v1/sandbox/health",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        health_data = data["data"]
        assert "status" in health_data
        assert "timestamp" in health_data
        assert "components" in health_data
        assert "stats" in health_data
        assert "analytics" in health_data
        
        # Check components structure
        components = health_data["components"]
        assert "sandbox_service" in components
        assert "analytics_service" in components
        assert "mock_data_generation" in components
        assert "test_scenarios" in components
        
        # Check that all components have health status
        for component, status in components.items():
            assert status in ["healthy", "unhealthy"]
    
    def test_get_sandbox_health_unauthorized(self, client):
        """Test getting sandbox health without API key"""
        response = client.get("/api/v1/sandbox/health")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_all_enhanced_endpoints_require_auth(self, client):
        """Test that all enhanced endpoints require authentication"""
        endpoints = [
            ("POST", "/api/v1/sandbox/initialize"),
            ("GET", "/api/v1/sandbox/scenarios/basic_integration"),
            ("POST", "/api/v1/sandbox/scenarios/basic_integration/execute"),
            ("GET", "/api/v1/sandbox/analytics"),
            ("PATCH", "/api/v1/sandbox/config"),
            ("GET", "/api/v1/sandbox/health")
        ]
        
        for method, endpoint in endpoints:
            if method == "POST":
                response = client.post(endpoint, json={})
            elif method == "GET":
                response = client.get(endpoint)
            elif method == "PATCH":
                response = client.patch(endpoint, json={})
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_initialize_environment_data_structure(self, client):
        """Test that initialization returns proper data structure"""
        response = client.post(
            "/api/v1/sandbox/initialize?environment=sandbox",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check mock data structure
        mock_data = data["data"]["mock_data"]
        assert "accounts" in mock_data
        assert "transactions" in mock_data
        assert "compliance_records" in mock_data
        assert "analytics_records" in mock_data
        
        # Check config structure
        config = data["data"]["config"]
        assert "default_account_count" in config
        assert "default_transaction_count" in config
        assert "countries" in config
        assert "networks" in config
        assert "rate_limits" in config
    
    def test_scenario_execution_data_structure(self, client):
        """Test that scenario execution returns proper data structure"""
        response = client.post(
            "/api/v1/sandbox/scenarios/analytics_testing/execute",
            headers={"X-API-Key": "test-api-key"},
            json={}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        execution_data = data["data"]
        assert execution_data["scenario_id"] == "analytics_testing"
        assert execution_data["status"] == "completed"
        assert execution_data["steps_completed"] > 0
        assert execution_data["expected_outcomes_met"] is True
        
        # Check execution log structure
        execution_log = execution_data["execution_log"]
        assert len(execution_log) == execution_data["steps_completed"]
        
        # Check log format
        for log_entry in execution_log:
            assert log_entry.startswith("Step ")
            assert " - Completed" in log_entry
    
    def test_analytics_data_structure(self, client):
        """Test that analytics endpoint returns proper data structure"""
        response = client.get(
            "/api/v1/sandbox/analytics",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        analytics_data = data["data"]
        
        # Check usage stats structure
        usage_stats = analytics_data["usage_stats"]
        assert "initialized_at" in usage_stats
        assert "total_requests" in usage_stats
        assert "mock_data_generated" in usage_stats
        assert "test_scenarios_run" in usage_stats
        assert "last_reset" in usage_stats
        
        # Check environment config structure
        env_config = analytics_data["environment_config"]
        assert "default_account_count" in env_config
        assert "default_transaction_count" in env_config
        assert "default_compliance_count" in env_config
        assert "countries" in env_config
        assert "account_types" in env_config
        assert "transaction_types" in env_config
        assert "networks" in env_config
        assert "environments" in env_config
        
        # Check rate limits structure
        rate_limits = analytics_data["rate_limits"]
        assert "requests_per_minute" in rate_limits
        assert "requests_per_hour" in rate_limits
        assert "requests_per_day" in rate_limits
    
    def test_health_status_components(self, client):
        """Test that health endpoint returns proper component status"""
        response = client.get(
            "/api/v1/sandbox/health",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        health_data = data["data"]
        components = health_data["components"]
        
        # Check all required components are present
        required_components = [
            "sandbox_service",
            "analytics_service", 
            "mock_data_generation",
            "test_scenarios"
        ]
        
        for component in required_components:
            assert component in components
            assert components[component] in ["healthy", "unhealthy"]
    
    def test_config_update_persistence(self, client):
        """Test that configuration updates persist across requests"""
        # Update config
        config_updates = {"default_account_count": 300}
        response = client.patch(
            "/api/v1/sandbox/config",
            headers={"X-API-Key": "test-api-key"},
            json=config_updates
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["updated_config"]["default_account_count"] == 300
        
        # Check that update persisted by getting analytics
        response = client.get(
            "/api/v1/sandbox/analytics",
            headers={"X-API-Key": "test-api-key"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        analytics_data = response.json()["data"]
        assert analytics_data["environment_config"]["default_account_count"] == 300
