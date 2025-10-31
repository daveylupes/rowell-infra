"""
Unit tests for ComplianceService - Flags functionality
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from decimal import Decimal

from api.services.compliance_service import ComplianceService


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return AsyncMock()


@pytest.fixture
def compliance_service(mock_db_session):
    """ComplianceService instance with mocked database"""
    return ComplianceService(mock_db_session)


@pytest.fixture
def sample_flag_data():
    """Sample flag data for testing"""
    return {
        "entity_type": "transaction",
        "entity_id": "tx_123456",
        "network": "stellar",
        "flag_type": "aml",
        "flag_severity": "high",
        "flag_reason": "Suspicious transaction pattern",
        "risk_score": 85.5,
        "country_code": "NG",
        "region": "west_africa"
    }


class TestComplianceFlagsService:
    """Test cases for ComplianceService flags functionality"""
    
    @pytest.mark.asyncio
    async def test_list_compliance_flags_success(self, compliance_service):
        """Test listing compliance flags successfully"""
        # Mock database results
        mock_flag = MagicMock()
        mock_flag.id = "flag_123"
        mock_flag.entity_type = "transaction"
        mock_flag.entity_id = "tx_123"
        mock_flag.network = "stellar"
        mock_flag.flag_type = "aml"
        mock_flag.flag_severity = "high"
        mock_flag.flag_status = "active"
        mock_flag.flag_reason = "Suspicious activity"
        mock_flag.risk_score = Decimal("85.5")
        mock_flag.country_code = "NG"
        mock_flag.region = "west_africa"
        mock_flag.resolved_by = None
        mock_flag.resolution_notes = None
        mock_flag.created_at = datetime.now()
        mock_flag.updated_at = datetime.now()
        mock_flag.resolved_at = None
        
        # Mock count result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Mock main query result
        mock_main_result = MagicMock()
        mock_main_result.scalars.return_value.all.return_value = [mock_flag]
        
        # Set up side effect for multiple calls
        compliance_service.db.execute = AsyncMock(side_effect=[mock_count_result, mock_main_result])
        
        result = await compliance_service.list_compliance_flags()
        
        assert result["success"] is True
        assert len(result["flags"]) == 1
        assert result["flags"][0]["id"] == "flag_123"
        assert result["flags"][0]["flag_type"] == "aml"
        assert result["flags"][0]["flag_severity"] == "high"
        assert result["pagination"]["total"] == 1
    
    @pytest.mark.asyncio
    async def test_list_compliance_flags_with_filters(self, compliance_service):
        """Test listing compliance flags with filters"""
        # Mock database results
        mock_flag = MagicMock()
        mock_flag.id = "flag_123"
        mock_flag.entity_type = "transaction"
        mock_flag.entity_id = "tx_123"
        mock_flag.network = "stellar"
        mock_flag.flag_type = "aml"
        mock_flag.flag_severity = "high"
        mock_flag.flag_status = "active"
        mock_flag.flag_reason = "Suspicious activity"
        mock_flag.risk_score = Decimal("85.5")
        mock_flag.country_code = "NG"
        mock_flag.region = "west_africa"
        mock_flag.resolved_by = None
        mock_flag.resolution_notes = None
        mock_flag.created_at = datetime.now()
        mock_flag.updated_at = datetime.now()
        mock_flag.resolved_at = None
        
        # Mock count result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Mock main query result
        mock_main_result = MagicMock()
        mock_main_result.scalars.return_value.all.return_value = [mock_flag]
        
        # Set up side effect for multiple calls
        compliance_service.db.execute = AsyncMock(side_effect=[mock_count_result, mock_main_result])
        
        result = await compliance_service.list_compliance_flags(
            entity_type="transaction",
            flag_type="aml",
            flag_severity="high",
            network="stellar"
        )
        
        assert result["success"] is True
        assert len(result["flags"]) == 1
        assert result["filters"]["entity_type"] == "transaction"
        assert result["filters"]["flag_type"] == "aml"
        assert result["filters"]["flag_severity"] == "high"
        assert result["filters"]["network"] == "stellar"
    
    @pytest.mark.asyncio
    async def test_list_compliance_flags_pagination(self, compliance_service):
        """Test listing compliance flags with pagination"""
        # Mock database results
        mock_flags = []
        for i in range(3):
            mock_flag = MagicMock()
            mock_flag.id = f"flag_{i}"
            mock_flag.entity_type = "transaction"
            mock_flag.entity_id = f"tx_{i}"
            mock_flag.network = "stellar"
            mock_flag.flag_type = "aml"
            mock_flag.flag_severity = "high"
            mock_flag.flag_status = "active"
            mock_flag.flag_reason = "Suspicious activity"
            mock_flag.risk_score = Decimal("85.5")
            mock_flag.country_code = "NG"
            mock_flag.region = "west_africa"
            mock_flag.resolved_by = None
            mock_flag.resolution_notes = None
            mock_flag.created_at = datetime.now()
            mock_flag.updated_at = datetime.now()
            mock_flag.resolved_at = None
            mock_flags.append(mock_flag)
        
        # Mock count result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 10  # Total count
        
        # Mock main query result
        mock_main_result = MagicMock()
        mock_main_result.scalars.return_value.all.return_value = mock_flags
        
        # Set up side effect for multiple calls
        compliance_service.db.execute = AsyncMock(side_effect=[mock_count_result, mock_main_result])
        
        result = await compliance_service.list_compliance_flags(limit=3, offset=0)
        
        assert result["success"] is True
        assert len(result["flags"]) == 3
        assert result["pagination"]["total"] == 10
        assert result["pagination"]["limit"] == 3
        assert result["pagination"]["offset"] == 0
        assert result["pagination"]["has_more"] is True
    
    @pytest.mark.asyncio
    async def test_list_compliance_flags_sorting(self, compliance_service):
        """Test listing compliance flags with sorting"""
        # Mock database results
        mock_flag = MagicMock()
        mock_flag.id = "flag_123"
        mock_flag.entity_type = "transaction"
        mock_flag.entity_id = "tx_123"
        mock_flag.network = "stellar"
        mock_flag.flag_type = "aml"
        mock_flag.flag_severity = "high"
        mock_flag.flag_status = "active"
        mock_flag.flag_reason = "Suspicious activity"
        mock_flag.risk_score = Decimal("85.5")
        mock_flag.country_code = "NG"
        mock_flag.region = "west_africa"
        mock_flag.resolved_by = None
        mock_flag.resolution_notes = None
        mock_flag.created_at = datetime.now()
        mock_flag.updated_at = datetime.now()
        mock_flag.resolved_at = None
        
        # Mock count result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Mock main query result
        mock_main_result = MagicMock()
        mock_main_result.scalars.return_value.all.return_value = [mock_flag]
        
        # Set up side effect for multiple calls
        compliance_service.db.execute = AsyncMock(side_effect=[mock_count_result, mock_main_result])
        
        result = await compliance_service.list_compliance_flags(
            sort_by="risk_score",
            sort_order="desc"
        )
        
        assert result["success"] is True
        assert result["sorting"]["sort_by"] == "risk_score"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_list_compliance_flags_database_error(self, compliance_service):
        """Test listing compliance flags with database error"""
        compliance_service.db.execute = AsyncMock(side_effect=Exception("Database error"))
        
        result = await compliance_service.list_compliance_flags()
        
        assert result["success"] is False
        assert "Failed to list compliance flags" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_flag_details_success(self, compliance_service):
        """Test getting flag details successfully"""
        flag_id = "flag_123"
        
        # Mock flag result
        mock_flag = MagicMock()
        mock_flag.id = flag_id
        mock_flag.entity_type = "transaction"
        mock_flag.entity_id = "tx_123"
        mock_flag.network = "stellar"
        mock_flag.flag_type = "aml"
        mock_flag.flag_severity = "high"
        mock_flag.flag_status = "active"
        mock_flag.flag_reason = "Suspicious activity"
        mock_flag.risk_score = Decimal("85.5")
        mock_flag.country_code = "NG"
        mock_flag.region = "west_africa"
        mock_flag.resolved_by = None
        mock_flag.resolution_notes = None
        mock_flag.created_at = datetime.now()
        mock_flag.updated_at = datetime.now()
        mock_flag.resolved_at = None
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_flag
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        
        result = await compliance_service.get_flag_details(flag_id)
        
        assert result["success"] is True
        assert result["flag"]["id"] == flag_id
        assert result["flag"]["flag_type"] == "aml"
        assert result["flag"]["flag_severity"] == "high"
        assert "history" in result
        assert "entity_info" in result
    
    @pytest.mark.asyncio
    async def test_get_flag_details_not_found(self, compliance_service):
        """Test getting flag details when flag not found"""
        flag_id = "nonexistent_flag"
        
        # Mock database result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        
        result = await compliance_service.get_flag_details(flag_id)
        
        assert result["success"] is False
        assert "Flag not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_update_flag_status_success(self, compliance_service):
        """Test updating flag status successfully"""
        flag_id = "flag_123"
        new_status = "resolved"
        resolved_by = "compliance_officer"
        resolution_notes = "False positive"
        
        # Mock flag result
        mock_flag = MagicMock()
        mock_flag.id = flag_id
        mock_flag.flag_status = "active"
        mock_flag.updated_at = datetime.now()
        mock_flag.resolved_at = None
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_flag
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        compliance_service.db.commit = AsyncMock()
        compliance_service.db.refresh = AsyncMock()
        
        result = await compliance_service.update_flag_status(
            flag_id=flag_id,
            new_status=new_status,
            resolved_by=resolved_by,
            resolution_notes=resolution_notes
        )
        
        assert result["success"] is True
        assert result["flag_id"] == flag_id
        assert result["new_status"] == new_status
        assert "updated_at" in result
        assert "resolved_at" in result
        
        # Verify database operations were called
        compliance_service.db.commit.assert_called_once()
        compliance_service.db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update_flag_status_not_found(self, compliance_service):
        """Test updating flag status when flag not found"""
        flag_id = "nonexistent_flag"
        
        # Mock database result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        
        result = await compliance_service.update_flag_status(
            flag_id=flag_id,
            new_status="resolved"
        )
        
        assert result["success"] is False
        assert "Flag not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_update_flag_status_database_error(self, compliance_service):
        """Test updating flag status with database error"""
        flag_id = "flag_123"
        
        # Mock flag result
        mock_flag = MagicMock()
        mock_flag.id = flag_id
        mock_flag.flag_status = "active"
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_flag
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        compliance_service.db.commit = AsyncMock(side_effect=Exception("Database error"))
        compliance_service.db.rollback = AsyncMock()
        
        result = await compliance_service.update_flag_status(
            flag_id=flag_id,
            new_status="resolved"
        )
        
        assert result["success"] is False
        assert "Failed to update flag status" in result["error"]
        compliance_service.db.rollback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_flag_analytics_success(self, compliance_service):
        """Test getting flag analytics successfully"""
        # Mock flags for analytics
        mock_flags = []
        for i in range(5):
            mock_flag = MagicMock()
            mock_flag.flag_status = "active" if i < 3 else "resolved"
            mock_flag.flag_severity = "high" if i < 2 else "medium"
            mock_flag.flag_type = "aml" if i < 3 else "kyc"
            mock_flag.network = "stellar" if i < 3 else "hedera"
            mock_flag.country_code = "NG" if i < 3 else "KE"
            mock_flag.risk_score = Decimal("85.5")
            mock_flags.append(mock_flag)
        
        # Mock database result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_flags
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        
        result = await compliance_service.get_flag_analytics()
        
        assert result["success"] is True
        assert result["summary"]["total_flags"] == 5
        assert result["summary"]["active_flags"] == 3
        assert result["summary"]["resolved_flags"] == 2
        assert result["severity_breakdown"]["high"] == 2
        assert result["severity_breakdown"]["medium"] == 3
        assert result["type_breakdown"]["aml"] == 3
        assert result["type_breakdown"]["kyc"] == 2
        assert result["network_breakdown"]["stellar"] == 3
        assert result["network_breakdown"]["hedera"] == 2
        assert len(result["top_countries"]) == 2
    
    @pytest.mark.asyncio
    async def test_get_flag_analytics_with_filters(self, compliance_service):
        """Test getting flag analytics with date and network filters"""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        # Mock flags for analytics
        mock_flags = []
        for i in range(3):
            mock_flag = MagicMock()
            mock_flag.flag_status = "active"
            mock_flag.flag_severity = "high"
            mock_flag.flag_type = "aml"
            mock_flag.network = "stellar"
            mock_flag.country_code = "NG"
            mock_flag.risk_score = Decimal("85.5")
            mock_flags.append(mock_flag)
        
        # Mock database result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_flags
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        
        result = await compliance_service.get_flag_analytics(
            start_date=start_date,
            end_date=end_date,
            network="stellar"
        )
        
        assert result["success"] is True
        assert result["summary"]["total_flags"] == 3
        assert result["period"]["start_date"] == start_date.isoformat()
        assert result["period"]["end_date"] == end_date.isoformat()
    
    @pytest.mark.asyncio
    async def test_get_flag_analytics_database_error(self, compliance_service):
        """Test getting flag analytics with database error"""
        compliance_service.db.execute = AsyncMock(side_effect=Exception("Database error"))
        
        result = await compliance_service.get_flag_analytics()
        
        assert result["success"] is False
        assert "Failed to get flag analytics" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_flag_history(self, compliance_service):
        """Test getting flag history"""
        flag_id = "flag_123"
        
        result = await compliance_service._get_flag_history(flag_id)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["action"] == "created"
        assert "timestamp" in result[0]
        assert result[0]["user"] == "system"
    
    @pytest.mark.asyncio
    async def test_get_entity_info(self, compliance_service):
        """Test getting entity information"""
        entity_type = "transaction"
        entity_id = "tx_123"
        
        result = await compliance_service._get_entity_info(entity_type, entity_id)
        
        assert result["entity_type"] == entity_type
        assert result["entity_id"] == entity_id
        assert result["entity_name"] == f"{entity_type}_{entity_id}"
        assert "last_activity" in result
    
    @pytest.mark.asyncio
    async def test_flag_transaction_success(self, compliance_service, sample_flag_data):
        """Test flagging transaction successfully"""
        # Mock database operations
        compliance_service.db.add = MagicMock()
        compliance_service.db.commit = AsyncMock()
        compliance_service.db.refresh = AsyncMock()
        
        result = await compliance_service.flag_transaction(sample_flag_data)
        
        assert result["success"] is True
        assert "flag_id" in result
        assert result["flag_status"] == "active"
        assert "created_at" in result
        
        # Verify database operations were called
        compliance_service.db.add.assert_called_once()
        compliance_service.db.commit.assert_called_once()
        compliance_service.db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_flag_transaction_database_error(self, compliance_service, sample_flag_data):
        """Test flagging transaction with database error"""
        # Mock database operations
        compliance_service.db.add = MagicMock()
        compliance_service.db.commit = AsyncMock(side_effect=Exception("Database error"))
        compliance_service.db.rollback = AsyncMock()
        
        result = await compliance_service.flag_transaction(sample_flag_data)
        
        assert result["success"] is False
        assert "Failed to flag transaction" in result["error"]
        compliance_service.db.rollback.assert_called_once()
