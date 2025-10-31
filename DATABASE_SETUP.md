# Database Setup Guide

This guide covers the complete PostgreSQL database setup for Rowell Infra, including migrations, management tools, and production deployment.

## 🏗️ Architecture Overview

Rowell Infra uses **PostgreSQL** as the primary database with the following components:

- **PostgreSQL 15**: Production-ready database with full ACID compliance
- **Alembic**: Database migration management
- **SQLAlchemy**: Async ORM with connection pooling
- **Docker**: Containerized database for development and production

## 📊 Database Schema

The database includes 19 tables organized into the following categories:

### Core Tables
- `accounts` - User and merchant accounts (Stellar/Hedera)
- `transactions` - Transaction records and analytics
- `account_balances` - Asset balance tracking
- `account_activity` - Activity analytics

### Developer Platform
- `developers` - Developer accounts and profiles
- `projects` - Developer projects
- `api_keys` - API key management
- `developer_sessions` - Session management

### Analytics & Compliance
- `payment_corridors` - Cross-border payment analytics
- `compliance_flags` - Compliance monitoring
- `kyc_verifications` - KYC/AML tracking
- `network_metrics` - Network performance metrics

### Additional Tables
- `transaction_events` - Real-time transaction tracking
- `merchant_activity` - Merchant analytics
- `remittance_flows` - Remittance tracking
- `stablecoin_adoption` - Stablecoin usage metrics
- `sanctions_list` - Sanctions screening

## 🚀 Quick Start

### 1. Start PostgreSQL
```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Verify it's running
docker-compose ps postgres
```

### 2. Switch to PostgreSQL Configuration
```bash
# Switch from SQLite to PostgreSQL
python switch_database.py postgresql

# Verify configuration
python switch_database.py status
```

### 3. Run Migrations
```bash
# Run all pending migrations
cd api && source venv/bin/activate
python manage_db.py migrate

# Or use alembic directly
alembic upgrade head
```

### 4. Verify Setup
```bash
# Check database status
python setup_database.py status
```

## 🛠️ Database Management Tools

### 1. Database Management Script (`api/manage_db.py`)

```bash
# Check database connection
python manage_db.py check

# Run migrations
python manage_db.py migrate

# Create new migration
python manage_db.py create-migration "Add new feature"

# Rollback migration
python manage_db.py rollback

# Show current version
python manage_db.py current

# Show migration history
python manage_db.py history
```

### 2. Database Setup Script (`setup_database.py`)

```bash
# Set up database with all tables
python setup_database.py setup

# Check database status
python setup_database.py status

# Reset database (WARNING: deletes all data!)
python setup_database.py reset
```

### 3. Database Configuration Switcher (`switch_database.py`)

```bash
# Switch to PostgreSQL
python switch_database.py postgresql

# Switch to SQLite (for development)
python switch_database.py sqlite

# Show current configuration
python switch_database.py status
```

## 🔄 Migration Workflow

### Creating Migrations

1. **Modify Models**: Update your SQLAlchemy models in `api/models/`
2. **Generate Migration**: 
   ```bash
   python manage_db.py create-migration "Description of changes"
   ```
3. **Review Migration**: Check the generated migration file in `api/alembic/versions/`
4. **Apply Migration**: 
   ```bash
   python manage_db.py migrate
   ```

### Migration Best Practices

- **Always review** auto-generated migrations before applying
- **Test migrations** on a copy of production data
- **Use descriptive names** for migration messages
- **Backup database** before major migrations
- **Run migrations** in a transaction when possible

## 🐳 Docker Configuration

### PostgreSQL Container
```yaml
postgres:
  image: postgres:15-alpine
  container_name: rowell-postgres
  environment:
    POSTGRES_DB: rowell_infra
    POSTGRES_USER: rowell
    POSTGRES_PASSWORD: rowell
  ports:
    - "5433:5432"  # External port 5433, internal 5432
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
```

### Connection Details
- **Host**: localhost
- **Port**: 5433 (external), 5432 (internal)
- **Database**: rowell_infra
- **Username**: rowell
- **Password**: rowell
- **URL**: `postgresql+asyncpg://rowell:rowell@localhost:5433/rowell_infra`

## 📈 Performance Optimization

### Connection Pooling
```python
# Configured in api/core/database.py
DATABASE_POOL_SIZE: int = 10
DATABASE_MAX_OVERFLOW: int = 20
```

### Indexes
The database includes comprehensive indexes for:
- Account lookups by network/environment
- Transaction queries by type/status
- Analytics queries by country/region
- API key authentication
- Session management

### Query Optimization
- Use async/await for all database operations
- Implement proper pagination for large result sets
- Use database-level aggregations for analytics
- Cache frequently accessed data in Redis

## 🔒 Security Considerations

### Database Security
- **Connection Encryption**: Use SSL in production
- **Access Control**: Limit database user permissions
- **Backup Encryption**: Encrypt database backups
- **Audit Logging**: Log all database access

### Application Security
- **SQL Injection Prevention**: Use parameterized queries
- **Connection String Security**: Store in environment variables
- **API Key Management**: Secure storage and rotation
- **Session Security**: Proper session management

## 🚀 Production Deployment

### Environment Variables
```bash
# Production database configuration
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30
```

### Migration Strategy
1. **Backup Production Database**
2. **Test Migrations on Staging**
3. **Schedule Maintenance Window**
4. **Run Migrations with Monitoring**
5. **Verify Application Functionality**

### Monitoring
- **Connection Pool Metrics**: Monitor active/idle connections
- **Query Performance**: Track slow queries
- **Migration Status**: Monitor alembic version
- **Database Size**: Track growth and cleanup

## 🧪 Testing

### Test Database Setup
```bash
# Use separate test database
DATABASE_URL=postgresql+asyncpg://rowell:rowell@localhost:5433/rowell_infra_test

# Run tests with test database
pytest tests/ --database-url=postgresql+asyncpg://rowell:rowell@localhost:5433/rowell_infra_test
```

### Test Data Management
- Use fixtures for consistent test data
- Clean up test data after each test
- Use transactions for test isolation
- Mock external dependencies

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Docker PostgreSQL Image](https://hub.docker.com/_/postgres)

## 🆘 Troubleshooting

### Common Issues

1. **Connection Refused**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps postgres
   
   # Check logs
   docker-compose logs postgres
   ```

2. **Migration Errors**
   ```bash
   # Check current version
   python manage_db.py current
   
   # Check migration history
   python manage_db.py history
   ```

3. **Permission Errors**
   ```bash
   # Check database permissions
   docker exec rowell-postgres psql -U rowell -d rowell_infra -c "\du"
   ```

4. **Configuration Issues**
   ```bash
   # Check current configuration
   python switch_database.py status
   
   # Verify environment variables
   python -c "from api.core.config import settings; print(settings.DATABASE_URL)"
   ```

### Getting Help

- Check the logs: `docker-compose logs postgres`
- Verify configuration: `python switch_database.py status`
- Test connection: `python manage_db.py check`
- Review migration status: `python manage_db.py current`

---

**🎉 Your PostgreSQL database is now production-ready with proper migrations, management tools, and comprehensive monitoring!**
