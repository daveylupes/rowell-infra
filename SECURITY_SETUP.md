# Security Setup Guide

This guide covers the secure configuration of Rowell Infra, including credential management, environment variables, and security best practices.

## 🔒 Security Overview

Rowell Infra implements multiple layers of security:

- **Environment-based Configuration**: Sensitive data stored in environment variables
- **Credential Isolation**: Local credentials separate from repository
- **Git Ignore Protection**: Sensitive files excluded from version control
- **Template-based Setup**: Secure credential setup process

## 🚨 Critical Security Notes

### ⚠️ NEVER COMMIT SENSITIVE DATA

The following files contain sensitive information and are **NEVER** committed to the repository:

- `.env.local` - Local environment variables with credentials
- `*.key` - Private key files
- `*.pem` - Certificate files
- `secrets/` - Any secrets directory
- `.secrets/` - Hidden secrets directory

### ✅ Safe to Commit

These files are safe to commit as they contain no sensitive data:

- `env.local.template` - Template with placeholder values
- `.env` - Default configuration (no real credentials)
- `*.example` - Example configuration files
- Documentation and code files

## 🔑 Credential Management

### 1. Hedera Testnet Credentials

**Getting Credentials:**
1. Visit [Hedera Portal](https://portal.hedera.com/)
2. Create an account or sign in
3. Go to "Testnet" section
4. Create a new testnet account
5. Copy the Account ID and Private Key

**Setting Up Credentials:**
```bash
# Create local environment file
python setup_credentials.py create

# Edit .env.local with your actual credentials
# HEDERA_TESTNET_OPERATOR_ID=0.0.1234567
# HEDERA_TESTNET_OPERATOR_KEY=302e020100300506032b657004220420...

# Verify setup
python setup_credentials.py check
```

### 2. Database Credentials

**Development:**
```bash
# PostgreSQL (default)
DATABASE_URL=postgresql+asyncpg://rowell:rowell@localhost:5433/rowell_infra

# SQLite (alternative)
DATABASE_URL=sqlite+aiosqlite:///./rowell_infra.db
```

**Production:**
```bash
# Use strong passwords and SSL
DATABASE_URL=postgresql+asyncpg://user:strong_password@host:5432/database?sslmode=require
```

### 3. Security Keys

**Development:**
```bash
SECRET_KEY=your-secret-key-change-in-production
WEBHOOK_SECRET=your-webhook-secret
```

**Production:**
```bash
# Generate strong, random keys
SECRET_KEY=$(openssl rand -hex 32)
WEBHOOK_SECRET=$(openssl rand -hex 32)
```

## 🛠️ Setup Tools

### Credential Setup Script

```bash
# Create local environment file
python setup_credentials.py create

# Check credential status
python setup_credentials.py status

# Verify configuration
python setup_credentials.py check

# Get help for credentials
python setup_credentials.py help-credentials
```

### Database Configuration Switcher

```bash
# Switch to PostgreSQL
python switch_database.py postgresql

# Switch to SQLite
python switch_database.py sqlite

# Check current configuration
python switch_database.py status
```

## 📁 File Structure

```
rowell-infra/
├── .env                    # Default configuration (safe to commit)
├── .env.local             # Local credentials (NEVER commit)
├── env.local.template     # Template file (safe to commit)
├── .gitignore            # Protects sensitive files
├── setup_credentials.py  # Credential setup tool
└── switch_database.py    # Database configuration tool
```

## 🔧 Environment Variables

### Required for Hedera Integration

```bash
# Hedera Testnet Credentials
HEDERA_TESTNET_OPERATOR_ID=0.0.1234567
HEDERA_TESTNET_OPERATOR_KEY=302e020100300506032b657004220420...
```

### Database Configuration

```bash
# PostgreSQL (recommended for production)
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# SQLite (development only)
DATABASE_URL=sqlite+aiosqlite:///./database.db
```

### Security Configuration

```bash
# Application Security
SECRET_KEY=your-secret-key-here
WEBHOOK_SECRET=your-webhook-secret-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

### Stellar Configuration

```bash
# Stellar Network URLs
STELLAR_TESTNET_URL=https://horizon-testnet.stellar.org
STELLAR_MAINNET_URL=https://horizon.stellar.org
STELLAR_TESTNET_PASSPHRASE=Test SDF Network ; September 2015
STELLAR_MAINNET_PASSPHRASE=Public Global Stellar Network ; September 2015
```

## 🚀 Production Deployment

### Environment Setup

1. **Create Production Environment File:**
   ```bash
   # Create .env.production with production values
   cp env.local.template .env.production
   # Edit with production credentials
   ```

2. **Use Environment Variables:**
   ```bash
   # Set environment variables directly
   export HEDERA_TESTNET_OPERATOR_ID="0.0.1234567"
   export HEDERA_TESTNET_OPERATOR_KEY="302e020100300506032b657004220420..."
   ```

3. **Use Secret Management:**
   ```bash
   # AWS Secrets Manager
   aws secretsmanager get-secret-value --secret-id rowell-infra/hedera-credentials
   
   # HashiCorp Vault
   vault kv get -field=operator_id secret/rowell-infra/hedera
   ```

### Docker Deployment

```yaml
# docker-compose.prod.yml
services:
  api:
    environment:
      - HEDERA_TESTNET_OPERATOR_ID=${HEDERA_TESTNET_OPERATOR_ID}
      - HEDERA_TESTNET_OPERATOR_KEY=${HEDERA_TESTNET_OPERATOR_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env.production
```

## 🔍 Security Checklist

### Development Setup

- [ ] `.env.local` created with actual credentials
- [ ] `.env.local` added to `.gitignore`
- [ ] Template files contain no real credentials
- [ ] Database credentials configured
- [ ] Security keys generated
- [ ] Credential setup script tested

### Production Deployment

- [ ] Strong passwords generated
- [ ] SSL/TLS enabled for database
- [ ] Environment variables set securely
- [ ] Secret management system configured
- [ ] Access controls implemented
- [ ] Monitoring and logging enabled
- [ ] Backup and recovery procedures tested

### Code Review

- [ ] No hardcoded credentials in code
- [ ] All sensitive data in environment variables
- [ ] Template files safe to commit
- [ ] `.gitignore` properly configured
- [ ] Documentation updated
- [ ] Security tests passing

## 🧪 Testing Security

### Credential Validation

```bash
# Test credential setup
python setup_credentials.py check

# Test database connection
python setup_database.py status

# Test Hedera integration
python -c "from api.services.hedera_service import HederaService; print('Hedera service:', HederaService('testnet').has_operator)"
```

### Security Scanning

```bash
# Check for exposed credentials
grep -r "0x[0-9a-fA-F]\{64\}" . --exclude-dir=.git
grep -r "302e020100300506032b657004220420" . --exclude-dir=.git

# Verify .gitignore
git check-ignore .env.local
git check-ignore *.key
git check-ignore secrets/
```

## 🆘 Troubleshooting

### Common Issues

1. **Credentials Not Working:**
   ```bash
   # Check if .env.local exists
   ls -la .env.local
   
   # Verify credentials are set
   python setup_credentials.py status
   
   # Test Hedera connection
   python -c "from api.services.hedera_service import HederaService; HederaService('testnet')"
   ```

2. **Environment Variables Not Loading:**
   ```bash
   # Check file format
   cat .env.local
   
   # Verify no spaces around =
   # Correct: HEDERA_TESTNET_OPERATOR_ID=0.0.1234567
   # Wrong:   HEDERA_TESTNET_OPERATOR_ID = 0.0.1234567
   ```

3. **Git Ignore Not Working:**
   ```bash
   # Check if file is already tracked
   git ls-files | grep .env.local
   
   # Remove from tracking if needed
   git rm --cached .env.local
   ```

### Getting Help

- Check credential status: `python setup_credentials.py status`
- Verify database connection: `python setup_database.py status`
- Review security checklist above
- Check logs for error messages
- Ensure all environment variables are set correctly

## 📚 Additional Resources

- [Hedera Portal](https://portal.hedera.com/) - Get testnet credentials
- [Environment Variables Best Practices](https://12factor.net/config)
- [Git Ignore Documentation](https://git-scm.com/docs/gitignore)
- [Docker Secrets Management](https://docs.docker.com/engine/swarm/secrets/)

---

**🔒 Remember: Security is everyone's responsibility. When in doubt, ask for help rather than compromising security!**
