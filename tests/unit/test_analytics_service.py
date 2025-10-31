"""
Unit tests for AnalyticsService
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from decimal import Decimal

from api.services.analytics_service import AnalyticsService
from api.models.account import Account
from api.models.transaction import Transaction


def create_mock_account(**kwargs):
    """Helper function to create mock account with default values"""
    defaults = {
        "id": "1",
        "account_id": "GABC1234567890",
        "network": "stellar",
        "environment": "testnet",
        "account_type": "user",
        "country_code": "NG",
        "is_active": True,
        "created_at": datetime.now()
    }
    defaults.update(kwargs)
    return Account(**defaults)


def create_mock_transaction(**kwargs):
    """Helper function to create mock transaction with default values"""
    defaults = {
        "id": "1",
        "transaction_hash": "mock_stellar_tx_123456",
        "from_account": "GABC1234567890",
        "to_account": "GXYZ0987654321",
        "asset_code": "XLM",
        "amount": "10.0",
        "amount_usd": "10.0",
        "network": "stellar",
        "environment": "testnet",
        "status": "success",
        "from_country": "NG",
        "to_country": "KE",
        "created_at": datetime.now()
    }
    defaults.update(kwargs)
    return Transaction(**defaults)


class TestAnalyticsService:
    """Test cases for AnalyticsService"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        return AsyncMock(spec=AsyncSession)
    
    @pytest.fixture
    def analytics_service(self, mock_db_session):
        """Analytics service instance with mocked database"""
        return AnalyticsService(mock_db_session)
    
    @pytest.mark.asyncio
    async def test_get_total_accounts_success(self, analytics_service, mock_db_session):
        """Test successful account count retrieval"""
        # Mock database query result
        mock_result = MagicMock()
        mock_result.scalar.return_value = 150
        mock_db_session.execute.return_value = mock_result
        
        # Test account count
        result = await analytics_service._get_total_accounts()
        
        # Assertions
        assert result == 150
        mock_db_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_total_accounts_zero(self, analytics_service, mock_db_session):
        """Test account count when no accounts exist"""
        # Mock database query result
        mock_result = MagicMock()
        mock_result.scalar.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test account count
        result = await analytics_service._get_total_accounts()
        
        # Assertions
        assert result == 0
    
    @pytest.mark.asyncio
    async def test_get_total_accounts_error(self, analytics_service, mock_db_session):
        """Test account count with database error"""
        # Mock database error
        mock_db_session.execute.side_effect = Exception("Database error")
        
        # Test account count
        result = await analytics_service._get_total_accounts()
        
        # Assertions
        assert result == 0
    
    @pytest.mark.asyncio
    async def test_get_total_transaction_volume_success(self, analytics_service, mock_db_session):
        """Test successful transaction volume calculation"""
        # Mock database query result
        count_result = MagicMock()
        count_result.scalar.return_value = 100
        mock_db_session.execute.return_value = count_result
        
        # Test transaction volume
        result = await analytics_service._get_total_transaction_volume()
        
        # Assertions
        assert result["transaction_count"] == 100
        assert result["total_volume"] == "1000"  # 100 * 10
        assert result["total_volume_usd"] == "1000"  # 100 * 10
        assert mock_db_session.execute.call_count == 1
    
    @pytest.mark.asyncio
    async def test_get_total_transaction_volume_empty(self, analytics_service, mock_db_session):
        """Test transaction volume when no transactions exist"""
        # Mock database query result
        count_result = MagicMock()
        count_result.scalar.return_value = 0
        mock_db_session.execute.return_value = count_result
        
        # Test transaction volume
        result = await analytics_service._get_total_transaction_volume()
        
        # Assertions
        assert result["transaction_count"] == 0
        assert result["total_volume"] == "0"
        assert result["total_volume_usd"] == "0"
    
    @pytest.mark.asyncio
    async def test_get_success_rate_success(self, analytics_service, mock_db_session):
        """Test successful success rate calculation"""
        # Mock database query results
        total_result = MagicMock()
        total_result.scalar.return_value = 100
        
        success_result = MagicMock()
        success_result.scalar.return_value = 85
        
        mock_db_session.execute.side_effect = [total_result, success_result]
        
        # Test success rate
        result = await analytics_service._get_success_rate()
        
        # Assertions
        assert result == 85.0
        assert mock_db_session.execute.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_success_rate_zero_transactions(self, analytics_service, mock_db_session):
        """Test success rate when no transactions exist"""
        # Mock database query result
        total_result = MagicMock()
        total_result.scalar.return_value = 0
        mock_db_session.execute.return_value = total_result
        
        # Test success rate
        result = await analytics_service._get_success_rate()
        
        # Assertions
        assert result == 0.0
    
    @pytest.mark.asyncio
    async def test_get_active_networks_success(self, analytics_service, mock_db_session):
        """Test successful active networks retrieval"""
        # Mock database query result
        mock_result = MagicMock()
        mock_result.__iter__ = lambda self: iter([
            MagicMock(network="stellar", environment="testnet", transaction_count=50, volume_usd=Decimal("500.0")),
            MagicMock(network="hedera", environment="testnet", transaction_count=30, volume_usd=Decimal("300.0"))
        ])
        mock_db_session.execute.return_value = mock_result
        
        # Test active networks
        result = await analytics_service._get_active_networks()
        
        # Assertions
        assert len(result) == 2
        assert result[0]["network"] == "stellar"
        assert result[0]["environment"] == "testnet"
        assert result[0]["transaction_count"] == 50
        assert result[0]["volume_usd"] == "500"
        assert result[0]["status"] == "active"
        assert result[1]["network"] == "hedera"
        assert result[1]["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_get_recent_activity_success(self, analytics_service, mock_db_session):
        """Test successful recent activity retrieval"""
        # Mock database query result
        mock_transaction = create_mock_transaction()
        mock_result = MagicMock()
        mock_result.scalars.return_value = [mock_transaction]
        mock_db_session.execute.return_value = mock_result
        
        # Test recent activity
        result = await analytics_service._get_recent_activity()
        
        # Assertions
        assert len(result) == 1
        assert result[0]["type"] == "transaction"
        assert result[0]["transaction_hash"] == "mock_stellar_tx_123456"
        assert result[0]["from_account"] == "GABC1234567890"
        assert result[0]["to_account"] == "GXYZ0987654321"
        assert result[0]["asset_code"] == "XLM"
        assert result[0]["amount"] == "10.0"
        assert result[0]["network"] == "stellar"
        assert result[0]["status"] == "success"
        assert result[0]["from_country"] == "NG"
        assert result[0]["to_country"] == "KE"
    
    @pytest.mark.asyncio
    async def test_get_recent_activity_empty(self, analytics_service, mock_db_session):
        """Test recent activity when no recent transactions exist"""
        # Mock database query result
        mock_result = MagicMock()
        mock_result.scalars.return_value = []
        mock_db_session.execute.return_value = mock_result
        
        # Test recent activity
        result = await analytics_service._get_recent_activity()
        
        # Assertions
        assert len(result) == 0
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_top_countries_success(self, analytics_service, mock_db_session):
        """Test successful top countries retrieval"""
        # Mock database query result
        mock_result = MagicMock()
        mock_result.__iter__ = lambda self: iter([
            MagicMock(from_country="NG", transaction_count=50, volume_usd=Decimal("500.0")),
            MagicMock(from_country="KE", transaction_count=30, volume_usd=Decimal("300.0"))
        ])
        mock_db_session.execute.return_value = mock_result
        
        # Test top countries
        result = await analytics_service._get_top_countries()
        
        # Assertions
        assert len(result) == 2
        assert result[0]["country_code"] == "NG"
        assert result[0]["transaction_count"] == 50
        assert result[0]["volume_usd"] == "500"
        assert result[1]["country_code"] == "KE"
        assert result[1]["transaction_count"] == 30
        assert result[1]["volume_usd"] == "300"
    
    @pytest.mark.asyncio
    async def test_get_dashboard_data_success(self, analytics_service, mock_db_session):
        """Test successful dashboard data retrieval"""
        # Mock all the individual methods
        with patch.object(analytics_service, '_get_total_accounts', return_value=150) as mock_accounts, \
             patch.object(analytics_service, '_get_total_transaction_volume', return_value={
                 "transaction_count": 100,
                 "total_volume": "1000.0",
                 "total_volume_usd": "1000.0"
             }) as mock_volume, \
             patch.object(analytics_service, '_get_success_rate', return_value=85.5) as mock_success, \
             patch.object(analytics_service, '_get_active_networks', return_value=[
                 {"network": "stellar", "environment": "testnet", "transaction_count": 50, "volume_usd": "500.0", "status": "active"}
             ]) as mock_networks, \
             patch.object(analytics_service, '_get_recent_activity', return_value=[
                 {"type": "transaction", "id": "1", "transaction_hash": "test_hash"}
             ]) as mock_activity, \
             patch.object(analytics_service, '_get_top_countries', return_value=[
                 {"country_code": "NG", "transaction_count": 50, "volume_usd": "500.0"}
             ]) as mock_countries:
            
            # Test dashboard data
            result = await analytics_service.get_dashboard_data()
            
            # Assertions
            assert result["total_accounts"] == 150
            assert result["total_transactions"] == 100
            assert result["total_volume"] == "1000.0"
            assert result["total_volume_usd"] == "1000.0"
            assert result["success_rate"] == 85.5
            assert len(result["active_networks"]) == 1
            assert result["active_networks"][0]["network"] == "stellar"
            assert len(result["recent_activity"]) == 1
            assert result["recent_activity"][0]["type"] == "transaction"
            assert len(result["top_countries"]) == 1
            assert result["top_countries"][0]["country_code"] == "NG"
            
            # Verify all methods were called
            mock_accounts.assert_called_once()
            mock_volume.assert_called_once()
            mock_success.assert_called_once()
            mock_networks.assert_called_once()
            mock_activity.assert_called_once()
            mock_countries.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_dashboard_data_error(self, analytics_service, mock_db_session):
        """Test dashboard data with error handling"""
        # Mock error in one of the methods
        with patch.object(analytics_service, '_get_total_accounts', side_effect=Exception("Database error")):
            
            # Test dashboard data
            result = await analytics_service.get_dashboard_data()
            
            # Assertions - should return empty data on error
            assert result["total_accounts"] == 0
            assert result["total_transactions"] == 0
            assert result["total_volume"] == "0"
            assert result["total_volume_usd"] == "0"
            assert result["success_rate"] == 0.0
            assert result["active_networks"] == []
            assert result["recent_activity"] == []
            assert result["top_countries"] == []
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_empty(self, analytics_service):
        """Test remittance flows returns empty list (MVP implementation)"""
        result = await analytics_service.get_remittance_flows()
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_empty(self, analytics_service):
        """Test stablecoin adoption returns empty list (MVP implementation)"""
        result = await analytics_service.get_stablecoin_adoption()
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_merchant_activity_empty(self, analytics_service):
        """Test merchant activity returns empty list (MVP implementation)"""
        result = await analytics_service.get_merchant_activity()
        assert result == []
    
    @pytest.mark.asyncio
    async def test_get_network_metrics_empty(self, analytics_service):
        """Test network metrics returns empty list (MVP implementation)"""
        result = await analytics_service.get_network_metrics()
        assert result == []
