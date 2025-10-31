-- Initialize Rowell Infra database
-- This script runs when the PostgreSQL container starts for the first time

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database if it doesn't exist (though it should be created by POSTGRES_DB)
-- This is just a safety measure

-- Set timezone
SET timezone = 'UTC';

-- Create indexes for better performance (these will be created by SQLAlchemy models)
-- But we can add some additional indexes here if needed

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE rowell_infra TO rowell;
