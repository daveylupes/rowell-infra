"""
Unit tests for enhanced SandboxService functionality
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta
import uuid

from api.services.sandbox_service import SandboxService, SandboxEnvironment


class TestEnhancedSandboxService:
    """Test cases for enhanced SandboxService functionality"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        return AsyncMock()
    
    @pytest.fixture
    def sandbox_service(self, mock_db_session):
        """SandboxService instance with mocked database"""
        return SandboxService(mock_db_session)
    
    @pytest.mark.asyncio
    async def test_initialize_sandbox_environment_success(self, sandbox_service):
        """Test successful sandbox environment initialization"""
        result = await sandbox_service.initialize_sandbox_environment(SandboxEnvironment.SANDBOX)
        
        assert result["environment"] == "sandbox"
        assert result["status"] == "initialized"
        assert "mock_data" in result
        assert "test_scenarios" in result
        assert "analytics_initialized" in result
        assert "initialized_at" in result
        assert "config" in result
        
        # Check mock data structure
        mock_data = result["mock_data"]
        assert "accounts" in mock_data
        assert "transactions" in mock_data
        assert "compliance_records" in mock_data
        assert "analytics_records" in mock_data
        
        # Check that usage stats were updated
        assert sandbox_service.usage_stats["initialized_at"] is not None
        assert sandbox_service.usage_stats["total_requests"] == 0
        assert sandbox_service.usage_stats["mock_data_generated"] > 0
    
    @pytest.mark.asyncio
    async def test_initialize_sandbox_environment_testnet(self, sandbox_service):
        """Test sandbox environment initialization with testnet"""
        result = await sandbox_service.initialize_sandbox_environment(SandboxEnvironment.TESTNET)
        
        assert result["environment"] == "testnet"
        assert result["status"] == "initialized"
    
    @pytest.mark.asyncio
    async def test_initialize_sandbox_environment_mock(self, sandbox_service):
        """Test sandbox environment initialization with mock"""
        result = await sandbox_service.initialize_sandbox_environment(SandboxEnvironment.MOCK)
        
        assert result["environment"] == "mock"
        assert result["status"] == "initialized"
    
    @pytest.mark.asyncio
    async def test_load_sandbox_config(self, sandbox_service):
        """Test sandbox configuration loading"""
        config = sandbox_service._load_sandbox_config()
        
        assert "default_account_count" in config
        assert "default_transaction_count" in config
        assert "default_compliance_count" in config
        assert "countries" in config
        assert "account_types" in config
        assert "transaction_types" in config
        assert "networks" in config
        assert "environments" in config
        assert "rate_limits" in config
        
        # Check default values
        assert config["default_account_count"] == 100
        assert config["default_transaction_count"] == 500
        assert config["default_compliance_count"] == 50
        assert "NG" in config["countries"]
        assert "stellar" in config["networks"]
        assert "testnet" in config["environments"]
        
        # Check rate limits
        rate_limits = config["rate_limits"]
        assert "requests_per_minute" in rate_limits
        assert "requests_per_hour" in rate_limits
        assert "requests_per_day" in rate_limits
    
    @pytest.mark.asyncio
    async def test_generate_comprehensive_mock_data(self, sandbox_service):
        """Test comprehensive mock data generation"""
        mock_data = await sandbox_service._generate_comprehensive_mock_data()
        
        assert "accounts_count" in mock_data
        assert "transactions_count" in mock_data
        assert "compliance_count" in mock_data
        assert "analytics_count" in mock_data
        assert "accounts" in mock_data
        assert "transactions" in mock_data
        assert "kyc_verifications" in mock_data
        assert "compliance_flags" in mock_data
        assert "analytics_data" in mock_data
        
        # Check counts match actual data
        assert mock_data["accounts_count"] == len(mock_data["accounts"])
        assert mock_data["transactions_count"] == len(mock_data["transactions"])
        assert mock_data["compliance_count"] == len(mock_data["kyc_verifications"]) + len(mock_data["compliance_flags"])
        
        # Check analytics data structure
        analytics_data = mock_data["analytics_data"]
        assert "remittance_flows" in analytics_data
        assert "stablecoin_adoption" in analytics_data
        assert "merchant_activity" in analytics_data
        assert "network_metrics" in analytics_data
    
    @pytest.mark.asyncio
    async def test_clear_sandbox_data(self, sandbox_service):
        """Test sandbox data clearing"""
        result = await sandbox_service._clear_sandbox_data()
        
        assert result["success"] is True
        assert "message" in result
        assert "timestamp" in result
        assert "cleared successfully" in result["message"]
    
    @pytest.mark.asyncio
    async def test_create_test_scenarios(self, sandbox_service):
        """Test test scenario creation"""
        scenarios = await sandbox_service._create_test_scenarios()
        
        assert len(scenarios) == 5
        
        # Check scenario structure
        for scenario in scenarios:
            assert "id" in scenario
            assert "name" in scenario
            assert "description" in scenario
            assert "estimated_duration" in scenario
            assert "steps" in scenario
            assert "required_data" in scenario
            assert "expected_outcomes" in scenario
        
        # Check specific scenarios
        scenario_ids = [s["id"] for s in scenarios]
        expected_scenarios = [
            "basic_integration",
            "compliance_testing",
            "analytics_testing",
            "stress_testing",
            "error_handling"
        ]
        for expected_id in expected_scenarios:
            assert expected_id in scenario_ids
    
    @pytest.mark.asyncio
    async def test_initialize_sandbox_analytics(self, sandbox_service):
        """Test sandbox analytics initialization"""
        result = await sandbox_service._initialize_sandbox_analytics()
        
        assert result["status"] == "initialized"
        assert "config" in result
        assert "initialized_at" in result
        
        # Check analytics config
        config = result["config"]
        assert "tracking_enabled" in config
        assert "metrics_collected" in config
        assert "retention_period" in config
        assert "real_time_monitoring" in config
        
        assert config["tracking_enabled"] is True
        assert config["real_time_monitoring"] is True
        assert config["retention_period"] == 30
        
        # Check metrics collected
        metrics = config["metrics_collected"]
        expected_metrics = [
            "api_requests",
            "mock_data_generation",
            "test_scenario_execution",
            "error_rates",
            "performance_metrics"
        ]
        for metric in expected_metrics:
            assert metric in metrics
    
    @pytest.mark.asyncio
    async def test_get_test_scenario_success(self, sandbox_service):
        """Test getting specific test scenario"""
        result = await sandbox_service.get_test_scenario("basic_integration")
        
        assert result["success"] is True
        assert "data" in result
        
        scenario = result["data"]
        assert scenario["id"] == "basic_integration"
        assert scenario["name"] == "Basic Integration Test"
        assert "steps" in scenario
        assert len(scenario["steps"]) > 0
    
    @pytest.mark.asyncio
    async def test_get_test_scenario_not_found(self, sandbox_service):
        """Test getting non-existent test scenario"""
        result = await sandbox_service.get_test_scenario("nonexistent_scenario")
        
        assert result["success"] is False
        assert "message" in result
        assert "not found" in result["message"]
    
    @pytest.mark.asyncio
    async def test_execute_test_scenario_success(self, sandbox_service):
        """Test successful test scenario execution"""
        result = await sandbox_service.execute_test_scenario("basic_integration")
        
        assert result["success"] is True
        assert "data" in result
        
        execution_data = result["data"]
        assert execution_data["scenario_id"] == "basic_integration"
        assert execution_data["status"] == "completed"
        assert execution_data["steps_completed"] > 0
        assert execution_data["expected_outcomes_met"] is True
        assert "execution_log" in execution_data
        assert "started_at" in execution_data
        assert "completed_at" in execution_data
        
        # Check that usage stats were updated
        assert sandbox_service.usage_stats["test_scenarios_run"] == 1
        assert sandbox_service.usage_stats["total_requests"] == 1
    
    @pytest.mark.asyncio
    async def test_execute_test_scenario_with_params(self, sandbox_service):
        """Test test scenario execution with parameters"""
        params = {"test_param": "test_value"}
        result = await sandbox_service.execute_test_scenario("basic_integration", params)
        
        assert result["success"] is True
        assert "data" in result
        
        execution_data = result["data"]
        assert execution_data["scenario_id"] == "basic_integration"
        assert execution_data["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_execute_test_scenario_not_found(self, sandbox_service):
        """Test executing non-existent test scenario"""
        result = await sandbox_service.execute_test_scenario("nonexistent_scenario")
        
        assert result["success"] is False
        assert "message" in result
        assert "not found" in result["message"]
    
    @pytest.mark.asyncio
    async def test_get_sandbox_usage_analytics(self, sandbox_service):
        """Test getting sandbox usage analytics"""
        # Initialize sandbox first
        await sandbox_service.initialize_sandbox_environment()
        
        result = await sandbox_service.get_sandbox_usage_analytics()
        
        assert result["success"] is True
        assert "data" in result
        
        analytics_data = result["data"]
        assert "usage_stats" in analytics_data
        assert "environment_config" in analytics_data
        assert "rate_limits" in analytics_data
        assert "current_status" in analytics_data
        assert "generated_at" in analytics_data
        
        # Check usage stats
        usage_stats = analytics_data["usage_stats"]
        assert "initialized_at" in usage_stats
        assert "total_requests" in usage_stats
        assert "mock_data_generated" in usage_stats
        assert "test_scenarios_run" in usage_stats
        assert "last_reset" in usage_stats
        
        # Check current status
        assert analytics_data["current_status"] == "active"
    
    @pytest.mark.asyncio
    async def test_update_sandbox_config_success(self, sandbox_service):
        """Test successful sandbox configuration update"""
        config_updates = {
            "default_account_count": 200,
            "default_transaction_count": 1000
        }
        
        result = await sandbox_service.update_sandbox_config(config_updates)
        
        assert result["success"] is True
        assert "message" in result
        assert "data" in result
        
        # Check that config was updated
        assert sandbox_service.sandbox_config["default_account_count"] == 200
        assert sandbox_service.sandbox_config["default_transaction_count"] == 1000
        
        # Check response data
        data = result["data"]
        assert "updated_config" in data
        assert "updated_at" in data
        assert data["updated_config"]["default_account_count"] == 200
    
    @pytest.mark.asyncio
    async def test_update_sandbox_config_invalid_key(self, sandbox_service):
        """Test sandbox configuration update with invalid key"""
        config_updates = {
            "invalid_key": "invalid_value"
        }
        
        result = await sandbox_service.update_sandbox_config(config_updates)
        
        # Should succeed but not update anything
        assert result["success"] is True
        assert "invalid_key" not in sandbox_service.sandbox_config
    
    @pytest.mark.asyncio
    async def test_usage_stats_tracking(self, sandbox_service):
        """Test that usage stats are properly tracked"""
        # Initialize sandbox
        await sandbox_service.initialize_sandbox_environment()
        
        # Execute a test scenario
        await sandbox_service.execute_test_scenario("basic_integration")
        
        # Check usage stats
        assert sandbox_service.usage_stats["initialized_at"] is not None
        assert sandbox_service.usage_stats["total_requests"] == 1
        assert sandbox_service.usage_stats["mock_data_generated"] > 0
        assert sandbox_service.usage_stats["test_scenarios_run"] == 1
    
    @pytest.mark.asyncio
    async def test_sandbox_environment_enum(self):
        """Test SandboxEnvironment enum values"""
        assert SandboxEnvironment.TESTNET.value == "testnet"
        assert SandboxEnvironment.SANDBOX.value == "sandbox"
        assert SandboxEnvironment.MOCK.value == "mock"
        
        # Test enum creation
        assert SandboxEnvironment("testnet") == SandboxEnvironment.TESTNET
        assert SandboxEnvironment("sandbox") == SandboxEnvironment.SANDBOX
        assert SandboxEnvironment("mock") == SandboxEnvironment.MOCK
    
    @pytest.mark.asyncio
    async def test_comprehensive_mock_data_integration(self, sandbox_service):
        """Test comprehensive mock data generation integration"""
        mock_data = await sandbox_service._generate_comprehensive_mock_data()
        
        # Verify all components are generated
        assert mock_data["accounts_count"] == sandbox_service.sandbox_config["default_account_count"]
        assert mock_data["transactions_count"] == sandbox_service.sandbox_config["default_transaction_count"]
        assert mock_data["compliance_count"] == sandbox_service.sandbox_config["default_compliance_count"] * 2  # KYC + flags
        
        # Verify data relationships
        accounts = mock_data["accounts"]
        transactions = mock_data["transactions"]
        
        # All transactions should reference valid account IDs
        account_ids = {acc.account_id for acc in accounts}
        for tx in transactions:
            assert tx.from_account in account_ids
            assert tx.to_account in account_ids
    
    @pytest.mark.asyncio
    async def test_test_scenario_execution_logging(self, sandbox_service):
        """Test that test scenario execution creates proper logs"""
        result = await sandbox_service.execute_test_scenario("compliance_testing")
        
        assert result["success"] is True
        execution_data = result["data"]
        
        # Check execution log structure
        execution_log = execution_data["execution_log"]
        assert len(execution_log) == execution_data["steps_completed"]
        
        # Check log format
        for log_entry in execution_log:
            assert log_entry.startswith("Step ")
            assert " - Completed" in log_entry
    
    @pytest.mark.asyncio
    async def test_sandbox_config_persistence(self, sandbox_service):
        """Test that sandbox configuration changes persist"""
        original_count = sandbox_service.sandbox_config["default_account_count"]
        
        # Update config
        await sandbox_service.update_sandbox_config({"default_account_count": 500})
        
        # Verify change persisted
        assert sandbox_service.sandbox_config["default_account_count"] == 500
        
        # Verify other config values unchanged
        assert sandbox_service.sandbox_config["default_transaction_count"] == 500  # Original value
        assert sandbox_service.sandbox_config["default_compliance_count"] == 50  # Original value
