"""
Unit tests for AnalyticsService stablecoin adoption functionality
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from api.services.analytics_service import AnalyticsService
from api.models.analytics import StablecoinAdoption


class TestAnalyticsServiceStablecoinAdoption:
    """Test cases for stablecoin adoption analytics"""
    
    @pytest.fixture
    def analytics_service(self):
        """Create AnalyticsService instance with mocked database"""
        mock_db = AsyncMock()
        return AnalyticsService(mock_db)
    
    @pytest.fixture
    def mock_stablecoin_adoption(self):
        """Create mock stablecoin adoption data"""
        adoption = MagicMock()
        adoption.id = "adoption_123"
        adoption.asset_code = "USDC"
        adoption.network = "stellar"
        adoption.country_code = "NG"
        adoption.region = "West Africa"
        adoption.total_volume = "5000.0"
        adoption.total_volume_usd = "5000.0"
        adoption.transaction_count = 100
        adoption.unique_users = 50
        adoption.avg_transaction_size = "50.0"
        adoption.avg_transaction_size_usd = "50.0"
        adoption.volume_growth_rate = 15.5
        adoption.user_growth_rate = 12.3
        adoption.period_start = datetime(2024, 1, 1)
        adoption.period_end = datetime(2024, 1, 31)
        adoption.period_type = "monthly"
        adoption.created_at = datetime(2024, 1, 1)
        adoption.updated_at = datetime(2024, 1, 1)
        return adoption
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_comprehensive(self, analytics_service, mock_stablecoin_adoption):
        """Test comprehensive stablecoin adoption retrieval (AC1-10)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test comprehensive adoption retrieval
        result = await analytics_service.get_stablecoin_adoption(
            asset_code="USDC",
            network="stellar",
            country_code="NG",
            period_type="monthly",
            limit=10,
            offset=0,
            sort_by="total_volume_usd",
            sort_order="desc"
        )
        
        # Verify response structure
        assert "adoptions" in result
        assert "pagination" in result
        assert "filters" in result
        assert "sorting" in result
        assert "analytics" in result
        
        # Verify adoptions data
        assert len(result["adoptions"]) == 1
        adoption = result["adoptions"][0]
        assert adoption["asset_code"] == "USDC"
        assert adoption["network"] == "stellar"
        assert adoption["country_code"] == "NG"
        assert adoption["total_volume"] == "5000.0"
        assert adoption["transaction_count"] == 100
        assert adoption["unique_users"] == 50
        assert adoption["volume_growth_rate"] == 15.5
        assert adoption["user_growth_rate"] == 12.3
        
        # Verify pagination
        assert result["pagination"]["total"] == 1
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["per_page"] == 10
        
        # Verify filters
        assert result["filters"]["asset_code"] == "USDC"
        assert result["filters"]["network"] == "stellar"
        assert result["filters"]["country_code"] == "NG"
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "total_volume_usd"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_with_filters(self, analytics_service, mock_stablecoin_adoption):
        """Test stablecoin adoption with various filters (AC1, AC6)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with multiple filters
        result = await analytics_service.get_stablecoin_adoption(
            asset_code="USDC",
            network="stellar",
            country_code="NG",
            region="West Africa",
            period_type="monthly"
        )
        
        # Verify filters are applied
        assert result["filters"]["asset_code"] == "USDC"
        assert result["filters"]["network"] == "stellar"
        assert result["filters"]["country_code"] == "NG"
        assert result["filters"]["region"] == "West Africa"
        assert result["filters"]["period_type"] == "monthly"
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_time_filtering(self, analytics_service, mock_stablecoin_adoption):
        """Test stablecoin adoption with time-based filtering (AC2, AC7)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with date range
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        
        result = await analytics_service.get_stablecoin_adoption(
            start_date=start_date,
            end_date=end_date,
            period_type="monthly"
        )
        
        # Verify date filters
        assert result["filters"]["start_date"] == start_date.isoformat()
        assert result["filters"]["end_date"] == end_date.isoformat()
        assert result["filters"]["period_type"] == "monthly"
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_pagination(self, analytics_service, mock_stablecoin_adoption):
        """Test stablecoin adoption pagination (AC1, AC10)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 25  # Total 25 adoptions
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test pagination
        result = await analytics_service.get_stablecoin_adoption(
            limit=5,
            offset=10
        )
        
        # Verify pagination metadata
        assert result["pagination"]["total"] == 25
        assert result["pagination"]["page"] == 3  # (10 // 5) + 1
        assert result["pagination"]["per_page"] == 5
        assert result["pagination"]["pages"] == 5  # (25 + 5 - 1) // 5
        assert result["pagination"]["has_next"] is True
        assert result["pagination"]["has_prev"] is True
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_sorting(self, analytics_service, mock_stablecoin_adoption):
        """Test stablecoin adoption sorting (AC5, AC9)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test sorting by transaction count ascending
        result = await analytics_service.get_stablecoin_adoption(
            sort_by="transaction_count",
            sort_order="asc"
        )
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "transaction_count"
        assert result["sorting"]["sort_order"] == "asc"
        
        # Reset mocks for second call
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test sorting by unique users descending
        result = await analytics_service.get_stablecoin_adoption(
            sort_by="unique_users",
            sort_order="desc"
        )
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "unique_users"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_analytics_summary(self, analytics_service):
        """Test stablecoin analytics summary (AC2-5, AC7-10)"""
        # Mock analytics queries
        mock_volume_result = MagicMock()
        mock_volume_result.first.return_value = MagicMock(
            total_volume_usd=10000,
            total_transactions=200,
            total_users=100,
            total_records=5
        )
        
        mock_asset_result = MagicMock()
        mock_asset_result.__iter__.return_value = [
            MagicMock(asset_code="USDC", volume=8000, transactions=160, users=80, avg_volume_growth=15.0, avg_user_growth=12.0),
            MagicMock(asset_code="USDT", volume=2000, transactions=40, users=20, avg_volume_growth=10.0, avg_user_growth=8.0)
        ]
        
        mock_network_result = MagicMock()
        mock_network_result.__iter__.return_value = [
            MagicMock(network="stellar", volume=7000, transactions=140, users=70, avg_volume_growth=14.0, avg_user_growth=11.0),
            MagicMock(network="hedera", volume=3000, transactions=60, users=30, avg_volume_growth=12.0, avg_user_growth=9.0)
        ]
        
        mock_country_result = MagicMock()
        mock_country_result.__iter__.return_value = [
            MagicMock(country_code="NG", volume=5000, transactions=100, users=50, avg_volume_growth=13.0, avg_user_growth=10.0),
            MagicMock(country_code="KE", volume=3000, transactions=60, users=30, avg_volume_growth=11.0, avg_user_growth=8.0)
        ]
        
        mock_regional_result = MagicMock()
        mock_regional_result.__iter__.return_value = [
            MagicMock(region="West Africa", volume=6000, transactions=120, users=60, avg_volume_growth=12.5, avg_user_growth=9.5)
        ]
        
        # Set up side_effect for multiple execute calls
        analytics_service.db.execute.side_effect = [
            mock_volume_result,
            mock_asset_result,
            mock_network_result,
            mock_country_result,
            mock_regional_result
        ]
        
        # Test analytics
        analytics = await analytics_service._get_stablecoin_analytics([])
        
        # Verify analytics structure
        assert "summary" in analytics
        assert "asset_breakdown" in analytics
        assert "network_comparison" in analytics
        assert "country_breakdown" in analytics
        assert "regional_breakdown" in analytics
        
        # Verify summary data
        assert analytics["summary"]["total_volume_usd"] == "10000"
        assert analytics["summary"]["total_transactions"] == 200
        assert analytics["summary"]["total_users"] == 100
        assert analytics["summary"]["total_records"] == 5
        
        # Verify asset breakdown
        assert len(analytics["asset_breakdown"]) == 2
        assert analytics["asset_breakdown"][0]["asset_code"] == "USDC"
        assert analytics["asset_breakdown"][0]["volume"] == "8000"
        assert analytics["asset_breakdown"][0]["avg_volume_growth"] == 15.0
        
        # Verify network comparison
        assert len(analytics["network_comparison"]) == 2
        assert analytics["network_comparison"][0]["network"] == "stellar"
        assert analytics["network_comparison"][0]["volume"] == "7000"
        assert analytics["network_comparison"][0]["avg_volume_growth"] == 14.0
        
        # Verify country breakdown
        assert len(analytics["country_breakdown"]) == 2
        assert analytics["country_breakdown"][0]["country_code"] == "NG"
        assert analytics["country_breakdown"][0]["volume"] == "5000"
        assert analytics["country_breakdown"][0]["avg_volume_growth"] == 13.0
        
        # Verify regional breakdown
        assert len(analytics["regional_breakdown"]) == 1
        assert analytics["regional_breakdown"][0]["region"] == "West Africa"
        assert analytics["regional_breakdown"][0]["volume"] == "6000"
        assert analytics["regional_breakdown"][0]["avg_volume_growth"] == 12.5
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_empty_result(self, analytics_service):
        """Test stablecoin adoption with no results"""
        # Mock empty result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 0
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test empty result
        result = await analytics_service.get_stablecoin_adoption()
        
        # Verify empty result structure
        assert result["adoptions"] == []
        assert result["pagination"]["total"] == 0
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["pages"] == 0
        assert result["pagination"]["has_next"] is False
        assert result["pagination"]["has_prev"] is False
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_error_handling(self, analytics_service):
        """Test stablecoin adoption error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling
        with pytest.raises(Exception, match="Database connection failed"):
            await analytics_service.get_stablecoin_adoption()
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_analytics_error_handling(self, analytics_service):
        """Test stablecoin analytics error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling - should return empty analytics
        analytics = await analytics_service._get_stablecoin_analytics([])
        
        # Verify fallback analytics structure
        assert analytics["summary"]["total_volume_usd"] == "0"
        assert analytics["summary"]["total_transactions"] == 0
        assert analytics["summary"]["total_users"] == 0
        assert analytics["summary"]["total_records"] == 0
        assert analytics["asset_breakdown"] == []
        assert analytics["network_comparison"] == []
        assert analytics["country_breakdown"] == []
        assert analytics["regional_breakdown"] == []
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_asset_breakdown(self, analytics_service, mock_stablecoin_adoption):
        """Test stablecoin adoption with asset breakdown (AC4, AC9)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with asset filter
        result = await analytics_service.get_stablecoin_adoption(
            asset_code="USDC"
        )
        
        # Verify asset filter
        assert result["filters"]["asset_code"] == "USDC"
        
        # Verify adoption has asset information
        assert result["adoptions"][0]["asset_code"] == "USDC"
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_network_comparison(self, analytics_service, mock_stablecoin_adoption):
        """Test stablecoin adoption with network comparison (AC4, AC9)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with network filter
        result = await analytics_service.get_stablecoin_adoption(
            network="stellar"
        )
        
        # Verify network filter
        assert result["filters"]["network"] == "stellar"
        
        # Verify adoption has network information
        assert result["adoptions"][0]["network"] == "stellar"
    
    @pytest.mark.asyncio
    async def test_get_stablecoin_adoption_country_analysis(self, analytics_service, mock_stablecoin_adoption):
        """Test stablecoin adoption with country analysis (AC3, AC8)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_stablecoin_adoption]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with country filter
        result = await analytics_service.get_stablecoin_adoption(
            country_code="NG"
        )
        
        # Verify country filter
        assert result["filters"]["country_code"] == "NG"
        
        # Verify adoption has country information
        assert result["adoptions"][0]["country_code"] == "NG"
