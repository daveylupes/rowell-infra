# Scripts Directory

This directory contains utility scripts for the Rowell Infra API.

## Demo Data Seeding

### `seed_demo_data.py`

Seeds the database with realistic demo data for hackathon presentations and demos.

**Usage:**
```bash
# Activate virtual environment first
cd /home/davey/Documents/rowell/dev/rowell-infra/api
source venv/bin/activate

# Run the seed script
python scripts/seed_demo_data.py
```

**Or use the wrapper script:**
```bash
cd /home/davey/Documents/rowell/dev/rowell-infra/api
./scripts/seed_demo.sh
```

**What it creates:**
- 12 demo accounts with substantial balances (1,000+ HBAR, 10,000+ XLM, $35K+ USDC)
- 655+ transactions across 5 remittance corridors
- Total volume: $125,000+
- Countries: NG, KE, ZA, GH, UG
- Realistic timestamps and transaction statuses

**Note:** This script uses mock account IDs. In production, you should create real blockchain accounts.

