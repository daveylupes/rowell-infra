"""
Seed Demo Data for Hackathon Presentation
Creates realistic demo data with substantial balances and transaction volumes
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
import random

from api.core.database import AsyncSessionLocal, engine
from api.models.account import Account, AccountBalance
from api.models.transaction import Transaction
import structlog

logger = structlog.get_logger()


# Demo account configurations
DEMO_ACCOUNTS = [
    # Hedera Accounts (High balances for remittance use case)
    {"network": "hedera", "environment": "testnet", "country_code": "NG", "region": "west_africa", "account_type": "user", "balance": "1500.00", "asset": "HBAR"},
    {"network": "hedera", "environment": "testnet", "country_code": "KE", "region": "east_africa", "account_type": "user", "balance": "2500.00", "asset": "HBAR"},
    {"network": "hedera", "environment": "testnet", "country_code": "ZA", "region": "southern_africa", "account_type": "merchant", "balance": "5000.00", "asset": "HBAR"},
    {"network": "hedera", "environment": "testnet", "country_code": "GH", "region": "west_africa", "account_type": "user", "balance": "1200.00", "asset": "HBAR"},
    {"network": "hedera", "environment": "testnet", "country_code": "UG", "region": "east_africa", "account_type": "user", "balance": "800.00", "asset": "HBAR"},
    
    # Stellar Accounts (High balances)
    {"network": "stellar", "environment": "testnet", "country_code": "NG", "region": "west_africa", "account_type": "user", "balance": "15000.00", "asset": "XLM"},
    {"network": "stellar", "environment": "testnet", "country_code": "KE", "region": "east_africa", "account_type": "merchant", "balance": "20000.00", "asset": "XLM"},
    {"network": "stellar", "environment": "testnet", "country_code": "ZA", "region": "southern_africa", "account_type": "anchor", "balance": "30000.00", "asset": "XLM"},
    {"network": "stellar", "environment": "testnet", "country_code": "GH", "region": "west_africa", "account_type": "user", "balance": "10000.00", "asset": "XLM"},
    {"network": "stellar", "environment": "testnet", "country_code": "UG", "region": "east_africa", "account_type": "user", "balance": "12000.00", "asset": "XLM"},
    
    # USDC Stablecoin Accounts (for stablecoin adoption metrics)
    {"network": "hedera", "environment": "testnet", "country_code": "NG", "region": "west_africa", "account_type": "user", "balance": "50000.00", "asset": "USDC"},
    {"network": "hedera", "environment": "testnet", "country_code": "KE", "region": "east_africa", "account_type": "user", "balance": "35000.00", "asset": "USDC"},
]


# Remittance flow configurations
REMITTANCE_FLOWS = [
    {"from_country": "NG", "to_country": "KE", "volume_usd": 50000, "transaction_count": 250, "asset": "USDC"},
    {"from_country": "KE", "to_country": "UG", "volume_usd": 30000, "transaction_count": 150, "asset": "USDC"},
    {"from_country": "ZA", "to_country": "NG", "volume_usd": 25000, "transaction_count": 100, "asset": "USDC"},
    {"from_country": "GH", "to_country": "KE", "volume_usd": 20000, "transaction_count": 80, "asset": "HBAR"},
    {"from_country": "NG", "to_country": "GH", "volume_usd": 15000, "transaction_count": 75, "asset": "XLM"},
]


async def generate_mock_account_id(network: str, index: int) -> str:
    """Generate a mock account ID for demo purposes"""
    if network == "hedera":
        # Hedera format: 0.0.1234567
        base = 1000000 + index
        return f"0.0.{base}"
    else:
        # Stellar format: G followed by base32 encoded data
        # For demo, use a simpler approach
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
        encoded = "".join(random.choices(chars, k=56))
        return f"G{encoded}"


async def create_demo_accounts(db: AsyncSession) -> list[Account]:
    """Create demo accounts with realistic data"""
    logger.info("Creating demo accounts")
    accounts = []
    
    for idx, account_config in enumerate(DEMO_ACCOUNTS):
        account_id = await generate_mock_account_id(account_config["network"], idx + 1)
        
        # Check if account already exists
        result = await db.execute(
            select(Account).where(Account.account_id == account_id)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            logger.info(f"Account {account_id} already exists, skipping")
            accounts.append(existing)
            continue
        
        account = Account(
            account_id=account_id,
            network=account_config["network"],
            environment=account_config["environment"],
            account_type=account_config["account_type"],
            country_code=account_config["country_code"],
            region=account_config["region"],
            is_active=True,
            is_verified=True,
            is_compliant=True,
            kyc_status="verified",
            created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90)),
            updated_at=datetime.now(timezone.utc),
            last_activity=datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 24)),
        )
        
        db.add(account)
        accounts.append(account)
        
        logger.info(
            f"Created demo account",
            account_id=account_id,
            network=account_config["network"],
            country=account_config["country_code"]
        )
    
    await db.commit()
    logger.info(f"Created {len(accounts)} demo accounts")
    return accounts


async def create_demo_balances(db: AsyncSession, accounts: list[Account]):
    """Create demo account balances"""
    logger.info("Creating demo account balances")
    
    for account, config in zip(accounts, DEMO_ACCOUNTS):
        asset_code = config["asset"]
        balance = config["balance"]
        
        # Calculate USD value (rough estimates)
        if asset_code == "HBAR":
            balance_usd = str(float(balance) * 0.05)  # ~$0.05 per HBAR
        elif asset_code == "XLM":
            balance_usd = str(float(balance) * 0.10)  # ~$0.10 per XLM
        elif asset_code == "USDC":
            balance_usd = balance  # USDC is 1:1 with USD
        
        # Check if balance already exists
        result = await db.execute(
            select(AccountBalance).where(
                AccountBalance.account_id == account.account_id,
                AccountBalance.asset_code == asset_code
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.balance = balance
            existing.balance_usd = balance_usd
            existing.updated_at = datetime.now(timezone.utc)
        else:
            balance_record = AccountBalance(
                account_id=account.account_id,
                network=account.network,
                asset_code=asset_code,
                asset_issuer=None if asset_code in ["HBAR", "XLM"] else "USDC_ISSUER",
                asset_type="native" if asset_code in ["HBAR", "XLM"] else "credit_alphanum4",
                balance=balance,
                balance_usd=balance_usd,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            db.add(balance_record)
        
        logger.info(
            f"Created balance",
            account_id=account.account_id,
            asset=asset_code,
            balance=balance
        )
    
    await db.commit()
    logger.info("Demo balances created")


async def create_demo_transactions(db: AsyncSession, accounts: list[Account]):
    """Create demo transactions showing remittance flows"""
    logger.info("Creating demo transactions")
    
    transactions_created = 0
    
    # Group accounts by country
    accounts_by_country = {}
    for account in accounts:
        country = account.country_code
        if country not in accounts_by_country:
            accounts_by_country[country] = []
        accounts_by_country[country].append(account)
    
    for flow_config in REMITTANCE_FLOWS:
        from_country = flow_config["from_country"]
        to_country = flow_config["to_country"]
        volume_usd = flow_config["volume_usd"]
        transaction_count = flow_config["transaction_count"]
        asset_code = flow_config["asset"]
        
        from_accounts = accounts_by_country.get(from_country, [])
        to_accounts = accounts_by_country.get(to_country, [])
        
        if not from_accounts or not to_accounts:
            logger.warning(
                f"No accounts found for remittance flow",
                from_country=from_country,
                to_country=to_country
            )
            continue
        
        # Calculate average transaction amount
        avg_amount_usd = volume_usd / transaction_count
        
        # Create transactions
        for i in range(transaction_count):
            from_account = random.choice(from_accounts)
            to_account = random.choice(to_accounts)
            
            # Skip if same account
            if from_account.account_id == to_account.account_id:
                continue
            
            # Convert USD to asset amount
            if asset_code == "USDC":
                amount = str(round(avg_amount_usd * (0.8 + random.random() * 0.4), 2))  # ±20% variance
                amount_usd = amount
            elif asset_code == "HBAR":
                amount = str(round(avg_amount_usd / 0.05 * (0.8 + random.random() * 0.4), 2))
                amount_usd = str(round(float(amount) * 0.05, 2))
            else:  # XLM
                amount = str(round(avg_amount_usd / 0.10 * (0.8 + random.random() * 0.4), 2))
                amount_usd = str(round(float(amount) * 0.10, 2))
            
            # Determine network from accounts
            network = from_account.network
            environment = from_account.environment
            
            # Generate transaction hash
            tx_hash = f"{network}_{random.randint(1000000, 9999999)}_{i}_{int(datetime.now().timestamp())}"
            
            # Random status (mostly success, some pending)
            status = "success" if random.random() > 0.1 else "pending"
            
            # Random timestamp within last 30 days
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            created_at = datetime.now(timezone.utc) - timedelta(days=days_ago, hours=hours_ago)
            
            # Check if transaction already exists
            result = await db.execute(
                select(Transaction).where(Transaction.transaction_hash == tx_hash)
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                continue
            
            transaction = Transaction(
                transaction_hash=tx_hash,
                network=network,
                environment=environment,
                transaction_type="payment",
                status=status,
                from_account=from_account.account_id,
                to_account=to_account.account_id,
                asset_code=asset_code,
                asset_issuer=None if asset_code in ["HBAR", "XLM"] else "USDC_ISSUER",
                amount=amount,
                amount_usd=amount_usd,
                from_country=from_country,
                to_country=to_country,
                from_region=from_account.region,
                to_region=to_account.region,
                memo=f"Remittance {from_country} → {to_country}",
                fee="0.001" if network == "hedera" else "0.00001",
                fee_usd="0.00005" if network == "hedera" else "0.0000001",
                created_at=created_at,
            )
            
            db.add(transaction)
            transactions_created += 1
            
            if transactions_created % 50 == 0:
                await db.commit()
                logger.info(f"Created {transactions_created} transactions so far...")
    
    await db.commit()
    logger.info(f"Created {transactions_created} demo transactions")


async def seed_demo_data():
    """Main function to seed all demo data"""
    logger.info("Starting demo data seeding")
    
    async with AsyncSessionLocal() as db:
        try:
            # Create demo accounts
            accounts = await create_demo_accounts(db)
            
            # Create demo balances
            await create_demo_balances(db, accounts)
            
            # Create demo transactions
            await create_demo_transactions(db, accounts)
            
            logger.info("✅ Demo data seeding completed successfully!")
            print("\n" + "="*60)
            print("✅ Demo Data Seeding Complete!")
            print("="*60)
            print(f"📊 Accounts created: {len(accounts)}")
            print(f"💰 Balances configured: {len(DEMO_ACCOUNTS)}")
            print(f"📈 Remittance flows: {len(REMITTANCE_FLOWS)}")
            print(f"💸 Total volume: ${sum(f['volume_usd'] for f in REMITTANCE_FLOWS):,.0f}")
            print("="*60 + "\n")
            
        except Exception as e:
            logger.error("Failed to seed demo data", error=str(e))
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_demo_data())

