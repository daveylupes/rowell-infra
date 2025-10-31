-- Migration: Add developer, project, and API key models
-- Date: 2025-01-15

-- Create developers table
CREATE TABLE IF NOT EXISTS developers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company VARCHAR(255),
    role VARCHAR(100),
    country_code VARCHAR(3),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    developer_id UUID NOT NULL REFERENCES developers(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    primary_network VARCHAR(20) DEFAULT 'stellar',
    environment VARCHAR(20) DEFAULT 'testnet',
    webhook_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create api_keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    developer_id UUID NOT NULL REFERENCES developers(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    key_name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    key_prefix VARCHAR(20) NOT NULL,
    permissions JSONB NOT NULL DEFAULT '[]',
    rate_limit INTEGER DEFAULT 1000,
    is_active BOOLEAN DEFAULT TRUE,
    last_used TIMESTAMP WITH TIME ZONE,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Create developer_sessions table
CREATE TABLE IF NOT EXISTS developer_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    developer_id UUID NOT NULL REFERENCES developers(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add project_id column to accounts table
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS project_id UUID REFERENCES projects(id);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_developers_email ON developers(email);
CREATE INDEX IF NOT EXISTS idx_projects_developer_id ON projects(developer_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_project_id ON api_keys(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON developer_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_developer_id ON developer_sessions(developer_id);
CREATE INDEX IF NOT EXISTS idx_accounts_project_id ON accounts(project_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_developers_updated_at BEFORE UPDATE ON developers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO developers (email, first_name, last_name, company, role, country_code, is_verified) VALUES
('demo@rowell-infra.com', 'Demo', 'Developer', 'Rowell Infra', 'Developer', 'NG', TRUE)
ON CONFLICT (email) DO NOTHING;

-- Get the demo developer ID
DO $$
DECLARE
    demo_dev_id UUID;
    demo_project_id UUID;
BEGIN
    SELECT id INTO demo_dev_id FROM developers WHERE email = 'demo@rowell-infra.com';
    
    -- Create a demo project
    INSERT INTO projects (developer_id, name, description, primary_network, environment)
    VALUES (demo_dev_id, 'Demo Project', 'Demo project for testing', 'stellar', 'testnet')
    ON CONFLICT DO NOTHING
    RETURNING id INTO demo_project_id;
    
    -- If no conflict, create a demo API key
    IF demo_project_id IS NOT NULL THEN
        INSERT INTO api_keys (developer_id, project_id, key_name, key_hash, key_prefix, permissions)
        VALUES (
            demo_dev_id,
            demo_project_id,
            'Demo API Key',
            'demo_hash_' || demo_project_id,
            'ri_demo_',
            '["accounts:read", "accounts:write", "transfers:read", "transfers:write"]'::jsonb
        );
    END IF;
END $$;
