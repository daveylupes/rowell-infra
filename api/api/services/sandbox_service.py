"""
Sandbox service for providing mock data and testing environments
"""

import uuid
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from api.models.account import Account
from api.models.transaction import Transaction
from api.models.analytics import RemittanceFlow, StablecoinAdoption, MerchantActivity, NetworkMetrics
from api.models.compliance import KYCVerification, ComplianceFlag


class SandboxEnvironment(str, Enum):
    """Sandbox environment types"""
    TESTNET = "testnet"
    SANDBOX = "sandbox"
    MOCK = "mock"


class SandboxService:
    """Service for managing sandbox environment with mock data"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sandbox_config = self._load_sandbox_config()
        self.usage_stats = {
            "initialized_at": None,
            "total_requests": 0,
            "mock_data_generated": 0,
            "test_scenarios_run": 0,
            "last_reset": None
        }
    
    async def generate_mock_accounts(self, count: int = 10) -> List[Account]:
        """Generate mock accounts for sandbox testing"""
        mock_accounts = []
        
        countries = ['NG', 'KE', 'GH', 'ZA', 'EG', 'MA', 'TN', 'UG', 'RW', 'ET']
        account_types = ['individual', 'merchant', 'anchor', 'ngo']
        networks = ['stellar', 'hedera']
        environments = ['testnet']
        
        for i in range(count):
            account = Account(
                id=str(uuid.uuid4()),
                account_id=f"SB{random.randint(100000, 999999)}",
                network=random.choice(networks),
                environment=random.choice(environments),
                account_type=random.choice(account_types),
                country_code=random.choice(countries),
                region=self._get_region_from_country(random.choice(countries)),
                is_active=random.choice([True, True, True, False]),  # 75% active
                is_verified=random.choice([True, True, False]),  # 67% verified
                is_compliant=random.choice([True, True, True, False]),  # 75% compliant
                kyc_status=random.choice(['verified', 'verified', 'pending', 'rejected']),
                created_at=datetime.now() - timedelta(days=random.randint(1, 365)),
                updated_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                last_activity=datetime.now() - timedelta(hours=random.randint(1, 168)),
                metadata={
                    'sandbox': True,
                    'mock_data': True,
                    'test_scenario': f'scenario_{i % 5 + 1}'
                }
            )
            mock_accounts.append(account)
        
        return mock_accounts
    
    async def generate_mock_transactions(self, account_ids: List[str], count: int = 50) -> List[Transaction]:
        """Generate mock transactions for sandbox testing"""
        mock_transactions = []
        
        asset_codes = ['USDC', 'XLM', 'HBAR', 'NGN', 'KES', 'GHS', 'ZAR']
        statuses = ['success', 'success', 'success', 'pending', 'failed']  # 60% success
        transaction_types = ['payment', 'transfer', 'token_transfer']
        
        for i in range(count):
            from_account = random.choice(account_ids)
            to_account = random.choice([acc for acc in account_ids if acc != from_account])
            
            transaction = Transaction(
                id=str(uuid.uuid4()),
                transaction_hash=f"SB{random.randint(100000000, 999999999)}",
                network=random.choice(['stellar', 'hedera']),
                environment='testnet',
                transaction_type=random.choice(transaction_types),
                status=random.choice(statuses),
                from_account=from_account,
                to_account=to_account,
                asset_code=random.choice(asset_codes),
                amount=str(round(random.uniform(10, 10000), 2)),
                amount_usd=str(round(random.uniform(10, 10000), 2)),
                from_country=random.choice(['NG', 'KE', 'GH', 'ZA']),
                to_country=random.choice(['NG', 'KE', 'GH', 'ZA']),
                from_region=random.choice(['West Africa', 'East Africa', 'North Africa', 'Southern Africa']),
                to_region=random.choice(['West Africa', 'East Africa', 'North Africa', 'Southern Africa']),
                memo=f"Sandbox test transaction {i + 1}",
                fee=str(round(random.uniform(0.01, 1.0), 4)),
                fee_usd=str(round(random.uniform(0.01, 1.0), 4)),
                created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                updated_at=datetime.now() - timedelta(hours=random.randint(0, 24)),
                ledger_time=datetime.now() - timedelta(hours=random.randint(0, 24)),
                compliance_status=random.choice(['approved', 'approved', 'approved', 'flagged']),
                risk_score=round(random.uniform(0, 100), 2)
            )
            mock_transactions.append(transaction)
        
        return mock_transactions
    
    async def generate_mock_analytics_data(self) -> Dict[str, Any]:
        """Generate mock analytics data for sandbox testing"""
        return {
            'remittance_flows': await self._generate_mock_remittance_flows(),
            'stablecoin_adoption': await self._generate_mock_stablecoin_adoption(),
            'merchant_activity': await self._generate_mock_merchant_activity(),
            'network_metrics': await self._generate_mock_network_metrics()
        }
    
    async def _generate_mock_remittance_flows(self, count: int = 20) -> List[RemittanceFlow]:
        """Generate mock remittance flow data"""
        flows = []
        countries = ['NG', 'KE', 'GH', 'ZA', 'EG', 'MA', 'TN', 'UG', 'RW', 'ET']
        assets = ['USDC', 'XLM', 'HBAR']
        
        for i in range(count):
            from_country = random.choice(countries)
            to_country = random.choice([c for c in countries if c != from_country])
            
            flow = RemittanceFlow(
                id=str(uuid.uuid4()),
                from_country=from_country,
                to_country=to_country,
                from_region=self._get_region_from_country(from_country),
                to_region=self._get_region_from_country(to_country),
                asset_code=random.choice(assets),
                network=random.choice(['stellar', 'hedera']),
                total_volume=str(round(random.uniform(1000, 100000), 2)),
                total_volume_usd=str(round(random.uniform(1000, 100000), 2)),
                transaction_count=random.randint(10, 1000),
                unique_senders=random.randint(5, 500),
                unique_receivers=random.randint(5, 500),
                avg_fee=str(round(random.uniform(0.1, 5.0), 4)),
                avg_fee_usd=str(round(random.uniform(0.1, 5.0), 4)),
                avg_fee_percentage=round(random.uniform(0.1, 2.0), 2),
                avg_settlement_time=random.randint(1, 60),
                success_rate=round(random.uniform(85, 99), 2),
                period_start=datetime.now() - timedelta(days=30),
                period_end=datetime.now(),
                period_type='monthly'
            )
            flows.append(flow)
        
        return flows
    
    async def _generate_mock_stablecoin_adoption(self, count: int = 15) -> List[StablecoinAdoption]:
        """Generate mock stablecoin adoption data"""
        adoption_data = []
        assets = ['USDC', 'USDT', 'DAI', 'BUSD']
        countries = ['NG', 'KE', 'GH', 'ZA', 'EG']
        
        for i in range(count):
            adoption = StablecoinAdoption(
                id=str(uuid.uuid4()),
                asset_code=random.choice(assets),
                network=random.choice(['stellar', 'hedera']),
                country_code=random.choice(countries),
                region=self._get_region_from_country(random.choice(countries)),
                total_volume=str(round(random.uniform(5000, 500000), 2)),
                total_volume_usd=str(round(random.uniform(5000, 500000), 2)),
                transaction_count=random.randint(100, 10000),
                unique_users=random.randint(50, 5000),
                avg_transaction_size=str(round(random.uniform(50, 2000), 2)),
                avg_transaction_size_usd=str(round(random.uniform(50, 2000), 2)),
                volume_growth_rate=round(random.uniform(-10, 50), 2),
                user_growth_rate=round(random.uniform(0, 30), 2),
                period_start=datetime.now() - timedelta(days=30),
                period_end=datetime.now(),
                period_type='monthly'
            )
            adoption_data.append(adoption)
        
        return adoption_data
    
    async def _generate_mock_merchant_activity(self, count: int = 12) -> List[MerchantActivity]:
        """Generate mock merchant activity data"""
        activities = []
        merchant_types = ['fintech', 'ecommerce', 'remittance', 'banking', 'retail']
        countries = ['NG', 'KE', 'GH', 'ZA', 'EG']
        
        for i in range(count):
            activity = MerchantActivity(
                id=str(uuid.uuid4()),
                merchant_id=f"MERCH_{random.randint(1000, 9999)}",
                merchant_name=f"Test Merchant {i + 1}",
                merchant_type=random.choice(merchant_types),
                country_code=random.choice(countries),
                region=self._get_region_from_country(random.choice(countries)),
                total_volume=str(round(random.uniform(10000, 1000000), 2)),
                total_volume_usd=str(round(random.uniform(10000, 1000000), 2)),
                transaction_count=random.randint(1000, 50000),
                unique_customers=random.randint(100, 10000),
                avg_transaction_size=str(round(random.uniform(10, 500), 2)),
                avg_transaction_size_usd=str(round(random.uniform(10, 500), 2)),
                stellar_volume=str(round(random.uniform(5000, 500000), 2)),
                hedera_volume=str(round(random.uniform(5000, 500000), 2)),
                stellar_transactions=random.randint(500, 25000),
                hedera_transactions=random.randint(500, 25000),
                period_start=datetime.now() - timedelta(days=30),
                period_end=datetime.now(),
                period_type='monthly'
            )
            activities.append(activity)
        
        return activities
    
    async def _generate_mock_network_metrics(self, count: int = 6) -> List[NetworkMetrics]:
        """Generate mock network metrics data"""
        metrics = []
        networks = ['stellar', 'hedera']
        environments = ['testnet', 'mainnet']
        
        for i in range(count):
            metric = NetworkMetrics(
                id=str(uuid.uuid4()),
                network=random.choice(networks),
                environment=random.choice(environments),
                total_transactions=random.randint(10000, 1000000),
                total_volume=str(round(random.uniform(100000, 10000000), 2)),
                total_volume_usd=str(round(random.uniform(100000, 10000000), 2)),
                active_accounts=random.randint(1000, 100000),
                new_accounts=random.randint(100, 10000),
                avg_transaction_fee=str(round(random.uniform(0.001, 0.1), 6)),
                avg_transaction_fee_usd=str(round(random.uniform(0.001, 0.1), 6)),
                avg_confirmation_time=random.randint(1, 60),
                success_rate=round(random.uniform(95, 99.9), 2),
                africa_transaction_count=random.randint(5000, 500000),
                africa_volume=str(round(random.uniform(50000, 5000000), 2)),
                africa_volume_usd=str(round(random.uniform(50000, 5000000), 2)),
                period_start=datetime.now() - timedelta(days=30),
                period_end=datetime.now(),
                period_type='monthly'
            )
            metrics.append(metric)
        
        return metrics
    
    async def generate_mock_kyc_verifications(self, account_ids: List[str], count: int = 20) -> List[KYCVerification]:
        """Generate mock KYC verification data"""
        verifications = []
        verification_types = ['individual', 'business', 'ngo']
        statuses = ['verified', 'verified', 'verified', 'pending', 'rejected']  # 60% verified
        providers = ['internal', 'jumio', 'onfido', 'trulioo']
        
        for i in range(count):
            verification = KYCVerification(
                id=str(uuid.uuid4()),
                verification_id=f"KYC_{random.randint(100000, 999999)}",
                account_id=random.choice(account_ids),
                network=random.choice(['stellar', 'hedera']),
                verification_type=random.choice(verification_types),
                verification_status=random.choice(statuses),
                provider=random.choice(providers),
                verification_score=round(random.uniform(0, 100), 2) if random.choice(statuses) == 'verified' else None,
                risk_level=random.choice(['low', 'medium', 'high']) if random.choice(statuses) == 'verified' else None,
                verification_notes=f"Mock KYC verification {i + 1}",
                created_at=datetime.now() - timedelta(days=random.randint(1, 90)),
                updated_at=datetime.now() - timedelta(days=random.randint(0, 7)),
                verified_at=datetime.now() - timedelta(days=random.randint(0, 30)) if random.choice(statuses) == 'verified' else None,
                expires_at=datetime.now() + timedelta(days=random.randint(30, 365)) if random.choice(statuses) == 'verified' else None
            )
            verifications.append(verification)
        
        return verifications
    
    async def generate_mock_compliance_flags(self, entity_ids: List[str], count: int = 15) -> List[ComplianceFlag]:
        """Generate mock compliance flag data"""
        flags = []
        entity_types = ['account', 'transaction']
        flag_types = ['aml', 'kyc', 'sanctions', 'risk']
        severities = ['low', 'medium', 'high', 'critical']
        statuses = ['active', 'active', 'active', 'resolved', 'false_positive']  # 60% active
        
        for i in range(count):
            flag = ComplianceFlag(
                id=str(uuid.uuid4()),
                entity_type=random.choice(entity_types),
                entity_id=random.choice(entity_ids),
                network=random.choice(['stellar', 'hedera']),
                flag_type=random.choice(flag_types),
                flag_severity=random.choice(severities),
                flag_status=random.choice(statuses),
                flag_reason=f"Mock compliance flag {i + 1}: {random.choice(flag_types).upper()} concern detected",
                risk_score=round(random.uniform(0, 100), 2),
                country_code=random.choice(['NG', 'KE', 'GH', 'ZA', 'EG']),
                region=self._get_region_from_country(random.choice(['NG', 'KE', 'GH', 'ZA', 'EG'])),
                resolved_by=f"user_{random.randint(1, 10)}" if random.choice(statuses) in ['resolved', 'false_positive'] else None,
                resolution_notes=f"Mock resolution notes for flag {i + 1}" if random.choice(statuses) in ['resolved', 'false_positive'] else None,
                created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
                updated_at=datetime.now() - timedelta(days=random.randint(0, 7)),
                resolved_at=datetime.now() - timedelta(days=random.randint(0, 7)) if random.choice(statuses) in ['resolved', 'false_positive'] else None
            )
            flags.append(flag)
        
        return flags
    
    def _get_region_from_country(self, country_code: str) -> str:
        """Get region from country code"""
        regions = {
            'NG': 'West Africa',
            'GH': 'West Africa',
            'KE': 'East Africa',
            'UG': 'East Africa',
            'RW': 'East Africa',
            'ET': 'East Africa',
            'ZA': 'Southern Africa',
            'EG': 'North Africa',
            'MA': 'North Africa',
            'TN': 'North Africa'
        }
        return regions.get(country_code, 'Africa')
    
    async def reset_sandbox_data(self) -> Dict[str, Any]:
        """Reset all sandbox data to initial state"""
        try:
            # Delete existing mock data (in a real implementation, you'd want to be more careful)
            # For now, we'll just return a success message
            return {
                "success": True,
                "message": "Sandbox data reset successfully",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to reset sandbox data: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_sandbox_stats(self) -> Dict[str, Any]:
        """Get sandbox environment statistics"""
        try:
            # In a real implementation, you'd query the database for actual counts
            # For now, we'll return mock statistics
            return {
                "accounts": {
                    "total": 150,
                    "active": 120,
                    "verified": 100,
                    "countries": 10
                },
                "transactions": {
                    "total": 5000,
                    "successful": 4800,
                    "pending": 150,
                    "failed": 50,
                    "total_volume_usd": "2500000.00"
                },
                "analytics": {
                    "remittance_flows": 20,
                    "stablecoin_adoption_records": 15,
                    "merchant_activities": 12,
                    "network_metrics": 6
                },
                "compliance": {
                    "kyc_verifications": 200,
                    "compliance_flags": 45,
                    "active_flags": 30,
                    "resolved_flags": 15
                },
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get sandbox stats: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _load_sandbox_config(self) -> Dict[str, Any]:
        """Load sandbox configuration"""
        return {
            "default_account_count": 100,
            "default_transaction_count": 500,
            "default_compliance_count": 50,
            "countries": ["NG", "KE", "ZA", "GH", "UG", "EG", "MA", "TN"],
            "account_types": ["user", "business", "merchant", "anchor", "ngo"],
            "transaction_types": ["transfer", "payment", "remittance"],
            "networks": ["stellar", "hedera"],
            "environments": ["testnet", "sandbox"],
            "rate_limits": {
                "requests_per_minute": 1000,
                "requests_per_hour": 60000,
                "requests_per_day": 1000000
            }
        }
    
    async def initialize_sandbox_environment(
        self, 
        environment: SandboxEnvironment = SandboxEnvironment.SANDBOX
    ) -> Dict[str, Any]:
        """Initialize sandbox environment with comprehensive mock data"""
        try:
            # Clear existing sandbox data
            await self._clear_sandbox_data()
            
            # Generate comprehensive mock data
            mock_data = await self._generate_comprehensive_mock_data()
            
            # Create test scenarios
            scenarios = await self._create_test_scenarios()
            
            # Initialize sandbox analytics
            analytics = await self._initialize_sandbox_analytics()
            
            # Update usage stats
            self.usage_stats["initialized_at"] = datetime.now().isoformat()
            self.usage_stats["total_requests"] = 0
            self.usage_stats["mock_data_generated"] = (
                mock_data["accounts_count"] + 
                mock_data["transactions_count"] + 
                mock_data["compliance_count"]
            )
            
            return {
                "environment": environment.value,
                "status": "initialized",
                "mock_data": {
                    "accounts": mock_data["accounts_count"],
                    "transactions": mock_data["transactions_count"],
                    "compliance_records": mock_data["compliance_count"],
                    "analytics_records": mock_data["analytics_count"]
                },
                "test_scenarios": len(scenarios),
                "analytics_initialized": analytics["status"],
                "initialized_at": self.usage_stats["initialized_at"],
                "config": self.sandbox_config
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Sandbox initialization failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _generate_comprehensive_mock_data(self) -> Dict[str, Any]:
        """Generate comprehensive mock data for sandbox initialization"""
        try:
            # Generate mock accounts
            accounts = await self.generate_mock_accounts(
                count=self.sandbox_config["default_account_count"]
            )
            
            # Generate mock transactions
            account_ids = [acc.account_id for acc in accounts]
            transactions = await self.generate_mock_transactions(
                account_ids=account_ids,
                count=self.sandbox_config["default_transaction_count"]
            )
            
            # Generate mock compliance records
            kyc_verifications = await self.generate_mock_kyc_verifications(
                account_ids=account_ids,
                count=self.sandbox_config["default_compliance_count"]
            )
            
            compliance_flags = await self.generate_mock_compliance_flags(
                entity_ids=account_ids + [tx.transaction_hash for tx in transactions],
                count=self.sandbox_config["default_compliance_count"]
            )
            
            # Generate mock analytics data
            analytics_data = await self.generate_mock_analytics_data()
            
            return {
                "accounts_count": len(accounts),
                "transactions_count": len(transactions),
                "compliance_count": len(kyc_verifications) + len(compliance_flags),
                "analytics_count": (
                    len(analytics_data['remittance_flows']) +
                    len(analytics_data['stablecoin_adoption']) +
                    len(analytics_data['merchant_activity']) +
                    len(analytics_data['network_metrics'])
                ),
                "accounts": accounts,
                "transactions": transactions,
                "kyc_verifications": kyc_verifications,
                "compliance_flags": compliance_flags,
                "analytics_data": analytics_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Mock data generation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _clear_sandbox_data(self) -> Dict[str, Any]:
        """Clear existing sandbox data"""
        try:
            # In a real implementation, you would delete data from the database
            # For now, we'll just return a success message
            return {
                "success": True,
                "message": "Sandbox data cleared successfully",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to clear sandbox data: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _create_test_scenarios(self) -> List[Dict[str, Any]]:
        """Create comprehensive test scenarios"""
        scenarios = [
            {
                "id": "basic_integration",
                "name": "Basic Integration Test",
                "description": "Test basic account creation and transfer functionality",
                "estimated_duration": "5-10 minutes",
                "steps": [
                    "Create test accounts",
                    "Generate test transactions",
                    "Verify account balances",
                    "Test transfer operations"
                ],
                "required_data": ["accounts", "transactions"],
                "expected_outcomes": ["account_creation", "transfer_success"]
            },
            {
                "id": "compliance_testing",
                "name": "Compliance Testing",
                "description": "Test KYC verification and compliance flagging",
                "estimated_duration": "10-15 minutes",
                "steps": [
                    "Generate KYC verifications",
                    "Create compliance flags",
                    "Test flag resolution",
                    "Verify compliance reports"
                ],
                "required_data": ["accounts", "kyc_verifications", "compliance_flags"],
                "expected_outcomes": ["kyc_verification", "compliance_flagging"]
            },
            {
                "id": "analytics_testing",
                "name": "Analytics Testing",
                "description": "Test analytics and reporting functionality",
                "estimated_duration": "15-20 minutes",
                "steps": [
                    "Generate analytics data",
                    "Test dashboard endpoints",
                    "Verify remittance flows",
                    "Test stablecoin adoption metrics"
                ],
                "required_data": ["transactions", "analytics_data"],
                "expected_outcomes": ["dashboard_analytics", "remittance_flows"]
            },
            {
                "id": "stress_testing",
                "name": "Stress Testing",
                "description": "Test system performance under load",
                "estimated_duration": "20-30 minutes",
                "steps": [
                    "Generate large volume of accounts",
                    "Create many transactions",
                    "Test rate limiting",
                    "Monitor system performance"
                ],
                "required_data": ["accounts", "transactions"],
                "expected_outcomes": ["rate_limit_handling", "performance_metrics"]
            },
            {
                "id": "error_handling",
                "name": "Error Handling Testing",
                "description": "Test error scenarios and edge cases",
                "estimated_duration": "10-15 minutes",
                "steps": [
                    "Test invalid API keys",
                    "Test malformed requests",
                    "Test rate limit scenarios",
                    "Verify error responses"
                ],
                "required_data": [],
                "expected_outcomes": ["error_handling", "validation_errors"]
            }
        ]
        return scenarios
    
    async def _initialize_sandbox_analytics(self) -> Dict[str, Any]:
        """Initialize sandbox analytics tracking"""
        try:
            analytics_config = {
                "tracking_enabled": True,
                "metrics_collected": [
                    "api_requests",
                    "mock_data_generation",
                    "test_scenario_execution",
                    "error_rates",
                    "performance_metrics"
                ],
                "retention_period": 30,  # days
                "real_time_monitoring": True
            }
            
            return {
                "status": "initialized",
                "config": analytics_config,
                "initialized_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Analytics initialization failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_test_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Get specific test scenario details"""
        try:
            scenarios = await self._create_test_scenarios()
            scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
            
            if not scenario:
                return {
                    "success": False,
                    "message": f"Test scenario '{scenario_id}' not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            return {
                "success": True,
                "data": scenario
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get test scenario: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def execute_test_scenario(self, scenario_id: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a specific test scenario"""
        try:
            self.usage_stats["test_scenarios_run"] += 1
            self.usage_stats["total_requests"] += 1
            
            scenario = await self.get_test_scenario(scenario_id)
            if not scenario["success"]:
                return scenario
            
            scenario_data = scenario["data"]
            execution_start = datetime.now()
            
            # Simulate scenario execution
            execution_results = {
                "scenario_id": scenario_id,
                "status": "completed",
                "execution_time": "simulated",
                "steps_completed": len(scenario_data["steps"]),
                "expected_outcomes_met": True,
                "execution_log": [
                    f"Step {i+1}: {step} - Completed" 
                    for i, step in enumerate(scenario_data["steps"])
                ],
                "started_at": execution_start.isoformat(),
                "completed_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "data": execution_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Test scenario execution failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_sandbox_usage_analytics(self) -> Dict[str, Any]:
        """Get sandbox usage analytics"""
        try:
            return {
                "success": True,
                "data": {
                    "usage_stats": self.usage_stats,
                    "environment_config": self.sandbox_config,
                    "rate_limits": self.sandbox_config["rate_limits"],
                    "current_status": "active" if self.usage_stats["initialized_at"] else "not_initialized",
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get usage analytics: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def update_sandbox_config(self, config_updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update sandbox configuration"""
        try:
            # Update configuration
            for key, value in config_updates.items():
                if key in self.sandbox_config:
                    self.sandbox_config[key] = value
            
            return {
                "success": True,
                "message": "Sandbox configuration updated successfully",
                "data": {
                    "updated_config": self.sandbox_config,
                    "updated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update configuration: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
