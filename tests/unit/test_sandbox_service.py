"""
Unit tests for SandboxService
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta
import uuid

from api.services.sandbox_service import SandboxService


class TestSandboxService:
    """Test cases for SandboxService"""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        return AsyncMock()
    
    @pytest.fixture
    def sandbox_service(self, mock_db_session):
        """SandboxService instance with mocked database"""
        return SandboxService(mock_db_session)
    
    @pytest.mark.asyncio
    async def test_generate_mock_accounts_default_count(self, sandbox_service):
        """Test generating mock accounts with default count"""
        accounts = await sandbox_service.generate_mock_accounts()
        
        assert len(accounts) == 10
        assert all(hasattr(account, 'id') for account in accounts)
        assert all(hasattr(account, 'account_id') for account in accounts)
        assert all(hasattr(account, 'network') for account in accounts)
        assert all(hasattr(account, 'environment') for account in accounts)
        assert all(hasattr(account, 'account_type') for account in accounts)
        assert all(hasattr(account, 'country_code') for account in accounts)
        assert all(hasattr(account, 'metadata') for account in accounts)
        
        # Check metadata
        for account in accounts:
            assert account.metadata['sandbox'] is True
            assert account.metadata['mock_data'] is True
            assert 'test_scenario' in account.metadata
    
    @pytest.mark.asyncio
    async def test_generate_mock_accounts_custom_count(self, sandbox_service):
        """Test generating mock accounts with custom count"""
        count = 25
        accounts = await sandbox_service.generate_mock_accounts(count)
        
        assert len(accounts) == count
        
        # Check that all accounts have valid data
        for account in accounts:
            assert account.network in ['stellar', 'hedera']
            assert account.environment == 'testnet'
            assert account.account_type in ['individual', 'merchant', 'anchor', 'ngo']
            assert account.country_code in ['NG', 'KE', 'GH', 'ZA', 'EG', 'MA', 'TN', 'UG', 'RW', 'ET']
            assert account.region in ['West Africa', 'East Africa', 'North Africa', 'Southern Africa', 'Africa']
    
    @pytest.mark.asyncio
    async def test_generate_mock_transactions(self, sandbox_service):
        """Test generating mock transactions"""
        account_ids = ['acc1', 'acc2', 'acc3', 'acc4']
        count = 20
        
        transactions = await sandbox_service.generate_mock_transactions(account_ids, count)
        
        assert len(transactions) == count
        
        for transaction in transactions:
            assert hasattr(transaction, 'id')
            assert hasattr(transaction, 'transaction_hash')
            assert hasattr(transaction, 'network')
            assert hasattr(transaction, 'environment')
            assert hasattr(transaction, 'transaction_type')
            assert hasattr(transaction, 'status')
            assert hasattr(transaction, 'from_account')
            assert hasattr(transaction, 'to_account')
            assert hasattr(transaction, 'asset_code')
            assert hasattr(transaction, 'amount')
            
            # Check transaction data validity
            assert transaction.network in ['stellar', 'hedera']
            assert transaction.environment == 'testnet'
            assert transaction.transaction_type in ['payment', 'transfer', 'token_transfer']
            assert transaction.status in ['success', 'pending', 'failed']
            assert transaction.from_account in account_ids
            assert transaction.to_account in account_ids
            assert transaction.from_account != transaction.to_account
            assert transaction.asset_code in ['USDC', 'XLM', 'HBAR', 'NGN', 'KES', 'GHS', 'ZAR']
    
    @pytest.mark.asyncio
    async def test_generate_mock_analytics_data(self, sandbox_service):
        """Test generating mock analytics data"""
        analytics_data = await sandbox_service.generate_mock_analytics_data()
        
        assert 'remittance_flows' in analytics_data
        assert 'stablecoin_adoption' in analytics_data
        assert 'merchant_activity' in analytics_data
        assert 'network_metrics' in analytics_data
        
        # Check remittance flows
        flows = analytics_data['remittance_flows']
        assert len(flows) == 20
        for flow in flows:
            assert hasattr(flow, 'from_country')
            assert hasattr(flow, 'to_country')
            assert hasattr(flow, 'asset_code')
            assert hasattr(flow, 'total_volume')
            assert hasattr(flow, 'avg_fee')
            assert hasattr(flow, 'avg_fee_percentage')
            assert flow.from_country != flow.to_country
        
        # Check stablecoin adoption
        adoption = analytics_data['stablecoin_adoption']
        assert len(adoption) == 15
        for item in adoption:
            assert hasattr(item, 'asset_code')
            assert hasattr(item, 'total_volume')
            assert item.asset_code in ['USDC', 'USDT', 'DAI', 'BUSD']
        
        # Check merchant activity
        activities = analytics_data['merchant_activity']
        assert len(activities) == 12
        for activity in activities:
            assert hasattr(activity, 'merchant_type')
            assert hasattr(activity, 'total_volume')
            assert activity.merchant_type in ['fintech', 'ecommerce', 'remittance', 'banking', 'retail']
        
        # Check network metrics
        metrics = analytics_data['network_metrics']
        assert len(metrics) == 6
        for metric in metrics:
            assert hasattr(metric, 'network')
            assert hasattr(metric, 'environment')
            assert hasattr(metric, 'total_transactions')
            assert metric.network in ['stellar', 'hedera']
            assert metric.environment in ['testnet', 'mainnet']
    
    @pytest.mark.asyncio
    async def test_generate_mock_kyc_verifications(self, sandbox_service):
        """Test generating mock KYC verifications"""
        account_ids = ['acc1', 'acc2', 'acc3']
        count = 10
        
        verifications = await sandbox_service.generate_mock_kyc_verifications(account_ids, count)
        
        assert len(verifications) == count
        
        for verification in verifications:
            assert hasattr(verification, 'verification_id')
            assert hasattr(verification, 'account_id')
            assert hasattr(verification, 'verification_type')
            assert hasattr(verification, 'verification_status')
            assert hasattr(verification, 'provider')
            
            assert verification.account_id in account_ids
            assert verification.verification_type in ['individual', 'business', 'ngo']
            assert verification.verification_status in ['verified', 'pending', 'rejected']
            assert verification.provider in ['internal', 'jumio', 'onfido', 'trulioo']
    
    @pytest.mark.asyncio
    async def test_generate_mock_compliance_flags(self, sandbox_service):
        """Test generating mock compliance flags"""
        entity_ids = ['entity1', 'entity2', 'entity3']
        count = 8
        
        flags = await sandbox_service.generate_mock_compliance_flags(entity_ids, count)
        
        assert len(flags) == count
        
        for flag in flags:
            assert hasattr(flag, 'entity_type')
            assert hasattr(flag, 'entity_id')
            assert hasattr(flag, 'flag_type')
            assert hasattr(flag, 'flag_severity')
            assert hasattr(flag, 'flag_status')
            
            assert flag.entity_type in ['account', 'transaction']
            assert flag.entity_id in entity_ids
            assert flag.flag_type in ['aml', 'kyc', 'sanctions', 'risk']
            assert flag.flag_severity in ['low', 'medium', 'high', 'critical']
            assert flag.flag_status in ['active', 'resolved', 'false_positive']
    
    @pytest.mark.asyncio
    async def test_get_region_from_country(self, sandbox_service):
        """Test getting region from country code"""
        assert sandbox_service._get_region_from_country('NG') == 'West Africa'
        assert sandbox_service._get_region_from_country('GH') == 'West Africa'
        assert sandbox_service._get_region_from_country('KE') == 'East Africa'
        assert sandbox_service._get_region_from_country('ZA') == 'Southern Africa'
        assert sandbox_service._get_region_from_country('EG') == 'North Africa'
        assert sandbox_service._get_region_from_country('UNKNOWN') == 'Africa'
    
    @pytest.mark.asyncio
    async def test_reset_sandbox_data_success(self, sandbox_service):
        """Test successful sandbox data reset"""
        result = await sandbox_service.reset_sandbox_data()
        
        assert result['success'] is True
        assert 'message' in result
        assert 'timestamp' in result
        assert 'reset successfully' in result['message']
    
    @pytest.mark.asyncio
    async def test_get_sandbox_stats_success(self, sandbox_service):
        """Test getting sandbox statistics"""
        stats = await sandbox_service.get_sandbox_stats()
        
        assert 'accounts' in stats
        assert 'transactions' in stats
        assert 'analytics' in stats
        assert 'compliance' in stats
        assert 'last_updated' in stats
        
        # Check accounts stats
        assert 'total' in stats['accounts']
        assert 'active' in stats['accounts']
        assert 'verified' in stats['accounts']
        assert 'countries' in stats['accounts']
        
        # Check transactions stats
        assert 'total' in stats['transactions']
        assert 'successful' in stats['transactions']
        assert 'pending' in stats['transactions']
        assert 'failed' in stats['transactions']
        assert 'total_volume_usd' in stats['transactions']
        
        # Check analytics stats
        assert 'remittance_flows' in stats['analytics']
        assert 'stablecoin_adoption_records' in stats['analytics']
        assert 'merchant_activities' in stats['analytics']
        assert 'network_metrics' in stats['analytics']
        
        # Check compliance stats
        assert 'kyc_verifications' in stats['compliance']
        assert 'compliance_flags' in stats['compliance']
        assert 'active_flags' in stats['compliance']
        assert 'resolved_flags' in stats['compliance']
    
    @pytest.mark.asyncio
    async def test_account_metadata_structure(self, sandbox_service):
        """Test that generated accounts have proper metadata structure"""
        accounts = await sandbox_service.generate_mock_accounts(5)
        
        for account in accounts:
            assert isinstance(account.metadata, dict)
            assert account.metadata['sandbox'] is True
            assert account.metadata['mock_data'] is True
            assert 'test_scenario' in account.metadata
            assert account.metadata['test_scenario'].startswith('scenario_')
    
    @pytest.mark.asyncio
    async def test_transaction_data_types(self, sandbox_service):
        """Test that generated transactions have correct data types"""
        account_ids = ['acc1', 'acc2']
        transactions = await sandbox_service.generate_mock_transactions(account_ids, 5)
        
        for transaction in transactions:
            # Check that numeric fields are strings (as per API spec)
            assert isinstance(transaction.amount, str)
            assert isinstance(transaction.amount_usd, str)
            assert isinstance(transaction.fee, str)
            assert isinstance(transaction.fee_usd, str)
            
            # Check that risk_score is float
            assert isinstance(transaction.risk_score, float)
            
            # Check that dates are datetime objects
            assert isinstance(transaction.created_at, datetime)
            assert isinstance(transaction.updated_at, datetime)
            assert isinstance(transaction.ledger_time, datetime)
    
    @pytest.mark.asyncio
    async def test_kyc_verification_data_types(self, sandbox_service):
        """Test that generated KYC verifications have correct data types"""
        account_ids = ['acc1', 'acc2']
        verifications = await sandbox_service.generate_mock_kyc_verifications(account_ids, 3)
        
        for verification in verifications:
            # Check that dates are datetime objects
            assert isinstance(verification.created_at, datetime)
            assert isinstance(verification.updated_at, datetime)
            
            # Check optional datetime fields
            if verification.verified_at:
                assert isinstance(verification.verified_at, datetime)
            if verification.expires_at:
                assert isinstance(verification.expires_at, datetime)
            
            # Check optional numeric fields
            if verification.verification_score:
                assert isinstance(verification.verification_score, float)
    
    @pytest.mark.asyncio
    async def test_compliance_flag_data_types(self, sandbox_service):
        """Test that generated compliance flags have correct data types"""
        entity_ids = ['entity1', 'entity2']
        flags = await sandbox_service.generate_mock_compliance_flags(entity_ids, 3)
        
        for flag in flags:
            # Check that dates are datetime objects
            assert isinstance(flag.created_at, datetime)
            assert isinstance(flag.updated_at, datetime)
            
            # Check optional datetime fields
            if flag.resolved_at:
                assert isinstance(flag.resolved_at, datetime)
            
            # Check optional numeric fields
            if flag.risk_score:
                assert isinstance(flag.risk_score, float)
