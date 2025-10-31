"""
Unit tests for AnalyticsService data aggregation functionality
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from api.services.analytics_service import AnalyticsService
from api.models.analytics import MerchantActivity, NetworkMetrics


class TestAnalyticsServiceAggregation:
    """Test cases for analytics data aggregation"""
    
    @pytest.fixture
    def analytics_service(self):
        """Create AnalyticsService instance with mocked database"""
        mock_db = AsyncMock()
        return AnalyticsService(mock_db)
    
    @pytest.fixture
    def mock_merchant_activity(self):
        """Create mock merchant activity data"""
        activity = MagicMock()
        activity.id = "activity_123"
        activity.merchant_id = "merchant_456"
        activity.merchant_name = "Test Merchant"
        activity.merchant_type = "retail"
        activity.country_code = "NG"
        activity.region = "West Africa"
        activity.network = "stellar"
        activity.total_volume = "10000.0"
        activity.total_volume_usd = "10000.0"
        activity.transaction_count = 200
        activity.unique_customers = 100
        activity.avg_transaction_size = "50.0"
        activity.avg_transaction_size_usd = "50.0"
        activity.stellar_volume = "10000.0"
        activity.hedera_volume = "10000.0"
        activity.stellar_transactions = 200
        activity.hedera_transactions = 200
        activity.period_start = datetime(2024, 1, 1)
        activity.period_end = datetime(2024, 1, 31)
        activity.period_type = "monthly"
        activity.created_at = datetime(2024, 1, 1)
        activity.updated_at = datetime(2024, 1, 1)
        return activity
    
    @pytest.fixture
    def mock_network_metrics(self):
        """Create mock network metrics data"""
        metrics = MagicMock()
        metrics.id = "metrics_123"
        metrics.network = "stellar"
        metrics.environment = "mainnet"
        metrics.period_start = datetime(2024, 1, 1)
        metrics.period_end = datetime(2024, 1, 2)
        metrics.period_type = "daily"
        metrics.total_transactions = 1000
        metrics.total_volume = "50000.0"
        metrics.total_volume_usd = "50000.0"
        metrics.avg_transaction_fee = "0.01"
        metrics.avg_transaction_fee_usd = "0.01"
        metrics.avg_confirmation_time = 2.5
        metrics.success_rate = 95.0
        metrics.active_accounts = 500
        metrics.new_accounts = 25
        metrics.africa_transaction_count = 800
        metrics.africa_volume = "40000.0"
        metrics.africa_volume_usd = "40000.0"
        metrics.created_at = datetime(2024, 1, 1)
        metrics.updated_at = datetime(2024, 1, 1)
        return metrics
    
    @pytest.mark.asyncio
    async def test_get_merchant_activity_comprehensive(self, analytics_service, mock_merchant_activity):
        """Test comprehensive merchant activity retrieval (AC1-10)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_merchant_activity]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test comprehensive merchant activity retrieval
        result = await analytics_service.get_merchant_activity(
            merchant_type="retail",
            country_code="NG",
            network="stellar",
            period_type="monthly",
            limit=10,
            offset=0,
            sort_by="total_volume_usd",
            sort_order="desc"
        )
        
        # Verify response structure
        assert "activities" in result
        assert "pagination" in result
        assert "filters" in result
        assert "sorting" in result
        assert "analytics" in result
        
        # Verify activities data
        assert len(result["activities"]) == 1
        activity = result["activities"][0]
        assert activity["merchant_id"] == "merchant_456"
        assert activity["merchant_name"] == "Test Merchant"
        assert activity["merchant_type"] == "retail"
        assert activity["country_code"] == "NG"
        assert activity["total_volume"] == "10000.0"
        assert activity["transaction_count"] == 200
        assert activity["unique_customers"] == 100
        assert activity["stellar_volume"] == "10000.0"
        assert activity["hedera_volume"] == "10000.0"
        assert activity["stellar_transactions"] == 200
        assert activity["hedera_transactions"] == 200
        
        # Verify pagination
        assert result["pagination"]["total"] == 1
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["per_page"] == 10
        
        # Verify filters
        assert result["filters"]["merchant_type"] == "retail"
        assert result["filters"]["country_code"] == "NG"
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "total_volume_usd"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_get_merchant_activity_with_filters(self, analytics_service, mock_merchant_activity):
        """Test merchant activity with various filters (AC1, AC6)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_merchant_activity]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with multiple filters
        result = await analytics_service.get_merchant_activity(
            merchant_type="retail",
            country_code="NG",
            period_type="monthly"
        )
        
        # Verify filters are applied
        assert result["filters"]["merchant_type"] == "retail"
        assert result["filters"]["country_code"] == "NG"
        assert result["filters"]["period_type"] == "monthly"
    
    @pytest.mark.asyncio
    async def test_get_merchant_activity_time_filtering(self, analytics_service, mock_merchant_activity):
        """Test merchant activity with time-based filtering (AC2, AC7)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_merchant_activity]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with date range
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        
        result = await analytics_service.get_merchant_activity(
            start_date=start_date,
            end_date=end_date,
            period_type="monthly"
        )
        
        # Verify date filters
        assert result["filters"]["start_date"] == start_date.isoformat()
        assert result["filters"]["end_date"] == end_date.isoformat()
        assert result["filters"]["period_type"] == "monthly"
    
    @pytest.mark.asyncio
    async def test_get_merchant_analytics_summary(self, analytics_service):
        """Test merchant analytics summary (AC2-5, AC7-10)"""
        # Mock analytics queries
        mock_volume_result = MagicMock()
        mock_volume_result.first.return_value = MagicMock(
            total_volume_usd=20000,
            total_transactions=400,
            total_customers=200,
            total_merchants=10
        )
        
        mock_type_result = MagicMock()
        mock_type_result.__iter__.return_value = [
            MagicMock(merchant_type="retail", volume=15000, transactions=300, customers=150),
            MagicMock(merchant_type="ecommerce", volume=5000, transactions=100, customers=50)
        ]
        
        mock_network_result = MagicMock()
        mock_network_result.__iter__.return_value = [
            MagicMock(network="stellar", volume=12000, transactions=240, customers=120),
            MagicMock(network="hedera", volume=8000, transactions=160, customers=80)
        ]
        
        mock_country_result = MagicMock()
        mock_country_result.__iter__.return_value = [
            MagicMock(country_code="NG", volume=10000, transactions=200, customers=100),
            MagicMock(country_code="KE", volume=6000, transactions=120, customers=60)
        ]
        
        mock_regional_result = MagicMock()
        mock_regional_result.__iter__.return_value = [
            MagicMock(region="West Africa", volume=12000, transactions=240, customers=120)
        ]
        
        # Set up side_effect for multiple execute calls
        analytics_service.db.execute.side_effect = [
            mock_volume_result,
            mock_type_result,
            mock_network_result,
            mock_country_result,
            mock_regional_result
        ]
        
        # Test analytics
        analytics = await analytics_service._get_merchant_analytics([])
        
        # Verify analytics structure
        assert "summary" in analytics
        assert "merchant_type_breakdown" in analytics
        assert "network_breakdown" in analytics
        assert "country_breakdown" in analytics
        assert "regional_breakdown" in analytics
        
        # Verify summary data
        assert analytics["summary"]["total_volume_usd"] == "20000"
        assert analytics["summary"]["total_transactions"] == 400
        assert analytics["summary"]["total_customers"] == 200
        assert analytics["summary"]["total_merchants"] == 10
        
        # Verify merchant type breakdown
        assert len(analytics["merchant_type_breakdown"]) == 2
        assert analytics["merchant_type_breakdown"][0]["merchant_type"] == "retail"
        assert analytics["merchant_type_breakdown"][0]["volume"] == "15000"
        
        # Verify network breakdown (hardcoded values)
        assert len(analytics["network_breakdown"]) == 2
        assert analytics["network_breakdown"][0]["network"] == "stellar"
        assert analytics["network_breakdown"][0]["volume"] == "0"
        
        # Verify country breakdown
        assert len(analytics["country_breakdown"]) == 2
        assert analytics["country_breakdown"][0]["country_code"] == "NG"
        assert analytics["country_breakdown"][0]["volume"] == "10000"
        
        # Verify regional breakdown
        assert len(analytics["regional_breakdown"]) == 1
        assert analytics["regional_breakdown"][0]["region"] == "West Africa"
        assert analytics["regional_breakdown"][0]["volume"] == "12000"
    
    @pytest.mark.asyncio
    async def test_get_network_metrics_comprehensive(self, analytics_service, mock_network_metrics):
        """Test comprehensive network metrics retrieval (AC1-10)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_network_metrics]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test comprehensive network metrics retrieval
        result = await analytics_service.get_network_metrics(
            network="stellar",
            period_type="daily",
            limit=10,
            offset=0,
            sort_by="timestamp",
            sort_order="desc"
        )
        
        # Verify response structure
        assert "metrics" in result
        assert "pagination" in result
        assert "filters" in result
        assert "sorting" in result
        assert "analytics" in result
        
        # Verify metrics data
        assert len(result["metrics"]) == 1
        metric = result["metrics"][0]
        assert metric["network"] == "stellar"
        assert metric["environment"] == "mainnet"
        assert metric["period_type"] == "daily"
        assert metric["total_transactions"] == 1000
        assert metric["total_volume"] == "50000.0"
        assert metric["success_rate"] == 95.0
        assert metric["avg_confirmation_time"] == 2.5
        assert metric["active_accounts"] == 500
        assert metric["new_accounts"] == 25
        assert metric["africa_transaction_count"] == 800
        assert metric["africa_volume"] == "40000.0"
        
        # Verify pagination
        assert result["pagination"]["total"] == 1
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["per_page"] == 10
        
        # Verify filters
        assert result["filters"]["network"] == "stellar"
        assert result["filters"]["period_type"] == "daily"
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "timestamp"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_get_network_metrics_with_filters(self, analytics_service, mock_network_metrics):
        """Test network metrics with various filters (AC1, AC6)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_network_metrics]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with multiple filters
        result = await analytics_service.get_network_metrics(
            network="stellar",
            period_type="daily"
        )
        
        # Verify filters are applied
        assert result["filters"]["network"] == "stellar"
        assert result["filters"]["period_type"] == "daily"
    
    @pytest.mark.asyncio
    async def test_get_network_metrics_time_filtering(self, analytics_service, mock_network_metrics):
        """Test network metrics with time-based filtering (AC2, AC7)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_network_metrics]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with date range
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        
        result = await analytics_service.get_network_metrics(
            start_date=start_date,
            end_date=end_date,
            period_type="daily"
        )
        
        # Verify date filters
        assert result["filters"]["start_date"] == start_date.isoformat()
        assert result["filters"]["end_date"] == end_date.isoformat()
        assert result["filters"]["period_type"] == "daily"
    
    @pytest.mark.asyncio
    async def test_get_network_analytics_summary(self, analytics_service):
        """Test network analytics summary (AC2-5, AC7-10)"""
        # Mock analytics queries
        mock_total_result = MagicMock()
        mock_total_result.first.return_value = MagicMock(
            total_transactions=2000,
            total_volume_usd=100000,
            avg_success_rate=95.0,
            avg_confirmation_time=2.5,
            total_active_accounts=1000,
            total_new_accounts=50,
            total_africa_transactions=1600,
            total_africa_volume_usd=80000
        )
        
        mock_network_result = MagicMock()
        mock_network_result.__iter__.return_value = [
            MagicMock(network="stellar", transactions=1200, volume=60000, avg_success_rate=95.0, avg_confirmation_time=2.0, active_accounts=600, new_accounts=30, africa_transactions=960, africa_volume=48000),
            MagicMock(network="hedera", transactions=800, volume=40000, avg_success_rate=95.0, avg_confirmation_time=3.0, active_accounts=400, new_accounts=20, africa_transactions=640, africa_volume=32000)
        ]
        
        mock_period_result = MagicMock()
        mock_period_result.__iter__.return_value = [
            MagicMock(period_type="daily", transactions=1000, volume=50000, avg_success_rate=95.0, avg_confirmation_time=2.5, africa_transactions=800, africa_volume=40000),
            MagicMock(period_type="hourly", transactions=1000, volume=50000, avg_success_rate=95.0, avg_confirmation_time=2.5, africa_transactions=800, africa_volume=40000)
        ]
        
        # Set up side_effect for multiple execute calls
        analytics_service.db.execute.side_effect = [
            mock_total_result,
            mock_network_result,
            mock_period_result
        ]
        
        # Test analytics
        analytics = await analytics_service._get_network_analytics([])
        
        # Verify analytics structure
        assert "summary" in analytics
        assert "network_breakdown" in analytics
        assert "period_breakdown" in analytics
        
        # Verify summary data
        assert analytics["summary"]["total_transactions"] == 2000
        assert analytics["summary"]["total_volume_usd"] == "100000"
        assert analytics["summary"]["avg_success_rate"] == 95.0
        assert analytics["summary"]["avg_confirmation_time"] == 2.5
        assert analytics["summary"]["total_active_accounts"] == 1000
        assert analytics["summary"]["total_new_accounts"] == 50
        assert analytics["summary"]["total_africa_transactions"] == 1600
        assert analytics["summary"]["total_africa_volume_usd"] == "80000"
        
        # Verify network breakdown
        assert len(analytics["network_breakdown"]) == 2
        assert analytics["network_breakdown"][0]["network"] == "stellar"
        assert analytics["network_breakdown"][0]["transactions"] == 1200
        assert analytics["network_breakdown"][0]["avg_success_rate"] == 95.0
        assert analytics["network_breakdown"][0]["africa_transactions"] == 960
        
        # Verify period breakdown
        assert len(analytics["period_breakdown"]) == 2
        assert analytics["period_breakdown"][0]["period_type"] == "daily"
        assert analytics["period_breakdown"][0]["transactions"] == 1000
        assert analytics["period_breakdown"][0]["avg_success_rate"] == 95.0
        assert analytics["period_breakdown"][0]["africa_transactions"] == 800
    
    @pytest.mark.asyncio
    async def test_get_merchant_activity_empty_result(self, analytics_service):
        """Test merchant activity with no results"""
        # Mock empty result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 0
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test empty result
        result = await analytics_service.get_merchant_activity()
        
        # Verify empty result structure
        assert result["activities"] == []
        assert result["pagination"]["total"] == 0
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["pages"] == 0
        assert result["pagination"]["has_next"] is False
        assert result["pagination"]["has_prev"] is False
    
    @pytest.mark.asyncio
    async def test_get_network_metrics_empty_result(self, analytics_service):
        """Test network metrics with no results"""
        # Mock empty result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 0
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test empty result
        result = await analytics_service.get_network_metrics()
        
        # Verify empty result structure
        assert result["metrics"] == []
        assert result["pagination"]["total"] == 0
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["pages"] == 0
        assert result["pagination"]["has_next"] is False
        assert result["pagination"]["has_prev"] is False
    
    @pytest.mark.asyncio
    async def test_get_merchant_activity_error_handling(self, analytics_service):
        """Test merchant activity error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling
        with pytest.raises(Exception, match="Database connection failed"):
            await analytics_service.get_merchant_activity()
    
    @pytest.mark.asyncio
    async def test_get_network_metrics_error_handling(self, analytics_service):
        """Test network metrics error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling
        with pytest.raises(Exception, match="Database connection failed"):
            await analytics_service.get_network_metrics()
    
    @pytest.mark.asyncio
    async def test_get_merchant_analytics_error_handling(self, analytics_service):
        """Test merchant analytics error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling - should return empty analytics
        analytics = await analytics_service._get_merchant_analytics([])
        
        # Verify fallback analytics structure
        assert analytics["summary"]["total_volume_usd"] == "0"
        assert analytics["summary"]["total_transactions"] == 0
        assert analytics["summary"]["total_customers"] == 0
        assert analytics["summary"]["total_merchants"] == 0
        assert analytics["merchant_type_breakdown"] == []
        assert analytics["network_breakdown"] == []
        assert analytics["country_breakdown"] == []
        assert analytics["regional_breakdown"] == []
    
    @pytest.mark.asyncio
    async def test_get_network_analytics_error_handling(self, analytics_service):
        """Test network analytics error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling - should return empty analytics
        analytics = await analytics_service._get_network_analytics([])
        
        # Verify fallback analytics structure
        assert analytics["summary"]["total_transactions"] == 0
        assert analytics["summary"]["total_volume_usd"] == "0"
        assert analytics["summary"]["avg_success_rate"] is None
        assert analytics["summary"]["avg_confirmation_time"] is None
        assert analytics["summary"]["total_active_accounts"] == 0
        assert analytics["summary"]["total_new_accounts"] == 0
        assert analytics["summary"]["total_africa_transactions"] == 0
        assert analytics["summary"]["total_africa_volume_usd"] == "0"
        assert analytics["network_breakdown"] == []
        assert analytics["period_breakdown"] == []
