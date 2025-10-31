"""
Unit tests for ComplianceService
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
def sample_verification_data():
    """Sample verification data for testing"""
    return {
        "account_id": "test_account_123",
        "network": "stellar",
        "verification_type": "individual",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "nationality": "NG",
        "document_type": "bvn",
        "document_number": "12345678901",
        "document_country": "NG",
        "bvn": "12345678901",
        "nin": "98765432109",
        "sa_id_number": "1234567890123",
        "ghana_card": "GHA-123456789-1"
    }


class TestComplianceService:
    """Test cases for ComplianceService"""
    
    @pytest.mark.asyncio
    async def test_verify_id_success(self, compliance_service, sample_verification_data):
        """Test successful KYC verification"""
        # Mock database operations
        compliance_service.db.add = MagicMock()
        compliance_service.db.commit = AsyncMock()
        compliance_service.db.refresh = AsyncMock()
        
        result = await compliance_service.verify_id(sample_verification_data)
        
        assert result["success"] is True
        assert "verification_id" in result
        assert result["verification_status"] in ["verified", "pending", "rejected"]
        assert "risk_score" in result
        assert "risk_level" in result
        assert "verification_notes" in result
        assert "expires_at" in result
        
        # Verify database operations were called
        compliance_service.db.add.assert_called_once()
        compliance_service.db.commit.assert_called_once()
        compliance_service.db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_verify_id_invalid_bvn_format(self, compliance_service, sample_verification_data):
        """Test KYC verification with invalid BVN format"""
        sample_verification_data["bvn"] = "123"  # Invalid BVN (too short)
        
        result = await compliance_service.verify_id(sample_verification_data)
        
        assert result["success"] is False
        assert "Invalid ID format" in result["error"]
        assert "BVN must be exactly 11 digits" in result["details"]
    
    @pytest.mark.asyncio
    async def test_verify_id_invalid_nin_format(self, compliance_service, sample_verification_data):
        """Test KYC verification with invalid NIN format"""
        sample_verification_data["nin"] = "123abc"  # Invalid NIN (contains letters)
        
        result = await compliance_service.verify_id(sample_verification_data)
        
        assert result["success"] is False
        assert "Invalid ID format" in result["error"]
        assert "NIN must be exactly 11 digits" in result["details"]
    
    @pytest.mark.asyncio
    async def test_verify_id_invalid_sa_id_format(self, compliance_service, sample_verification_data):
        """Test KYC verification with invalid SA ID format"""
        sample_verification_data["sa_id_number"] = "123"  # Invalid SA ID (too short)
        
        result = await compliance_service.verify_id(sample_verification_data)
        
        assert result["success"] is False
        assert "Invalid ID format" in result["error"]
        assert "SA ID must be exactly 13 digits" in result["details"]
    
    @pytest.mark.asyncio
    async def test_verify_id_invalid_ghana_card_format(self, compliance_service, sample_verification_data):
        """Test KYC verification with invalid Ghana Card format"""
        sample_verification_data["ghana_card"] = "INVALID"  # Invalid Ghana Card format
        
        result = await compliance_service.verify_id(sample_verification_data)
        
        assert result["success"] is False
        assert "Invalid ID format" in result["error"]
        assert "Ghana Card must be in format GHA-XXXXXXXXX-X" in result["details"]
    
    @pytest.mark.asyncio
    async def test_verify_id_sanctions_hit(self, compliance_service, sample_verification_data):
        """Test KYC verification with sanctions hit"""
        sample_verification_data["first_name"] = "john"  # Mock sanctions hit
        
        # Mock database operations
        compliance_service.db.add = MagicMock()
        compliance_service.db.commit = AsyncMock()
        compliance_service.db.refresh = AsyncMock()
        
        result = await compliance_service.verify_id(sample_verification_data)
        
        assert result["success"] is True
        assert result["risk_score"] >= 50.0  # Should be high due to sanctions hit
        assert result["risk_level"] == "high"
        assert result["verification_status"] == "rejected"
    
    @pytest.mark.asyncio
    async def test_verify_id_database_error(self, compliance_service, sample_verification_data):
        """Test KYC verification with database error"""
        compliance_service.db.add = MagicMock()
        compliance_service.db.commit = AsyncMock(side_effect=Exception("Database error"))
        compliance_service.db.rollback = AsyncMock()
        
        result = await compliance_service.verify_id(sample_verification_data)
        
        assert result["success"] is False
        assert "KYC verification failed" in result["error"]
        compliance_service.db.rollback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_validate_id_formats_bvn_valid(self, compliance_service):
        """Test BVN validation with valid format"""
        verification_data = {"bvn": "12345678901"}
        
        result = await compliance_service._validate_id_formats(verification_data)
        
        assert result["valid"] is True
        assert result["status"] == "valid"
        assert result["validation_results"]["bvn"] == "valid"
    
    @pytest.mark.asyncio
    async def test_validate_id_formats_nin_valid(self, compliance_service):
        """Test NIN validation with valid format"""
        verification_data = {"nin": "98765432109"}
        
        result = await compliance_service._validate_id_formats(verification_data)
        
        assert result["valid"] is True
        assert result["status"] == "valid"
        assert result["validation_results"]["nin"] == "valid"
    
    @pytest.mark.asyncio
    async def test_validate_id_formats_sa_id_valid(self, compliance_service):
        """Test SA ID validation with valid format"""
        verification_data = {"sa_id_number": "1234567890123"}
        
        result = await compliance_service._validate_id_formats(verification_data)
        
        assert result["valid"] is True
        assert result["status"] == "valid"
        assert result["validation_results"]["sa_id_number"] == "valid"
    
    @pytest.mark.asyncio
    async def test_validate_id_formats_ghana_card_valid(self, compliance_service):
        """Test Ghana Card validation with valid format"""
        verification_data = {"ghana_card": "GHA-123456789-1"}
        
        result = await compliance_service._validate_id_formats(verification_data)
        
        assert result["valid"] is True
        assert result["status"] == "valid"
        assert result["validation_results"]["ghana_card"] == "valid"
    
    @pytest.mark.asyncio
    async def test_validate_id_formats_generic_document_valid(self, compliance_service):
        """Test generic document validation with valid format"""
        verification_data = {"document_number": "DOC123456789"}
        
        result = await compliance_service._validate_id_formats(verification_data)
        
        assert result["valid"] is True
        assert result["status"] == "valid"
        assert result["validation_results"]["document_number"] == "valid"
    
    @pytest.mark.asyncio
    async def test_validate_id_formats_generic_document_invalid(self, compliance_service):
        """Test generic document validation with invalid format"""
        verification_data = {"document_number": "123"}  # Too short
        
        result = await compliance_service._validate_id_formats(verification_data)
        
        assert result["valid"] is False
        assert result["status"] == "invalid"
        assert "Document number must be between 5 and 20 characters" in result["errors"]
    
    @pytest.mark.asyncio
    async def test_check_sanctions_lists_clear(self, compliance_service):
        """Test sanctions check with clear result"""
        verification_data = {"first_name": "Alice", "last_name": "Smith"}
        
        result = await compliance_service._check_sanctions_lists(verification_data)
        
        assert result["hit"] is False
        assert result["status"] == "clear"
        assert len(result["details"]) == 0
    
    @pytest.mark.asyncio
    async def test_check_sanctions_lists_hit(self, compliance_service):
        """Test sanctions check with hit"""
        verification_data = {"first_name": "john", "last_name": "doe"}
        
        result = await compliance_service._check_sanctions_lists(verification_data)
        
        assert result["hit"] is True
        assert result["status"] == "flagged"
        assert len(result["details"]) > 0
    
    @pytest.mark.asyncio
    async def test_calculate_risk_score_low_risk(self, compliance_service):
        """Test risk score calculation for low risk case"""
        verification_data = {
            "document_type": "bvn",
            "document_country": "NG",
            "date_of_birth": "1990-01-01"
        }
        sanctions_result = {"hit": False}
        
        result = await compliance_service._calculate_risk_score(verification_data, sanctions_result)
        
        assert 0.0 <= result <= 100.0
        assert result < 40.0  # Should be low risk
    
    @pytest.mark.asyncio
    async def test_calculate_risk_score_high_risk(self, compliance_service):
        """Test risk score calculation for high risk case"""
        verification_data = {
            "document_type": "passport",
            "document_country": "XX",  # High risk country
            "date_of_birth": "2010-01-01"  # Under 18
        }
        sanctions_result = {"hit": True}
        
        result = await compliance_service._calculate_risk_score(verification_data, sanctions_result)
        
        assert 0.0 <= result <= 100.0
        assert result >= 70.0  # Should be high risk
    
    def test_determine_verification_status_verified(self, compliance_service):
        """Test verification status determination for verified case"""
        risk_score = 30.0
        validation_result = {"valid": True}
        
        result = compliance_service._determine_verification_status(risk_score, validation_result)
        
        assert result == "verified"
    
    def test_determine_verification_status_pending(self, compliance_service):
        """Test verification status determination for pending case"""
        risk_score = 50.0
        validation_result = {"valid": True}
        
        result = compliance_service._determine_verification_status(risk_score, validation_result)
        
        assert result == "pending"
    
    def test_determine_verification_status_rejected_high_risk(self, compliance_service):
        """Test verification status determination for rejected high risk case"""
        risk_score = 80.0
        validation_result = {"valid": True}
        
        result = compliance_service._determine_verification_status(risk_score, validation_result)
        
        assert result == "rejected"
    
    def test_determine_verification_status_rejected_invalid(self, compliance_service):
        """Test verification status determination for rejected invalid case"""
        risk_score = 30.0
        validation_result = {"valid": False}
        
        result = compliance_service._determine_verification_status(risk_score, validation_result)
        
        assert result == "rejected"
    
    def test_get_risk_level_low(self, compliance_service):
        """Test risk level determination for low risk"""
        result = compliance_service._get_risk_level(30.0)
        assert result == "low"
    
    def test_get_risk_level_medium(self, compliance_service):
        """Test risk level determination for medium risk"""
        result = compliance_service._get_risk_level(50.0)
        assert result == "medium"
    
    def test_get_risk_level_high(self, compliance_service):
        """Test risk level determination for high risk"""
        result = compliance_service._get_risk_level(80.0)
        assert result == "high"
    
    @pytest.mark.asyncio
    async def test_get_verification_status_success(self, compliance_service):
        """Test getting verification status successfully"""
        verification_id = "KYC_123456789ABC"
        
        # Mock database result
        mock_kyc_record = MagicMock()
        mock_kyc_record.verification_id = verification_id
        mock_kyc_record.verification_status = "verified"
        mock_kyc_record.verification_score = Decimal("25.5")
        mock_kyc_record.risk_level = "low"
        mock_kyc_record.verification_notes = "Test notes"
        mock_kyc_record.created_at = datetime.now()
        mock_kyc_record.updated_at = datetime.now()
        mock_kyc_record.verified_at = datetime.now()
        mock_kyc_record.expires_at = datetime.now() + timedelta(days=365)
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_kyc_record
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        
        result = await compliance_service.get_verification_status(verification_id)
        
        assert result["success"] is True
        assert result["verification_id"] == verification_id
        assert result["verification_status"] == "verified"
        assert result["risk_score"] == 25.5
        assert result["risk_level"] == "low"
    
    @pytest.mark.asyncio
    async def test_get_verification_status_not_found(self, compliance_service):
        """Test getting verification status when not found"""
        verification_id = "KYC_NONEXISTENT"
        
        # Mock database result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        compliance_service.db.execute = AsyncMock(return_value=mock_result)
        
        result = await compliance_service.get_verification_status(verification_id)
        
        assert result["success"] is False
        assert "Verification not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_list_verifications_success(self, compliance_service):
        """Test listing verifications successfully"""
        # Mock database results
        mock_verification = MagicMock()
        mock_verification.id = "test_id"
        mock_verification.verification_id = "KYC_123"
        mock_verification.account_id = "account_123"
        mock_verification.network = "stellar"
        mock_verification.verification_type = "individual"
        mock_verification.verification_status = "verified"
        mock_verification.verification_score = Decimal("25.0")
        mock_verification.risk_level = "low"
        mock_verification.created_at = datetime.now()
        mock_verification.updated_at = datetime.now()
        mock_verification.verified_at = datetime.now()
        mock_verification.expires_at = datetime.now() + timedelta(days=365)
        
        # Mock count result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Mock main query result
        mock_main_result = MagicMock()
        mock_main_result.scalars.return_value.all.return_value = [mock_verification]
        
        # Set up side effect for multiple calls
        compliance_service.db.execute = AsyncMock(side_effect=[mock_count_result, mock_main_result])
        
        result = await compliance_service.list_verifications()
        
        assert result["success"] is True
        assert len(result["verifications"]) == 1
        assert result["verifications"][0]["verification_id"] == "KYC_123"
        assert result["pagination"]["total"] == 1
    
    @pytest.mark.asyncio
    async def test_list_verifications_with_filters(self, compliance_service):
        """Test listing verifications with filters"""
        # Mock database results
        mock_verification = MagicMock()
        mock_verification.id = "test_id"
        mock_verification.verification_id = "KYC_123"
        mock_verification.account_id = "account_123"
        mock_verification.network = "stellar"
        mock_verification.verification_type = "individual"
        mock_verification.verification_status = "verified"
        mock_verification.verification_score = Decimal("25.0")
        mock_verification.risk_level = "low"
        mock_verification.created_at = datetime.now()
        mock_verification.updated_at = datetime.now()
        mock_verification.verified_at = datetime.now()
        mock_verification.expires_at = datetime.now() + timedelta(days=365)
        
        # Mock count result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Mock main query result
        mock_main_result = MagicMock()
        mock_main_result.scalars.return_value.all.return_value = [mock_verification]
        
        # Set up side effect for multiple calls
        compliance_service.db.execute = AsyncMock(side_effect=[mock_count_result, mock_main_result])
        
        result = await compliance_service.list_verifications(
            account_id="account_123",
            verification_status="verified",
            network="stellar"
        )
        
        assert result["success"] is True
        assert len(result["verifications"]) == 1
    
    @pytest.mark.asyncio
    async def test_flag_transaction_success(self, compliance_service):
        """Test flagging transaction successfully"""
        flag_data = {
            "entity_type": "transaction",
            "entity_id": "tx_123",
            "network": "stellar",
            "flag_type": "aml",
            "flag_severity": "high",
            "flag_reason": "Suspicious activity",
            "country_code": "NG",
            "region": "west_africa"
        }
        
        # Mock database operations
        compliance_service.db.add = MagicMock()
        compliance_service.db.commit = AsyncMock()
        compliance_service.db.refresh = AsyncMock()
        
        result = await compliance_service.flag_transaction(flag_data)
        
        assert result["success"] is True
        assert "flag_id" in result
        assert result["flag_status"] == "active"
        assert "created_at" in result
        
        # Verify database operations were called
        compliance_service.db.add.assert_called_once()
        compliance_service.db.commit.assert_called_once()
        compliance_service.db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_flag_transaction_database_error(self, compliance_service):
        """Test flagging transaction with database error"""
        flag_data = {
            "entity_type": "transaction",
            "entity_id": "tx_123",
            "network": "stellar",
            "flag_type": "aml",
            "flag_severity": "high",
            "flag_reason": "Suspicious activity"
        }
        
        # Mock database operations
        compliance_service.db.add = MagicMock()
        compliance_service.db.commit = AsyncMock(side_effect=Exception("Database error"))
        compliance_service.db.rollback = AsyncMock()
        
        result = await compliance_service.flag_transaction(flag_data)
        
        assert result["success"] is False
        assert "Failed to flag transaction" in result["error"]
        compliance_service.db.rollback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_compliance_reports(self, compliance_service):
        """Test getting compliance reports"""
        result = await compliance_service.get_compliance_reports()
        
        assert result == []
