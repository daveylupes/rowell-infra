"""
Unit tests for AccountService
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.account_service import AccountService
from api.models.account import Account


class TestAccountService:
    """Test cases for AccountService"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        return AsyncMock(spec=AsyncSession)
    
    @pytest.fixture
    def account_service(self, mock_db_session):
        """Account service instance with mocked database"""
        return AccountService(mock_db_session)
    
    @pytest.mark.asyncio
    async def test_create_account_stellar_success(self, account_service, mock_db_session):
        """Test successful Stellar account creation"""
        # Mock the Stellar service
        with patch('api.services.account_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_instance.create_account.return_value = {
                "account_id": "GABC1234567890",
                "secret_key": "SABC1234567890",
                "network": "stellar",
                "environment": "testnet"
            }
            mock_stellar_service.return_value = mock_stellar_instance
            
            # Mock database operations
            from datetime import datetime
            mock_account = Account(
                id=1,
                account_id="GABC1234567890",
                network="stellar",
                environment="testnet",
                account_type="user",
                country_code="NG",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=None
            )
            mock_db_session.add.return_value = None
            mock_db_session.commit.return_value = None
            # Mock refresh to set the account object with proper values
            def mock_refresh(account):
                account.id = 1
                account.created_at = datetime.now()
                account.updated_at = datetime.now()
                account.last_activity = None
            mock_db_session.refresh.side_effect = mock_refresh
            
            # Test account creation
            result = await account_service.create_account(
                network="stellar",
                environment="testnet",
                account_type="user",
                country_code="NG"
            )
            
            # Assertions
            assert result["account_id"] == "GABC1234567890"
            assert result["network"] == "stellar"
            assert result["environment"] == "testnet"
            assert result["account_type"] == "user"
            assert result["country_code"] == "NG"
            
            # Verify database operations
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_account_hedera_mock(self, account_service, mock_db_session):
        """Test Hedera account creation (mock response)"""
        # Mock database operations
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="0.0.123456",
            network="hedera",
            environment="testnet",
            account_type="user",
            country_code="NG",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None
        # Mock refresh to set the account object with proper values
        def mock_refresh(account):
            account.id = 1
            account.created_at = datetime.now()
            account.updated_at = datetime.now()
            account.last_activity = None
        mock_db_session.refresh.side_effect = mock_refresh
        
        result = await account_service.create_account(
            network="hedera",
            environment="testnet",
            account_type="user",
            country_code="NG"
        )
        
        # Assertions for mock Hedera response
        assert result["network"] == "hedera"
        assert result["environment"] == "testnet"
        assert result["account_type"] == "user"
        assert result["country_code"] == "NG"
        assert result["account_id"].startswith("0.0.")
        assert result["secret_key"].startswith("mock_hedera_private_")
    
    @pytest.mark.asyncio
    async def test_create_account_invalid_network(self, account_service):
        """Test account creation with invalid network"""
        with pytest.raises(ValueError, match="Unsupported network"):
            await account_service.create_account(
                network="bitcoin",
                environment="testnet",
                account_type="user",
                country_code="NG"
            )
    
    @pytest.mark.asyncio
    async def test_create_account_database_error(self, account_service, mock_db_session):
        """Test account creation with database error"""
        # Mock Stellar service success
        with patch('api.services.account_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_instance.create_account.return_value = {
                "account_id": "GABC1234567890",
                "secret_key": "SABC1234567890"
            }
            mock_stellar_service.return_value = mock_stellar_instance
            
            # Mock database error
            mock_db_session.commit.side_effect = Exception("Database error")
            mock_db_session.rollback.return_value = None
            
            # Test that exception is raised and rollback is called
            with pytest.raises(Exception, match="Database error"):
                await account_service.create_account(
                    network="stellar",
                    environment="testnet",
                    account_type="user",
                    country_code="NG"
                )
            
            mock_db_session.rollback.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_list_accounts_basic(self, account_service, mock_db_session):
        """Test basic account listing with pagination"""
        # Mock database query results
        from datetime import datetime
        mock_accounts = [
            Account(
                id=1,
                account_id="GABC1234567890",
                network="stellar",
                environment="testnet",
                account_type="user",
                country_code="NG",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=None
            ),
            Account(
                id=2,
                account_id="GXYZ0987654321",
                network="stellar",
                environment="testnet",
                account_type="merchant",
                country_code="KE",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=None
            )
        ]
        
        # Mock the two database calls (accounts query and count query)
        accounts_result = MagicMock()
        accounts_result.scalars.return_value.all.return_value = mock_accounts
        
        count_result = MagicMock()
        count_result.scalar.return_value = 2
        
        mock_db_session.execute.side_effect = [accounts_result, count_result]
        
        # Test listing accounts
        result = await account_service.list_accounts()
        
        # Assertions
        assert "accounts" in result
        assert "pagination" in result
        assert len(result["accounts"]) == 2
        assert result["accounts"][0]["account_id"] == "GABC1234567890"
        assert result["accounts"][1]["account_id"] == "GXYZ0987654321"
        assert result["accounts"][0]["account_type"] == "user"
        assert result["accounts"][1]["account_type"] == "merchant"
        assert result["pagination"]["total"] == 2
        assert result["pagination"]["limit"] == 100
        assert result["pagination"]["offset"] == 0
        assert result["pagination"]["has_more"] == False
    
    @pytest.mark.asyncio
    async def test_list_accounts_with_filters(self, account_service, mock_db_session):
        """Test account listing with filters (AC2, AC6-9)"""
        # Mock database query results
        from datetime import datetime
        mock_accounts = [
            Account(
                id=1,
                account_id="GABC1234567890",
                network="stellar",
                environment="testnet",
                account_type="user",
                country_code="NG",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=None
            )
        ]
        
        accounts_result = MagicMock()
        accounts_result.scalars.return_value.all.return_value = mock_accounts
        
        count_result = MagicMock()
        count_result.scalar.return_value = 1
        
        mock_db_session.execute.side_effect = [accounts_result, count_result]
        
        # Test listing accounts with filters
        result = await account_service.list_accounts(
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            limit=50,
            offset=0
        )
        
        # Assertions
        assert len(result["accounts"]) == 1
        assert result["accounts"][0]["network"] == "stellar"
        assert result["accounts"][0]["environment"] == "testnet"
        assert result["accounts"][0]["account_type"] == "user"
        assert result["accounts"][0]["country_code"] == "NG"
        assert result["pagination"]["limit"] == 50
        assert result["pagination"]["offset"] == 0
    
    @pytest.mark.asyncio
    async def test_list_accounts_with_balances(self, account_service, mock_db_session):
        """Test account listing with balance information (AC4, AC10)"""
        # Mock database query results
        from datetime import datetime
        mock_accounts = [
            Account(
                id=1,
                account_id="GABC1234567890",
                network="stellar",
                environment="testnet",
                account_type="user",
                country_code="NG",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=None
            )
        ]
        
        accounts_result = MagicMock()
        accounts_result.scalars.return_value.all.return_value = mock_accounts
        
        count_result = MagicMock()
        count_result.scalar.return_value = 1
        
        mock_db_session.execute.side_effect = [accounts_result, count_result]
        
        # Mock the get_account_balances method
        with patch.object(account_service, 'get_account_balances', return_value=[
            {"asset_code": "XLM", "balance": "100.00", "asset_type": "native"}
        ]) as mock_get_balances:
            
            # Test listing accounts with balances
            result = await account_service.list_accounts(include_balances=True)
            
            # Assertions
            assert len(result["accounts"]) == 1
            assert "balances" in result["accounts"][0]
            assert len(result["accounts"][0]["balances"]) == 1
            assert result["accounts"][0]["balances"][0]["asset_code"] == "XLM"
            assert result["accounts"][0]["balances"][0]["balance"] == "100.00"
            mock_get_balances.assert_called_once_with("GABC1234567890")
    
    @pytest.mark.asyncio
    async def test_list_accounts_pagination(self, account_service, mock_db_session):
        """Test account listing pagination (AC1)"""
        # Mock database query results
        from datetime import datetime
        mock_accounts = [
            Account(
                id=2,
                account_id="GXYZ0987654321",
                network="stellar",
                environment="testnet",
                account_type="merchant",
                country_code="KE",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=None
            )
        ]
        
        accounts_result = MagicMock()
        accounts_result.scalars.return_value.all.return_value = mock_accounts
        
        count_result = MagicMock()
        count_result.scalar.return_value = 5  # Total of 5 accounts
        
        mock_db_session.execute.side_effect = [accounts_result, count_result]
        
        # Test pagination (offset=1, limit=1)
        result = await account_service.list_accounts(limit=1, offset=1)
        
        # Assertions
        assert len(result["accounts"]) == 1
        assert result["pagination"]["total"] == 5
        assert result["pagination"]["limit"] == 1
        assert result["pagination"]["offset"] == 1
        assert result["pagination"]["has_more"] == True  # (1 + 1) < 5
    
    @pytest.mark.asyncio
    async def test_list_accounts_empty_result(self, account_service, mock_db_session):
        """Test account listing with no results"""
        # Mock database query results (no accounts)
        accounts_result = MagicMock()
        accounts_result.scalars.return_value.all.return_value = []
        
        count_result = MagicMock()
        count_result.scalar.return_value = 0
        
        mock_db_session.execute.side_effect = [accounts_result, count_result]
        
        # Test listing accounts with no results
        result = await account_service.list_accounts()
        
        # Assertions
        assert len(result["accounts"]) == 0
        assert result["pagination"]["total"] == 0
        assert result["pagination"]["has_more"] == False
    
    @pytest.mark.asyncio
    async def test_list_accounts_balance_error(self, account_service, mock_db_session):
        """Test account listing when balance retrieval fails"""
        # Mock database query results
        from datetime import datetime
        mock_accounts = [
            Account(
                id=1,
                account_id="GABC1234567890",
                network="stellar",
                environment="testnet",
                account_type="user",
                country_code="NG",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                last_activity=None
            )
        ]
        
        accounts_result = MagicMock()
        accounts_result.scalars.return_value.all.return_value = mock_accounts
        
        count_result = MagicMock()
        count_result.scalar.return_value = 1
        
        mock_db_session.execute.side_effect = [accounts_result, count_result]
        
        # Mock the get_account_balances method to raise an exception
        with patch.object(account_service, 'get_account_balances', side_effect=Exception("Balance error")):
            
            # Test listing accounts with balance error
            result = await account_service.list_accounts(include_balances=True)
            
            # Assertions - should still return account but with empty balances
            assert len(result["accounts"]) == 1
            assert "balances" in result["accounts"][0]
            assert result["accounts"][0]["balances"] == []
    
    @pytest.mark.asyncio
    async def test_get_account_success(self, account_service, mock_db_session):
        """Test getting account by ID"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Test getting account
        result = await account_service.get_account("GABC1234567890")
        
        # Assertions
        assert result is not None
        assert result["account_id"] == "GABC1234567890"
        assert result["network"] == "stellar"
        assert result["account_type"] == "user"
    
    @pytest.mark.asyncio
    async def test_get_account_not_found(self, account_service, mock_db_session):
        """Test getting non-existent account"""
        # Mock database query result (no account found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test getting non-existent account
        result = await account_service.get_account("NONEXISTENT")
        
        # Assertions
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_account_balances_stellar(self, account_service, mock_db_session):
        """Test getting account balances for Stellar"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service
        with patch('api.services.account_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_instance.get_account_balances.return_value = [
                {"asset_code": "XLM", "balance": "100.00", "asset_type": "native"},
                {"asset_code": "USDC", "balance": "50.00", "asset_type": "credit_alphanum4"}
            ]
            mock_stellar_service.return_value = mock_stellar_instance
            
            # Test getting balances
            result = await account_service.get_account_balances("GABC1234567890")
            
            # Assertions
            assert len(result) == 2
            assert result[0]["asset_code"] == "XLM"
            assert result[0]["balance"] == "100.00"
            assert result[1]["asset_code"] == "USDC"
            assert result[1]["balance"] == "50.00"
    
    @pytest.mark.asyncio
    async def test_get_account_balances_hedera_mock(self, account_service, mock_db_session):
        """Test getting account balances for Hedera (mock)"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="0.0.123456",
            network="hedera",
            environment="testnet",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Test getting balances (should return mock data)
        result = await account_service.get_account_balances("0.0.123456")
        
        # Assertions for mock Hedera response
        assert len(result) == 1
        assert result[0]["asset_code"] == "HBAR"
        assert result[0]["balance"] == "100.00"
        assert result[0]["asset_type"] == "native"
    
    @pytest.mark.asyncio
    async def test_get_account_balances_account_not_found(self, account_service, mock_db_session):
        """Test getting balances for non-existent account"""
        # Mock database query result (no account found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test getting balances for non-existent account
        with pytest.raises(ValueError, match="Account not found"):
            await account_service.get_account_balances("NONEXISTENT")
    
    @pytest.mark.asyncio
    async def test_get_account_details_comprehensive(self, account_service, mock_db_session):
        """Test comprehensive account details retrieval (AC1-9)"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock the other methods
        with patch.object(account_service, 'get_account_balances', return_value=[
            {"asset_code": "XLM", "balance": "100.00", "asset_type": "native"}
        ]) as mock_balances, \
             patch.object(account_service, 'get_account_transactions', return_value=[
                 {"id": "tx1", "amount": "10.00", "type": "payment"}
             ]) as mock_transactions, \
             patch.object(account_service, 'get_account_compliance', return_value={
                 "kyc_status": "verified",
                 "is_verified": True,
                 "is_compliant": True,
                 "flags": [],
                 "last_verified": "2024-01-01T00:00:00Z",
                 "verification_level": "basic",
                 "risk_score": 0.1
             }) as mock_compliance:
            
            # Test comprehensive account details
            result = await account_service.get_account_details("GABC1234567890")
            
            # Assertions
            assert result is not None
            assert result["account_id"] == "GABC1234567890"
            assert result["network"] == "stellar"
            assert result["environment"] == "testnet"
            assert result["account_type"] == "user"
            assert result["country_code"] == "NG"
            
            # Check balances (AC2, AC6)
            assert "balances" in result
            assert len(result["balances"]) == 1
            assert result["balances"][0]["asset_code"] == "XLM"
            assert result["balances"][0]["balance"] == "100.00"
            
            # Check transactions (AC3, AC7)
            assert "recent_transactions" in result
            assert len(result["recent_transactions"]) == 1
            assert result["recent_transactions"][0]["id"] == "tx1"
            assert result["recent_transactions"][0]["amount"] == "10.00"
            
            # Check compliance (AC4, AC8)
            assert "compliance" in result
            assert result["compliance"]["kyc_status"] == "verified"
            assert result["compliance"]["is_verified"] == True
            assert result["compliance"]["is_compliant"] == True
            assert result["compliance"]["verification_level"] == "basic"
            assert result["compliance"]["risk_score"] == 0.1
            
            # Verify method calls
            mock_balances.assert_called_once_with("GABC1234567890")
            mock_transactions.assert_called_once_with("GABC1234567890", limit=10)
            mock_compliance.assert_called_once_with("GABC1234567890")
    
    @pytest.mark.asyncio
    async def test_get_account_details_account_not_found(self, account_service, mock_db_session):
        """Test account details for non-existent account (AC5)"""
        # Mock database query result (no account found)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Test getting details for non-existent account
        result = await account_service.get_account_details("NONEXISTENT")
        
        # Assertions
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_account_details_with_optional_params(self, account_service, mock_db_session):
        """Test account details with optional parameters"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock the get_account method
        with patch.object(account_service, 'get_account', return_value={
            "id": "1",
            "account_id": "GABC1234567890",
            "network": "stellar",
            "environment": "testnet",
            "account_type": "user",
            "country_code": "NG",
            "is_active": True,
            "is_verified": True,
            "is_compliant": True,
            "kyc_status": "verified",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "last_activity": None,
            "metadata": {}
        }) as mock_get_account:
            
            # Test with balances disabled
            result = await account_service.get_account_details(
                "GABC1234567890", 
                include_balances=False,
                include_transactions=False,
                include_compliance=False
            )
            
            # Assertions
            assert result is not None
            assert result["account_id"] == "GABC1234567890"
            assert "balances" not in result
            assert "recent_transactions" not in result
            assert "compliance" not in result
            
            mock_get_account.assert_called_once_with("GABC1234567890")
    
    @pytest.mark.asyncio
    async def test_get_account_details_graceful_degradation(self, account_service, mock_db_session):
        """Test account details with graceful degradation on errors (AC5)"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            account_type="user",
            country_code="NG",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock the get_account method
        with patch.object(account_service, 'get_account', return_value={
            "id": "1",
            "account_id": "GABC1234567890",
            "network": "stellar",
            "environment": "testnet",
            "account_type": "user",
            "country_code": "NG",
            "is_active": True,
            "is_verified": True,
            "is_compliant": True,
            "kyc_status": "verified",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "last_activity": None,
            "metadata": {}
        }) as mock_get_account, \
             patch.object(account_service, 'get_account_balances', side_effect=Exception("Balance error")), \
             patch.object(account_service, 'get_account_transactions', side_effect=Exception("Transaction error")), \
             patch.object(account_service, 'get_account_compliance', side_effect=Exception("Compliance error")):
            
            # Test graceful degradation
            result = await account_service.get_account_details("GABC1234567890")
            
            # Assertions - should still return account with empty/fallback data
            assert result is not None
            assert result["account_id"] == "GABC1234567890"
            assert result["balances"] == []  # Empty due to error
            assert result["recent_transactions"] == []  # Empty due to error
            assert result["compliance"]["kyc_status"] == "verified"  # Fallback data
            assert result["compliance"]["is_verified"] == True
            assert result["compliance"]["is_compliant"] == True
            assert result["compliance"]["flags"] == []
    
    @pytest.mark.asyncio
    async def test_get_account_transactions_success(self, account_service, mock_db_session):
        """Test getting account transactions (AC3, AC7)"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Mock Stellar service
        with patch('api.services.account_service.StellarService') as mock_stellar_service:
            mock_stellar_instance = AsyncMock()
            mock_stellar_instance.get_account_transactions.return_value = [
                {"id": "tx1", "amount": "10.00", "type": "payment", "created_at": "2024-01-01T00:00:00Z"},
                {"id": "tx2", "amount": "5.00", "type": "payment", "created_at": "2024-01-02T00:00:00Z"}
            ]
            mock_stellar_service.return_value = mock_stellar_instance
            
            # Test getting transactions
            result = await account_service.get_account_transactions("GABC1234567890", limit=5, offset=0)
            
            # Assertions
            assert len(result) == 2
            assert result[0]["id"] == "tx1"
            assert result[0]["amount"] == "10.00"
            assert result[1]["id"] == "tx2"
            assert result[1]["amount"] == "5.00"
            
            mock_stellar_instance.get_account_transactions.assert_called_once_with("GABC1234567890", limit=5, offset=0)
    
    @pytest.mark.asyncio
    async def test_get_account_compliance_success(self, account_service, mock_db_session):
        """Test getting account compliance information (AC4, AC8)"""
        # Mock database query result
        from datetime import datetime
        mock_account = Account(
            id=1,
            account_id="GABC1234567890",
            network="stellar",
            environment="testnet",
            kyc_status="verified",
            is_verified=True,
            is_compliant=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_activity=None
        )
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_account
        mock_db_session.execute.return_value = mock_result
        
        # Test getting compliance info
        result = await account_service.get_account_compliance("GABC1234567890")
        
        # Assertions
        assert result["kyc_status"] == "verified"
        assert result["is_verified"] == True
        assert result["is_compliant"] == True
        assert result["flags"] == []
        assert result["verification_level"] == "basic"
        assert result["risk_score"] == 0.0
        assert result["last_verified"] is not None
