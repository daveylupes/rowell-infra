-- Migration: Add User Authentication Models
-- Description: Create tables for user authentication, roles, and permissions
-- Date: 2024-12-19

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company VARCHAR(255),
    phone VARCHAR(20),
    country_code VARCHAR(2),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    password_changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create permissions table
CREATE TABLE IF NOT EXISTS permissions (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create user_roles junction table
CREATE TABLE IF NOT EXISTS user_roles (
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    role_id VARCHAR(36) REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    assigned_by VARCHAR(36) REFERENCES users(id),
    PRIMARY KEY (user_id, role_id)
);

-- Create role_permissions junction table
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id VARCHAR(36) REFERENCES roles(id) ON DELETE CASCADE,
    permission_id VARCHAR(36) REFERENCES permissions(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (role_id, permission_id)
);

-- Create user_sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    refresh_token VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create email_verifications table
CREATE TABLE IF NOT EXISTS email_verifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Create password_resets table
CREATE TABLE IF NOT EXISTS password_resets (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_is_verified ON users(is_verified);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(name);
CREATE INDEX IF NOT EXISTS idx_roles_is_active ON roles(is_active);

CREATE INDEX IF NOT EXISTS idx_permissions_name ON permissions(name);
CREATE INDEX IF NOT EXISTS idx_permissions_resource ON permissions(resource);
CREATE INDEX IF NOT EXISTS idx_permissions_action ON permissions(action);
CREATE INDEX IF NOT EXISTS idx_permissions_is_active ON permissions(is_active);

CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_session_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_user_sessions_refresh_token ON user_sessions(refresh_token);
CREATE INDEX IF NOT EXISTS idx_user_sessions_is_active ON user_sessions(is_active);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON user_sessions(expires_at);

CREATE INDEX IF NOT EXISTS idx_email_verifications_token ON email_verifications(token);
CREATE INDEX IF NOT EXISTS idx_email_verifications_user_id ON email_verifications(user_id);
CREATE INDEX IF NOT EXISTS idx_email_verifications_is_used ON email_verifications(is_used);
CREATE INDEX IF NOT EXISTS idx_email_verifications_expires_at ON email_verifications(expires_at);

CREATE INDEX IF NOT EXISTS idx_password_resets_token ON password_resets(token);
CREATE INDEX IF NOT EXISTS idx_password_resets_user_id ON password_resets(user_id);
CREATE INDEX IF NOT EXISTS idx_password_resets_is_used ON password_resets(is_used);
CREATE INDEX IF NOT EXISTS idx_password_resets_expires_at ON password_resets(expires_at);

-- Insert default roles
INSERT INTO roles (id, name, description, is_active) VALUES
    ('admin-role-id', 'admin', 'Full system access and management', TRUE),
    ('developer-role-id', 'developer', 'Project owner with development access', TRUE),
    ('viewer-role-id', 'viewer', 'Read-only access to assigned projects', TRUE),
    ('support-role-id', 'support', 'Customer support with compliance access', TRUE)
ON CONFLICT (name) DO NOTHING;

-- Insert default permissions
INSERT INTO permissions (id, name, resource, action, description, is_active) VALUES
    -- Admin permissions
    ('admin-all-permission-id', '*:*', '*', '*', 'All permissions', TRUE),
    ('users-read-permission-id', 'users:read', 'users', 'read', 'Read user information', TRUE),
    ('users-write-permission-id', 'users:write', 'users', 'write', 'Create and update users', TRUE),
    ('users-delete-permission-id', 'users:delete', 'users', 'delete', 'Delete users', TRUE),
    ('roles-read-permission-id', 'roles:read', 'roles', 'read', 'Read role information', TRUE),
    ('roles-write-permission-id', 'roles:write', 'roles', 'write', 'Create and update roles', TRUE),
    ('system-read-permission-id', 'system:read', 'system', 'read', 'Read system information', TRUE),
    ('system-write-permission-id', 'system:write', 'system', 'write', 'Modify system settings', TRUE),
    
    -- Developer permissions
    ('projects-read-permission-id', 'projects:read', 'projects', 'read', 'Read project information', TRUE),
    ('projects-write-permission-id', 'projects:write', 'projects', 'write', 'Create and update projects', TRUE),
    ('projects-delete-permission-id', 'projects:delete', 'projects', 'delete', 'Delete projects', TRUE),
    ('accounts-read-permission-id', 'accounts:read', 'accounts', 'read', 'Read account information', TRUE),
    ('accounts-write-permission-id', 'accounts:write', 'accounts', 'write', 'Create and update accounts', TRUE),
    ('transfers-read-permission-id', 'transfers:read', 'transfers', 'read', 'Read transfer information', TRUE),
    ('transfers-write-permission-id', 'transfers:write', 'transfers', 'write', 'Create and update transfers', TRUE),
    ('api-keys-read-permission-id', 'api_keys:read', 'api_keys', 'read', 'Read API key information', TRUE),
    ('api-keys-write-permission-id', 'api_keys:write', 'api_keys', 'write', 'Create and update API keys', TRUE),
    ('api-keys-delete-permission-id', 'api_keys:delete', 'api_keys', 'delete', 'Delete API keys', TRUE),
    ('analytics-read-permission-id', 'analytics:read', 'analytics', 'read', 'Read analytics data', TRUE),
    
    -- Viewer permissions
    ('viewer-projects-read-permission-id', 'projects:read', 'projects', 'read', 'Read project information', TRUE),
    ('viewer-accounts-read-permission-id', 'accounts:read', 'accounts', 'read', 'Read account information', TRUE),
    ('viewer-transfers-read-permission-id', 'transfers:read', 'transfers', 'read', 'Read transfer information', TRUE),
    ('viewer-analytics-read-permission-id', 'analytics:read', 'analytics', 'read', 'Read analytics data', TRUE),
    
    -- Support permissions
    ('support-users-read-permission-id', 'users:read', 'users', 'read', 'Read user information', TRUE),
    ('support-accounts-read-permission-id', 'accounts:read', 'accounts', 'read', 'Read account information', TRUE),
    ('support-transfers-read-permission-id', 'transfers:read', 'transfers', 'read', 'Read transfer information', TRUE),
    ('compliance-read-permission-id', 'compliance:read', 'compliance', 'read', 'Read compliance information', TRUE),
    ('compliance-write-permission-id', 'compliance:write', 'compliance', 'write', 'Update compliance information', TRUE),
    ('kyc-read-permission-id', 'kyc:read', 'kyc', 'read', 'Read KYC information', TRUE),
    ('kyc-write-permission-id', 'kyc:write', 'kyc', 'write', 'Update KYC information', TRUE)
ON CONFLICT (name) DO NOTHING;

-- Assign permissions to roles
-- Admin gets all permissions
INSERT INTO role_permissions (role_id, permission_id) VALUES
    ('admin-role-id', 'admin-all-permission-id'),
    ('admin-role-id', 'users-read-permission-id'),
    ('admin-role-id', 'users-write-permission-id'),
    ('admin-role-id', 'users-delete-permission-id'),
    ('admin-role-id', 'roles-read-permission-id'),
    ('admin-role-id', 'roles-write-permission-id'),
    ('admin-role-id', 'system-read-permission-id'),
    ('admin-role-id', 'system-write-permission-id'),
    ('admin-role-id', 'projects-read-permission-id'),
    ('admin-role-id', 'projects-write-permission-id'),
    ('admin-role-id', 'projects-delete-permission-id'),
    ('admin-role-id', 'accounts-read-permission-id'),
    ('admin-role-id', 'accounts-write-permission-id'),
    ('admin-role-id', 'transfers-read-permission-id'),
    ('admin-role-id', 'transfers-write-permission-id'),
    ('admin-role-id', 'api-keys-read-permission-id'),
    ('admin-role-id', 'api-keys-write-permission-id'),
    ('admin-role-id', 'api-keys-delete-permission-id'),
    ('admin-role-id', 'analytics-read-permission-id'),
    ('admin-role-id', 'compliance-read-permission-id'),
    ('admin-role-id', 'compliance-write-permission-id'),
    ('admin-role-id', 'kyc-read-permission-id'),
    ('admin-role-id', 'kyc-write-permission-id')
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- Developer permissions
INSERT INTO role_permissions (role_id, permission_id) VALUES
    ('developer-role-id', 'projects-read-permission-id'),
    ('developer-role-id', 'projects-write-permission-id'),
    ('developer-role-id', 'projects-delete-permission-id'),
    ('developer-role-id', 'accounts-read-permission-id'),
    ('developer-role-id', 'accounts-write-permission-id'),
    ('developer-role-id', 'transfers-read-permission-id'),
    ('developer-role-id', 'transfers-write-permission-id'),
    ('developer-role-id', 'api-keys-read-permission-id'),
    ('developer-role-id', 'api-keys-write-permission-id'),
    ('developer-role-id', 'api-keys-delete-permission-id'),
    ('developer-role-id', 'analytics-read-permission-id')
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- Viewer permissions
INSERT INTO role_permissions (role_id, permission_id) VALUES
    ('viewer-role-id', 'viewer-projects-read-permission-id'),
    ('viewer-role-id', 'viewer-accounts-read-permission-id'),
    ('viewer-role-id', 'viewer-transfers-read-permission-id'),
    ('viewer-role-id', 'viewer-analytics-read-permission-id')
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- Support permissions
INSERT INTO role_permissions (role_id, permission_id) VALUES
    ('support-role-id', 'support-users-read-permission-id'),
    ('support-role-id', 'support-accounts-read-permission-id'),
    ('support-role-id', 'support-transfers-read-permission-id'),
    ('support-role-id', 'compliance-read-permission-id'),
    ('support-role-id', 'compliance-write-permission-id'),
    ('support-role-id', 'kyc-read-permission-id'),
    ('support-role-id', 'kyc-write-permission-id')
ON CONFLICT (role_id, permission_id) DO NOTHING;
