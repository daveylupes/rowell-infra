"""
Unit tests for AnalyticsService remittance flows functionality
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from api.services.analytics_service import AnalyticsService
from api.models.analytics import RemittanceFlow


class TestAnalyticsServiceRemittanceFlows:
    """Test cases for remittance flows analytics"""
    
    @pytest.fixture
    def analytics_service(self):
        """Create AnalyticsService instance with mocked database"""
        mock_db = AsyncMock()
        return AnalyticsService(mock_db)
    
    @pytest.fixture
    def mock_remittance_flow(self):
        """Create mock remittance flow data"""
        flow = MagicMock()
        flow.id = "flow_123"
        flow.from_country = "NG"
        flow.to_country = "KE"
        flow.from_region = "West Africa"
        flow.to_region = "East Africa"
        flow.asset_code = "USDC"
        flow.network = "stellar"
        flow.total_volume = "1000.0"
        flow.total_volume_usd = "1000.0"
        flow.transaction_count = 50
        flow.unique_senders = 25
        flow.unique_receivers = 30
        flow.avg_fee = "0.01"
        flow.avg_fee_usd = "0.01"
        flow.avg_fee_percentage = 1.0
        flow.avg_settlement_time = 5.5
        flow.success_rate = 98.5
        flow.period_start = datetime(2024, 1, 1)
        flow.period_end = datetime(2024, 1, 31)
        flow.period_type = "monthly"
        flow.created_at = datetime(2024, 1, 1)
        flow.updated_at = datetime(2024, 1, 1)
        return flow
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_comprehensive(self, analytics_service, mock_remittance_flow):
        """Test comprehensive remittance flows retrieval (AC1-10)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_remittance_flow]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test comprehensive flows retrieval
        result = await analytics_service.get_remittance_flows(
            from_country="NG",
            to_country="KE",
            asset_code="USDC",
            network="stellar",
            period_type="monthly",
            limit=10,
            offset=0,
            sort_by="total_volume_usd",
            sort_order="desc"
        )
        
        # Verify response structure
        assert "flows" in result
        assert "pagination" in result
        assert "filters" in result
        assert "sorting" in result
        assert "analytics" in result
        
        # Verify flows data
        assert len(result["flows"]) == 1
        flow = result["flows"][0]
        assert flow["from_country"] == "NG"
        assert flow["to_country"] == "KE"
        assert flow["asset_code"] == "USDC"
        assert flow["network"] == "stellar"
        assert flow["total_volume"] == "1000.0"
        assert flow["transaction_count"] == 50
        assert flow["unique_senders"] == 25
        assert flow["unique_receivers"] == 30
        
        # Verify pagination
        assert result["pagination"]["total"] == 1
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["per_page"] == 10
        
        # Verify filters
        assert result["filters"]["from_country"] == "NG"
        assert result["filters"]["to_country"] == "KE"
        assert result["filters"]["asset_code"] == "USDC"
        assert result["filters"]["network"] == "stellar"
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "total_volume_usd"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_with_filters(self, analytics_service, mock_remittance_flow):
        """Test remittance flows with various filters (AC1, AC6)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_remittance_flow]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with multiple filters
        result = await analytics_service.get_remittance_flows(
            from_country="NG",
            to_country="KE",
            from_region="West Africa",
            to_region="East Africa",
            asset_code="USDC",
            network="stellar",
            period_type="monthly"
        )
        
        # Verify filters are applied
        assert result["filters"]["from_country"] == "NG"
        assert result["filters"]["to_country"] == "KE"
        assert result["filters"]["from_region"] == "West Africa"
        assert result["filters"]["to_region"] == "East Africa"
        assert result["filters"]["asset_code"] == "USDC"
        assert result["filters"]["network"] == "stellar"
        assert result["filters"]["period_type"] == "monthly"
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_time_filtering(self, analytics_service, mock_remittance_flow):
        """Test remittance flows with time-based filtering (AC3, AC8)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_remittance_flow]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with date range
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        
        result = await analytics_service.get_remittance_flows(
            start_date=start_date,
            end_date=end_date,
            period_type="monthly"
        )
        
        # Verify date filters
        assert result["filters"]["start_date"] == start_date.isoformat()
        assert result["filters"]["end_date"] == end_date.isoformat()
        assert result["filters"]["period_type"] == "monthly"
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_pagination(self, analytics_service, mock_remittance_flow):
        """Test remittance flows pagination (AC1, AC10)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_remittance_flow]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 25  # Total 25 flows
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test pagination
        result = await analytics_service.get_remittance_flows(
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
    async def test_get_remittance_flows_sorting(self, analytics_service, mock_remittance_flow):
        """Test remittance flows sorting (AC5, AC9)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_remittance_flow]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test sorting by transaction count ascending
        result = await analytics_service.get_remittance_flows(
            sort_by="transaction_count",
            sort_order="asc"
        )
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "transaction_count"
        assert result["sorting"]["sort_order"] == "asc"
        
        # Reset mocks for second call
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test sorting by period start descending
        result = await analytics_service.get_remittance_flows(
            sort_by="period_start",
            sort_order="desc"
        )
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "period_start"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_get_remittance_analytics_summary(self, analytics_service):
        """Test remittance analytics summary (AC2, AC7)"""
        # Mock analytics queries
        mock_volume_result = MagicMock()
        mock_volume_result.first.return_value = MagicMock(
            total_volume_usd=1000,
            total_transactions=50,
            total_flows=5
        )
        
        mock_corridors_result = MagicMock()
        mock_corridors_result.__iter__.return_value = [
            MagicMock(from_country="NG", to_country="KE", volume=500, transactions=25),
            MagicMock(from_country="GH", to_country="NG", volume=300, transactions=15)
        ]
        
        mock_asset_result = MagicMock()
        mock_asset_result.__iter__.return_value = [
            MagicMock(asset_code="USDC", volume=800, transactions=40),
            MagicMock(asset_code="XLM", volume=200, transactions=10)
        ]
        
        mock_regional_result = MagicMock()
        mock_regional_result.__iter__.return_value = [
            MagicMock(from_region="West Africa", to_region="East Africa", volume=600, transactions=30)
        ]
        
        # Set up side_effect for multiple execute calls
        analytics_service.db.execute.side_effect = [
            mock_volume_result,
            mock_corridors_result,
            mock_asset_result,
            mock_regional_result
        ]
        
        # Test analytics
        analytics = await analytics_service._get_remittance_analytics([])
        
        # Verify analytics structure
        assert "summary" in analytics
        assert "top_corridors" in analytics
        assert "asset_breakdown" in analytics
        assert "regional_breakdown" in analytics
        
        # Verify summary data
        assert analytics["summary"]["total_volume_usd"] == "1000"
        assert analytics["summary"]["total_transactions"] == 50
        assert analytics["summary"]["total_flows"] == 5
        
        # Verify top corridors
        assert len(analytics["top_corridors"]) == 2
        assert analytics["top_corridors"][0]["from_country"] == "NG"
        assert analytics["top_corridors"][0]["to_country"] == "KE"
        assert analytics["top_corridors"][0]["volume"] == "500"
        
        # Verify asset breakdown
        assert len(analytics["asset_breakdown"]) == 2
        assert analytics["asset_breakdown"][0]["asset_code"] == "USDC"
        assert analytics["asset_breakdown"][0]["volume"] == "800"
        
        # Verify regional breakdown
        assert len(analytics["regional_breakdown"]) == 1
        assert analytics["regional_breakdown"][0]["from_region"] == "West Africa"
        assert analytics["regional_breakdown"][0]["to_region"] == "East Africa"
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_empty_result(self, analytics_service):
        """Test remittance flows with no results"""
        # Mock empty result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 0
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test empty result
        result = await analytics_service.get_remittance_flows()
        
        # Verify empty result structure
        assert result["flows"] == []
        assert result["pagination"]["total"] == 0
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["pages"] == 0
        assert result["pagination"]["has_next"] is False
        assert result["pagination"]["has_prev"] is False
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_error_handling(self, analytics_service):
        """Test remittance flows error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling
        with pytest.raises(Exception, match="Database connection failed"):
            await analytics_service.get_remittance_flows()
    
    @pytest.mark.asyncio
    async def test_get_remittance_analytics_error_handling(self, analytics_service):
        """Test remittance analytics error handling"""
        # Mock database error
        analytics_service.db.execute.side_effect = Exception("Database connection failed")
        
        # Test error handling - should return empty analytics
        analytics = await analytics_service._get_remittance_analytics([])
        
        # Verify fallback analytics structure
        assert analytics["summary"]["total_volume_usd"] == "0"
        assert analytics["summary"]["total_transactions"] == 0
        assert analytics["summary"]["total_flows"] == 0
        assert analytics["top_corridors"] == []
        assert analytics["asset_breakdown"] == []
        assert analytics["regional_breakdown"] == []
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_asset_breakdown(self, analytics_service, mock_remittance_flow):
        """Test remittance flows with asset type breakdown (AC4, AC9)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_remittance_flow]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with asset filter
        result = await analytics_service.get_remittance_flows(
            asset_code="USDC"
        )
        
        # Verify asset filter
        assert result["filters"]["asset_code"] == "USDC"
        
        # Verify flow has asset information
        assert result["flows"][0]["asset_code"] == "USDC"
    
    @pytest.mark.asyncio
    async def test_get_remittance_flows_regional_analysis(self, analytics_service, mock_remittance_flow):
        """Test remittance flows with regional analysis (AC5, AC10)"""
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [mock_remittance_flow]
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        analytics_service.db.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with regional filters
        result = await analytics_service.get_remittance_flows(
            from_region="West Africa",
            to_region="East Africa"
        )
        
        # Verify regional filters
        assert result["filters"]["from_region"] == "West Africa"
        assert result["filters"]["to_region"] == "East Africa"
        
        # Verify flow has regional information
        assert result["flows"][0]["from_region"] == "West Africa"
        assert result["flows"][0]["to_region"] == "East Africa"
