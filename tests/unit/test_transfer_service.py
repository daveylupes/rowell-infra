"""
Unit tests for TransferService
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from api.services.transfer_service import TransferService
from api.models.transaction import Transaction


def create_mock_transaction(**kwargs):
    """Helper function to create mock transaction with default values"""
    defaults = {
        "id": 1,
        "transaction_hash": "mock_stellar_tx_123456",
        "from_account": "GABC1234567890",
        "to_account": "GXYZ0987654321",
        "asset_code": "XLM",
        "amount": "10.0",
        "network": "stellar",
        "environment": "testnet",
        "status": "pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "ledger_time": None
    }
    defaults.update(kwargs)
    return Transaction(**defaults)


class TestTransferService:
    """Test cases for TransferService"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        return AsyncMock(spec=AsyncSession)
    
    @pytest.fixture
    def transfer_service(self, mock_db_session):
        """Transfer service instance with mocked database"""
        return TransferService(mock_db_session)
    
    @pytest.mark.asyncio
    async def test_create_transfer_stellar_success(self, transfer_service, mock_db_session):
        """Test successful Stellar transfer creation"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock the Stellar service
        with patch('api.services.transfer_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_service.return_value = mock_stellar_instance
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "XLM", "balance": "100.0", "asset_issuer": None}
            ]
            
            # Mock database operations
            mock_transaction = create_mock_transaction()
            mock_db_session.add.return_value = None
            mock_db_session.commit.return_value = None
            mock_db_session.refresh.return_value = None
            
            # Test transfer creation
            result = await transfer_service.create_transfer(
                from_account="GABC1234567890",
                to_account="GXYZ0987654321",
                asset_code="XLM",
                amount="10.0",
                network="stellar",
                environment="testnet",
                from_country="NG",
                to_country="KE",
                api_key="test_api_key"
            )
            
            # Assertions
            assert result["transaction_hash"].startswith("mock_stellar_tx_")
            assert result["from_account"] == "GABC1234567890"
            assert result["to_account"] == "GXYZ0987654321"
            assert result["asset_code"] == "XLM"
            assert result["amount"] == "10.0"
            assert result["network"] == "stellar"
            assert result["status"] == "pending"
            
            # Verify database operations
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_transfer_hedera_mock(self, transfer_service, mock_db_session):
        """Test Hedera transfer creation (mock response)"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="0.0.123456",
            network="hedera",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Hedera service
        with patch('api.services.hedera_service.HederaService') as mock_hedera_service:
            mock_hedera_instance = AsyncMock()
            mock_hedera_service.return_value = mock_hedera_instance
            mock_hedera_instance.get_account_balances.return_value = [
                {"asset_code": "HBAR", "balance": "100.0", "asset_issuer": None}
            ]
            
            # Mock database operations
            from datetime import datetime
            mock_transaction = Transaction(
                id=1,
                transaction_hash="mock_hedera_tx_123456",
                from_account="0.0.123456",
                to_account="0.0.789012",
                asset_code="HBAR",
                amount="10.0",
                network="hedera",
                environment="testnet",
                status="pending",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                ledger_time=None
            )
            mock_db_session.add.return_value = None
            mock_db_session.commit.return_value = None
            # Mock refresh to set the transaction object with proper values
            def mock_refresh(transaction):
                transaction.id = 1
                transaction.created_at = datetime.now()
                transaction.updated_at = datetime.now()
                transaction.ledger_time = None
            mock_db_session.refresh.side_effect = mock_refresh
            
            result = await transfer_service.create_transfer(
                from_account="0.0.123456",
                to_account="0.0.789012",
                asset_code="HBAR",
                amount="10.0",
                network="hedera",
                environment="testnet",
                api_key="test_api_key"
            )
        
        # Assertions for mock Hedera response
        assert result["network"] == "hedera"
        assert result["environment"] == "testnet"
        assert result["status"] == "pending"
        assert result["transaction_hash"].startswith("mock_hedera_tx_")
    
    @pytest.mark.asyncio
    async def test_create_transfer_invalid_network(self, transfer_service, mock_db_session):
        """Test transfer creation with invalid network"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        with pytest.raises(ValueError, match="Unsupported network"):
            await transfer_service.create_transfer(
                from_account="GABC1234567890",
                to_account="GXYZ0987654321",
                asset_code="XLM",
                amount="10.0",
                network="bitcoin",
                environment="testnet",
                api_key="test_api_key"
            )
    
    @pytest.mark.asyncio
    async def test_create_transfer_database_error(self, transfer_service, mock_db_session):
        """Test transfer creation with database error"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service
        with patch('api.services.transfer_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_service.return_value = mock_stellar_instance
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "XLM", "balance": "100.0", "asset_issuer": None}
            ]
            
            # Mock database error
            mock_db_session.commit.side_effect = Exception("Database error")
            mock_db_session.rollback.return_value = None
            
            # Test that exception is raised and rollback is called
            with pytest.raises(Exception, match="Database error"):
                await transfer_service.create_transfer(
                    from_account="GABC1234567890",
                    to_account="GXYZ0987654321",
                    asset_code="XLM",
                    amount="10.0",
                    network="stellar",
                    environment="testnet",
                    api_key="test_api_key"
                )
            
            mock_db_session.rollback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_transfer_success(self, transfer_service, mock_db_session):
        """Test getting transfer by ID"""
        # Mock database query result
        mock_transaction = create_mock_transaction()
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_transaction
        mock_db_session.execute.return_value = mock_result
        
        # Test getting transfer
        result = await transfer_service.get_transfer("1")
        
        # Assertions
        assert result is not None
        assert result["id"] == "1"
        assert result["transaction_hash"] == "mock_stellar_tx_123456"
        assert result["from_account"] == "GABC1234567890"
        assert result["to_account"] == "GXYZ0987654321"
        assert result["asset_code"] == "XLM"
        assert result["amount"] == "10.0"
    
    @pytest.mark.asyncio
    async def test_get_transfer_not_found(self, transfer_service, mock_db_session):
        """Test getting non-existent transfer"""
        # Mock database query result (no transaction found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test getting non-existent transfer
        result = await transfer_service.get_transfer("999")
        
        # Assertions
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_transfer_by_hash_success(self, transfer_service, mock_db_session):
        """Test getting transfer by transaction hash"""
        # Mock database query result
        mock_transaction = create_mock_transaction()
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_transaction
        mock_db_session.execute.return_value = mock_result
        
        # Test getting transfer by hash
        result = await transfer_service.get_transfer_by_hash("mock_stellar_tx_123456")
        
        # Assertions
        assert result is not None
        assert result["transaction_hash"] == "mock_stellar_tx_123456"
        assert result["from_account"] == "GABC1234567890"
        assert result["to_account"] == "GXYZ0987654321"
    
    @pytest.mark.asyncio
    async def test_list_transfers_with_filters(self, transfer_service, mock_db_session):
        """Test listing transfers with filters"""
        # Mock database query result
        mock_transactions = [
            create_mock_transaction(
                id=1,
                transaction_hash="mock_stellar_tx_123456",
                from_country="NG",
                to_country="KE"
            ),
            create_mock_transaction(
                id=2,
                transaction_hash="mock_stellar_tx_789012",
                to_account="GDEF3456789012",
                asset_code="USDC",
                amount="50.0",
                status="success",
                from_country="NG",
                to_country="GH"
            )
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 2
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Test listing transfers with filters
        result = await transfer_service.list_transfers(
            from_account="GABC1234567890",
            network="stellar",
            status="pending",
            limit=10
        )
        
        # Assertions
        assert "transfers" in result
        assert len(result["transfers"]) == 2
        assert result["transfers"][0]["from_account"] == "GABC1234567890"
        assert result["transfers"][0]["network"] == "stellar"
        assert result["transfers"][1]["from_account"] == "GABC1234567890"
        assert result["transfers"][1]["network"] == "stellar"
        
        # Verify pagination and filters
        assert result["pagination"]["total"] == 2
        assert result["filters"]["from_account"] == "GABC1234567890"
        assert result["filters"]["network"] == "stellar"
        assert result["filters"]["status"] == "pending"
    
    @pytest.mark.asyncio
    async def test_list_transfers_pagination(self, transfer_service, mock_db_session):
        """Test listing transfers with pagination"""
        # Mock database query result
        mock_transactions = [
            create_mock_transaction()
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        mock_db_session.execute.return_value = mock_result
        
        # Test listing transfers with pagination
        result = await transfer_service.list_transfers(
            skip=10,
            limit=5
        )
        
        # Assertions
        assert len(result) == 1
        assert result[0]["transaction_hash"] == "mock_stellar_tx_123456"
    
    @pytest.mark.asyncio
    async def test_list_transfers_empty_result(self, transfer_service, mock_db_session):
        """Test listing transfers with empty result"""
        # Mock database query result (no transactions)
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute.return_value = mock_result
        
        # Test listing transfers
        result = await transfer_service.list_transfers()
        
        # Assertions
        assert len(result) == 0
        assert result == []
    
    @pytest.mark.asyncio
    async def test_validate_account_ownership_success(self, transfer_service, mock_db_session):
        """Test successful account ownership validation"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Test account ownership validation
        await transfer_service._validate_account_ownership("GABC1234567890", "test_api_key")
        
        # Verify database query was made
        mock_db_session.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_validate_account_ownership_account_not_found(self, transfer_service, mock_db_session):
        """Test account ownership validation with non-existent account"""
        # Mock database query result (no account found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test that exception is raised
        with pytest.raises(ValueError, match="Account not found"):
            await transfer_service._validate_account_ownership("GINVALID123", "test_api_key")
    
    @pytest.mark.asyncio
    async def test_validate_account_ownership_no_api_key(self, transfer_service, mock_db_session):
        """Test account ownership validation without API key"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Test that exception is raised
        with pytest.raises(ValueError, match="API key is required"):
            await transfer_service._validate_account_ownership("GABC1234567890", None)
    
    @pytest.mark.asyncio
    async def test_validate_account_ownership_inactive_account(self, transfer_service, mock_db_session):
        """Test account ownership validation with inactive account"""
        # Mock inactive account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=False
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Test that exception is raised
        with pytest.raises(ValueError, match="Account GABC1234567890 is not active"):
            await transfer_service._validate_account_ownership("GABC1234567890", "test_api_key")
    
    @pytest.mark.asyncio
    async def test_validate_sufficient_balance_success(self, transfer_service, mock_db_session):
        """Test successful balance validation"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service with sufficient balance
        with patch('api.services.transfer_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_service.return_value = mock_stellar_instance
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "XLM", "balance": "100.0", "asset_issuer": None}
            ]
            
            # Test balance validation
            await transfer_service._validate_sufficient_balance(
                "GABC1234567890", "XLM", "50.0", "stellar", "testnet"
            )
            
            # Verify blockchain service was called
            mock_stellar_instance.get_account_balances.assert_called_once_with("GABC1234567890")
    
    @pytest.mark.asyncio
    async def test_validate_sufficient_balance_insufficient_funds(self, transfer_service, mock_db_session):
        """Test balance validation with insufficient funds"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service with insufficient balance
        with patch('api.services.transfer_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_service.return_value = mock_stellar_instance
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "XLM", "balance": "10.0", "asset_issuer": None}
            ]
            
            # Test that exception is raised
            with pytest.raises(ValueError, match="Insufficient balance"):
                await transfer_service._validate_sufficient_balance(
                    "GABC1234567890", "XLM", "50.0", "stellar", "testnet"
                )
    
    @pytest.mark.asyncio
    async def test_validate_sufficient_balance_asset_not_found(self, transfer_service, mock_db_session):
        """Test balance validation with asset not found in account"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service with different asset
        with patch('api.services.transfer_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_service.return_value = mock_stellar_instance
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "USDC", "balance": "100.0", "asset_issuer": "GDUKMGUGDZQK6YHYA5Z6AY2G4XDSZPSZ3SW5UN3ARVMO6QSRDWP5YLEX"}
            ]
            
            # Test that exception is raised
            with pytest.raises(ValueError, match="Asset XLM not found"):
                await transfer_service._validate_sufficient_balance(
                    "GABC1234567890", "XLM", "50.0", "stellar", "testnet"
                )
    
    @pytest.mark.asyncio
    async def test_validate_sufficient_balance_hedera_success(self, transfer_service, mock_db_session):
        """Test successful balance validation for Hedera"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="0.0.123456",
            network="hedera",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Hedera service with sufficient balance
        with patch('api.services.hedera_service.HederaService') as mock_hedera_service:
            mock_hedera_instance = AsyncMock()
            mock_hedera_service.return_value = mock_hedera_instance
            mock_hedera_instance.get_account_balances.return_value = [
                {"asset_code": "HBAR", "balance": "100.0", "asset_issuer": None}
            ]
            
            # Test balance validation
            await transfer_service._validate_sufficient_balance(
                "0.0.123456", "HBAR", "50.0", "hedera", "testnet"
            )
            
            # Verify blockchain service was called
            mock_hedera_instance.get_account_balances.assert_called_once_with("0.0.123456")
    
    @pytest.mark.asyncio
    async def test_create_transfer_with_validation_success(self, transfer_service, mock_db_session):
        """Test transfer creation with successful validation"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service
        with patch('api.services.transfer_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_service.return_value = mock_stellar_instance
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "XLM", "balance": "100.0", "asset_issuer": None}
            ]
            
            # Mock database operations
            mock_db_session.add.return_value = None
            mock_db_session.commit.return_value = None
            mock_db_session.refresh.return_value = None
            
            # Test transfer creation with validation
            result = await transfer_service.create_transfer(
                from_account="GABC1234567890",
                to_account="GXYZ0987654321",
                asset_code="XLM",
                amount="10.0",
                network="stellar",
                environment="testnet",
                api_key="test_api_key"
            )
            
            # Assertions
            assert result["transaction_hash"].startswith("mock_stellar_tx_")
            assert result["from_account"] == "GABC1234567890"
            assert result["to_account"] == "GXYZ0987654321"
            assert result["asset_code"] == "XLM"
            assert result["amount"] == "10.0"
            assert result["network"] == "stellar"
            assert result["status"] == "pending"
            
            # Verify database operations
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_transfer_with_validation_insufficient_balance(self, transfer_service, mock_db_session):
        """Test transfer creation with insufficient balance validation failure"""
        # Mock account in database
        from api.models.account import Account
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            is_active=True
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service with insufficient balance
        with patch('api.services.transfer_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_service.return_value = mock_stellar_instance
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "XLM", "balance": "5.0", "asset_issuer": None}
            ]
            
            # Test that exception is raised
            with pytest.raises(ValueError, match="Insufficient balance"):
                await transfer_service.create_transfer(
                    from_account="GABC1234567890",
                    to_account="GXYZ0987654321",
                    asset_code="XLM",
                    amount="10.0",
                    network="stellar",
                    environment="testnet",
                    api_key="test_api_key"
                )
    
    @pytest.mark.asyncio
    async def test_create_transfer_with_validation_account_not_found(self, transfer_service, mock_db_session):
        """Test transfer creation with account not found validation failure"""
        # Mock database query result (no account found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test that exception is raised
        with pytest.raises(ValueError, match="Account not found"):
            await transfer_service.create_transfer(
                from_account="GINVALID123",
                to_account="GXYZ0987654321",
                asset_code="XLM",
                amount="10.0",
                network="stellar",
                environment="testnet",
                api_key="test_api_key"
            )
    
    # Transfer Status Tests (Story 2.2)
    
    @pytest.mark.asyncio
    async def test_get_transfer_status_comprehensive(self, transfer_service, mock_db_session):
        """Test comprehensive transfer status retrieval (AC1-10)"""
        # Mock transaction in database
        mock_transaction = create_mock_transaction(
            id=1,
            transaction_hash="mock_tx_hash_123",
            status="confirmed",
            compliance_status="approved",
            risk_score=0.1,
            ledger_time=datetime.now()
        )
        
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_transaction
        mock_db_session.execute.return_value = mock_result
        
        # Mock blockchain service
        with patch('api.services.transfer_service.StellarService') as mock_stellar:
            mock_stellar_instance = AsyncMock()
            mock_stellar.return_value = mock_stellar_instance
            mock_stellar_instance.get_transaction_details.return_value = {
                "status": "success",
                "ledger": 12345,
                "fee": "0.00001",
                "success": True
            }
            
            # Test comprehensive status retrieval
            result = await transfer_service.get_transfer_status(
                transfer_id="test_transfer_id",
                include_events=True,
                include_fees=True,
                include_compliance=True,
                refresh_blockchain=False
            )
            
            # Verify basic transfer info
            assert result["id"] == "1"
            assert result["transaction_hash"] == "mock_tx_hash_123"
            assert result["status"] == "confirmed"
            assert result["compliance_status"] == "approved"
            assert result["risk_score"] == 0.1
            
            # Verify blockchain details
            assert "blockchain_details" in result
            assert result["blockchain_details"]["status"] == "success"
            assert result["blockchain_details"]["ledger"] == 12345
            
            # Verify events
            assert "events" in result
            assert len(result["events"]) >= 1
            # Events are sorted by timestamp, so check that created event exists
            event_types = [event["event_type"] for event in result["events"]]
            assert "created" in event_types
            
            # Verify fees
            assert "fees" in result
            assert result["fees"]["total_fee"] == "0.00101"
            assert result["fees"]["network_fee"] == "0.00001"
            assert result["fees"]["service_fee"] == "0.001"
            
            # Verify compliance
            assert "compliance" in result
            assert result["compliance"]["status"] == "approved"
            assert result["compliance"]["risk_score"] == 0.1
    
    @pytest.mark.asyncio
    async def test_get_transfer_status_not_found(self, transfer_service, mock_db_session):
        """Test transfer status for non-existent transfer (AC6)"""
        # Mock empty database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test non-existent transfer
        result = await transfer_service.get_transfer_status("non_existent_id")
        
        # Verify None is returned
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_transfer_status_with_optional_params(self, transfer_service, mock_db_session):
        """Test transfer status with optional parameters disabled"""
        # Mock transaction in database
        mock_transaction = create_mock_transaction()
        
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_transaction
        mock_db_session.execute.return_value = mock_result
        
        # Test with optional parameters disabled
        result = await transfer_service.get_transfer_status(
            transfer_id="test_transfer_id",
            include_events=False,
            include_fees=False,
            include_compliance=False
        )
        
        # Verify basic info is present
        assert result["id"] == "1"
        assert result["transaction_hash"] == "mock_stellar_tx_123456"
        
        # Verify optional sections are not included or empty
        assert result.get("events") == []
        assert result.get("fees") == {
            "total_fee": "0",
            "network_fee": "0",
            "service_fee": "0",
            "breakdown": []
        }
        assert result.get("compliance") == {
            "status": "unknown",
            "risk_score": 0.0,
            "flags": [],
            "last_checked": None
        }
    
    @pytest.mark.asyncio
    async def test_get_transfer_events(self, transfer_service, mock_db_session):
        """Test transfer events retrieval (AC3, AC9)"""
        # Mock transaction with different timestamps
        created_time = datetime.now()
        updated_time = datetime.now()
        ledger_time = datetime.now()
        
        mock_transaction = create_mock_transaction(
            created_at=created_time,
            updated_at=updated_time,
            ledger_time=ledger_time,
            status="confirmed"
        )
        
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_transaction
        mock_db_session.execute.return_value = mock_result
        
        # Test events retrieval
        events = await transfer_service.get_transfer_events("test_transfer_id")
        
        # Verify events are generated
        assert len(events) == 3
        
        # Verify event types
        event_types = [event["event_type"] for event in events]
        assert "created" in event_types
        assert "updated" in event_types
        assert "confirmed" in event_types
        
        # Verify events are sorted by timestamp
        timestamps = [event["timestamp"] for event in events]
        assert timestamps == sorted(timestamps)
    
    @pytest.mark.asyncio
    async def test_get_transfer_fees(self, transfer_service, mock_db_session):
        """Test transfer fees calculation (AC5)"""
        # Mock transaction
        mock_transaction = create_mock_transaction(asset_code="USDC")
        
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_transaction
        mock_db_session.execute.return_value = mock_result
        
        # Test fees calculation
        fees = await transfer_service.get_transfer_fees("test_transfer_id")
        
        # Verify fee structure
        assert fees["total_fee"] == "0.00101"
        assert fees["network_fee"] == "0.00001"
        assert fees["service_fee"] == "0.001"
        assert len(fees["breakdown"]) == 2
        
        # Verify breakdown details
        network_fee = next(fee for fee in fees["breakdown"] if fee["type"] == "network")
        service_fee = next(fee for fee in fees["breakdown"] if fee["type"] == "service")
        
        assert network_fee["amount"] == "0.00001"
        assert network_fee["currency"] == "USDC"
        assert service_fee["amount"] == "0.001"
        assert service_fee["currency"] == "USDC"
    
    @pytest.mark.asyncio
    async def test_get_transfer_compliance(self, transfer_service, mock_db_session):
        """Test transfer compliance information (AC4, AC10)"""
        # Mock transaction with compliance data
        mock_transaction = create_mock_transaction(
            compliance_status="approved",
            risk_score=0.2
        )
        
        # Mock database query
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_transaction
        mock_db_session.execute.return_value = mock_result
        
        # Test compliance retrieval
        compliance = await transfer_service.get_transfer_compliance("test_transfer_id")
        
        # Verify compliance structure
        assert compliance["status"] == "approved"
        assert compliance["risk_score"] == 0.2
        assert compliance["flags"] == []
        assert compliance["compliance_level"] == "basic"
        assert compliance["aml_status"] == "passed"
        assert compliance["kyc_status"] == "verified"
    
    @pytest.mark.asyncio
    async def test_get_blockchain_transaction_details_stellar(self, transfer_service):
        """Test blockchain transaction details for Stellar (AC2, AC8)"""
        # Mock StellarService
        with patch('api.services.transfer_service.StellarService') as mock_stellar:
            mock_stellar_instance = AsyncMock()
            mock_stellar.return_value = mock_stellar_instance
            mock_stellar_instance.get_transaction_details.return_value = {
                "status": "success",
                "ledger": 12345,
                "fee": "0.00001",
                "success": True,
                "result_code": "txSUCCESS"
            }
            
            # Test blockchain details retrieval
            details = await transfer_service.get_blockchain_transaction_details(
                transaction_hash="test_hash",
                network="stellar",
                environment="testnet"
            )
            
            # Verify details structure
            assert details["transaction_hash"] == "test_hash"
            assert details["network"] == "stellar"
            assert details["environment"] == "testnet"
            assert details["status"] == "success"
            assert details["ledger"] == 12345
            assert details["fee"] == "0.00001"
            assert details["success"] is True
            assert details["result_code"] == "txSUCCESS"
    
    @pytest.mark.asyncio
    async def test_get_blockchain_transaction_details_hedera(self, transfer_service):
        """Test blockchain transaction details for Hedera (AC2, AC8)"""
        # Mock HederaService
        with patch('api.services.hedera_service.HederaService') as mock_hedera:
            mock_hedera_instance = AsyncMock()
            mock_hedera.return_value = mock_hedera_instance
            mock_hedera_instance.get_transaction_details.return_value = {
                "status": "success",
                "ledger": 12345,
                "fee": "0.0001",
                "success": True
            }
            
            # Test blockchain details retrieval
            details = await transfer_service.get_blockchain_transaction_details(
                transaction_hash="test_hash",
                network="hedera",
                environment="testnet"
            )
            
            # Verify details structure
            assert details["transaction_hash"] == "test_hash"
            assert details["network"] == "hedera"
            assert details["environment"] == "testnet"
            assert details["status"] == "success"
            assert details["ledger"] == 12345
            assert details["fee"] == "0.0001"
            assert details["success"] is True
    
    @pytest.mark.asyncio
    async def test_get_blockchain_transaction_details_unsupported_network(self, transfer_service):
        """Test blockchain transaction details for unsupported network"""
        # Test unsupported network
        with pytest.raises(ValueError, match="Unsupported network"):
            await transfer_service.get_blockchain_transaction_details(
                transaction_hash="test_hash",
                network="bitcoin",
                environment="testnet"
            )
    
    # Transfer Listing Tests (Story 2.3)
    
    @pytest.mark.asyncio
    async def test_list_transfers_comprehensive(self, transfer_service, mock_db_session):
        """Test comprehensive transfer listing with all features (AC1-10)"""
        # Mock transactions in database
        mock_transactions = [
            create_mock_transaction(
                id=1,
                transaction_hash="tx_hash_1",
                from_account="GABC1234567890",
                to_account="GXYZ0987654321",
                amount="10.0",
                status="confirmed",
                network="stellar"
            ),
            create_mock_transaction(
                id=2,
                transaction_hash="tx_hash_2",
                from_account="GABC1234567890",
                to_account="GDEF9876543210",
                amount="5.0",
                status="pending",
                network="stellar"
            )
        ]
        
        # Mock database queries - need to handle two calls
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 2
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Mock get_transfer_fees
        with patch.object(transfer_service, 'get_transfer_fees') as mock_get_fees:
            mock_get_fees.return_value = {
                "total_fee": "0.00101",
                "network_fee": "0.00001",
                "service_fee": "0.001",
                "breakdown": []
            }
            
            # Test comprehensive listing
            result = await transfer_service.list_transfers(
                from_account="GABC1234567890",
                status="confirmed",
                limit=10,
                skip=0,
                sort_by="created_at",
                sort_order="desc",
                include_fees=True,
                include_compliance=True
            )
            
            # Verify response structure
            assert "transfers" in result
            assert "pagination" in result
            assert "filters" in result
            assert "sorting" in result
            
            # Verify transfers
            assert len(result["transfers"]) == 2
            assert result["transfers"][0]["id"] == "1"
            assert result["transfers"][0]["from_account"] == "GABC1234567890"
            assert result["transfers"][0]["status"] == "confirmed"
            
            # Verify pagination
            assert result["pagination"]["total"] == 2
            assert result["pagination"]["page"] == 1
            assert result["pagination"]["per_page"] == 10
            assert result["pagination"]["has_next"] is False
            assert result["pagination"]["has_prev"] is False
            
            # Verify filters
            assert result["filters"]["from_account"] == "GABC1234567890"
            assert result["filters"]["status"] == "confirmed"
            
            # Verify sorting
            assert result["sorting"]["sort_by"] == "created_at"
            assert result["sorting"]["sort_order"] == "desc"
            
            # Verify fees are included
            assert "fees" in result["transfers"][0]
            assert result["transfers"][0]["fees"]["total_fee"] == "0.00101"
            
            # Verify compliance is included
            assert "compliance_status" in result["transfers"][0]
            assert "risk_score" in result["transfers"][0]
    
    @pytest.mark.asyncio
    async def test_list_transfers_pagination(self, transfer_service, mock_db_session):
        """Test transfer listing pagination (AC1, AC10)"""
        # Mock transactions
        mock_transactions = [create_mock_transaction(id=i) for i in range(1, 6)]
        
        # Mock database queries - need to handle two calls
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 25  # Total 25 transfers
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Test pagination
        result = await transfer_service.list_transfers(
            limit=5,
            skip=10,
            include_fees=False,
            include_compliance=False
        )
        
        # Verify pagination metadata
        assert result["pagination"]["total"] == 25
        assert result["pagination"]["page"] == 3  # (10 // 5) + 1
        assert result["pagination"]["per_page"] == 5
        assert result["pagination"]["pages"] == 5  # (25 + 5 - 1) // 5
        assert result["pagination"]["has_next"] is True
        assert result["pagination"]["has_prev"] is True
    
    @pytest.mark.asyncio
    async def test_list_transfers_filtering(self, transfer_service, mock_db_session):
        """Test transfer listing with various filters (AC2, AC6)"""
        # Mock transactions
        mock_transactions = [create_mock_transaction()]
        
        # Mock database queries - need to handle two calls
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with multiple filters
        result = await transfer_service.list_transfers(
            from_account="GABC1234567890",
            to_account="GXYZ0987654321",
            network="stellar",
            environment="testnet",
            asset_code="XLM",
            status="confirmed",
            from_country="NG",
            to_country="US",
            include_fees=False,
            include_compliance=False
        )
        
        # Verify filters are applied
        assert result["filters"]["from_account"] == "GABC1234567890"
        assert result["filters"]["to_account"] == "GXYZ0987654321"
        assert result["filters"]["network"] == "stellar"
        assert result["filters"]["environment"] == "testnet"
        assert result["filters"]["asset_code"] == "XLM"
        assert result["filters"]["status"] == "confirmed"
        assert result["filters"]["from_country"] == "NG"
        assert result["filters"]["to_country"] == "US"
    
    @pytest.mark.asyncio
    async def test_list_transfers_sorting(self, transfer_service, mock_db_session):
        """Test transfer listing with different sorting options (AC5, AC9)"""
        # Mock transactions
        mock_transactions = [create_mock_transaction()]
        
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Test sorting by amount ascending
        result = await transfer_service.list_transfers(
            sort_by="amount",
            sort_order="asc",
            include_fees=False,
            include_compliance=False
        )
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "amount"
        assert result["sorting"]["sort_order"] == "asc"
        
        # Reset mocks for second call
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Test sorting by status descending
        result = await transfer_service.list_transfers(
            sort_by="status",
            sort_order="desc",
            include_fees=False,
            include_compliance=False
        )
        
        # Verify sorting
        assert result["sorting"]["sort_by"] == "status"
        assert result["sorting"]["sort_order"] == "desc"
    
    @pytest.mark.asyncio
    async def test_list_transfers_with_fees(self, transfer_service, mock_db_session):
        """Test transfer listing with fee information (AC4, AC8)"""
        # Mock transactions
        mock_transactions = [create_mock_transaction()]
        
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Mock get_transfer_fees
        with patch.object(transfer_service, 'get_transfer_fees') as mock_get_fees:
            mock_get_fees.return_value = {
                "total_fee": "0.00101",
                "network_fee": "0.00001",
                "service_fee": "0.001",
                "breakdown": [
                    {"type": "network", "amount": "0.00001", "currency": "XLM"},
                    {"type": "service", "amount": "0.001", "currency": "XLM"}
                ]
            }
            
            # Test with fees included
            result = await transfer_service.list_transfers(
                include_fees=True,
                include_compliance=False
            )
            
            # Verify fees are included
            assert "fees" in result["transfers"][0]
            assert result["transfers"][0]["fees"]["total_fee"] == "0.00101"
            assert result["transfers"][0]["fees"]["network_fee"] == "0.00001"
            assert result["transfers"][0]["fees"]["service_fee"] == "0.001"
            assert len(result["transfers"][0]["fees"]["breakdown"]) == 2
    
    @pytest.mark.asyncio
    async def test_list_transfers_with_compliance(self, transfer_service, mock_db_session):
        """Test transfer listing with compliance information (AC3, AC7)"""
        # Mock transactions with compliance data
        mock_transactions = [create_mock_transaction(
            compliance_status="approved",
            risk_score=0.2
        )]
        
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Test with compliance included
        result = await transfer_service.list_transfers(
            include_fees=False,
            include_compliance=True
        )
        
        # Verify compliance information is included
        assert "compliance_status" in result["transfers"][0]
        assert "risk_score" in result["transfers"][0]
        assert result["transfers"][0]["compliance_status"] == "approved"
        assert result["transfers"][0]["risk_score"] == 0.2
    
    @pytest.mark.asyncio
    async def test_list_transfers_empty_result(self, transfer_service, mock_db_session):
        """Test transfer listing with no results"""
        # Mock empty result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 0
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Test empty result
        result = await transfer_service.list_transfers(
            include_fees=False,
            include_compliance=False
        )
        
        # Verify empty result structure
        assert result["transfers"] == []
        assert result["pagination"]["total"] == 0
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["pages"] == 0
        assert result["pagination"]["has_next"] is False
        assert result["pagination"]["has_prev"] is False
    
    @pytest.mark.asyncio
    async def test_list_transfers_fee_error_handling(self, transfer_service, mock_db_session):
        """Test transfer listing with fee retrieval error"""
        # Mock transactions
        mock_transactions = [create_mock_transaction()]
        
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_transactions
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Set up side_effect to return different results for different calls
        mock_db_session.execute.side_effect = [mock_result, mock_count_result]
        
        # Mock get_transfer_fees to raise exception
        with patch.object(transfer_service, 'get_transfer_fees') as mock_get_fees:
            mock_get_fees.side_effect = Exception("Fee service unavailable")
            
            # Test with fees included but error occurs
            result = await transfer_service.list_transfers(
                include_fees=True,
                include_compliance=False
            )
            
            # Verify fallback fee structure
            assert "fees" in result["transfers"][0]
            assert result["transfers"][0]["fees"]["total_fee"] == "0"
            assert result["transfers"][0]["fees"]["network_fee"] == "0"
            assert result["transfers"][0]["fees"]["service_fee"] == "0"
            assert result["transfers"][0]["fees"]["breakdown"] == []