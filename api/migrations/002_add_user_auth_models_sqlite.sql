-- Migration: Add User Authentication Models (SQLite compatible)
-- Description: Create tables for user authentication, roles, and permissions
-- Date: 2024-12-19

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    company TEXT,
    phone TEXT,
    country_code TEXT,
    is_active BOOLEAN DEFAULT 1,
    is_verified BOOLEAN DEFAULT 0,
    email_verified_at TEXT,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TEXT,
    password_changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT,
    last_login TEXT
);

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- Create permissions table
CREATE TABLE IF NOT EXISTS permissions (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    resource TEXT NOT NULL,
    action TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- Create user_roles junction table
CREATE TABLE IF NOT EXISTS user_roles (
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    role_id TEXT REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,
    assigned_by TEXT REFERENCES users(id),
    PRIMARY KEY (user_id, role_id)
);

-- Create role_permissions junction table
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id TEXT REFERENCES roles(id) ON DELETE CASCADE,
    permission_id TEXT REFERENCES permissions(id) ON DELETE CASCADE,
    assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, permission_id)
);

-- Create user_sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    session_token TEXT UNIQUE NOT NULL,
    refresh_token TEXT UNIQUE NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT NOT NULL,
    last_activity TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Create email_verifications table
CREATE TABLE IF NOT EXISTS email_verifications (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    token TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    is_used BOOLEAN DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT NOT NULL
);

-- Create password_resets table
CREATE TABLE IF NOT EXISTS password_resets (
    id TEXT PRIMARY KEY,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    token TEXT UNIQUE NOT NULL,
    is_used BOOLEAN DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT NOT NULL
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
INSERT OR IGNORE INTO roles (id, name, description, is_active) VALUES
    ('admin-role-id', 'admin', 'Full system access and management', 1),
    ('developer-role-id', 'developer', 'Project owner with development access', 1),
    ('viewer-role-id', 'viewer', 'Read-only access to assigned projects', 1),
    ('support-role-id', 'support', 'Customer support with compliance access', 1);

-- Insert default permissions
INSERT OR IGNORE INTO permissions (id, name, resource, action, description, is_active) VALUES
    -- Admin permissions
    ('admin-all-permission-id', '*:*', '*', '*', 'All permissions', 1),
    ('users-read-permission-id', 'users:read', 'users', 'read', 'Read user information', 1),
    ('users-write-permission-id', 'users:write', 'users', 'write', 'Create and update users', 1),
    ('users-delete-permission-id', 'users:delete', 'users', 'delete', 'Delete users', 1),
    ('roles-read-permission-id', 'roles:read', 'roles', 'read', 'Read role information', 1),
    ('roles-write-permission-id', 'roles:write', 'roles', 'write', 'Create and update roles', 1),
    ('system-read-permission-id', 'system:read', 'system', 'read', 'Read system information', 1),
    ('system-write-permission-id', 'system:write', 'system', 'write', 'Modify system settings', 1),
    
    -- Developer permissions
    ('projects-read-permission-id', 'projects:read', 'projects', 'read', 'Read project information', 1),
    ('projects-write-permission-id', 'projects:write', 'projects', 'write', 'Create and update projects', 1),
    ('projects-delete-permission-id', 'projects:delete', 'projects', 'delete', 'Delete projects', 1),
    ('accounts-read-permission-id', 'accounts:read', 'accounts', 'read', 'Read account information', 1),
    ('accounts-write-permission-id', 'accounts:write', 'accounts', 'write', 'Create and update accounts', 1),
    ('transfers-read-permission-id', 'transfers:read', 'transfers', 'read', 'Read transfer information', 1),
    ('transfers-write-permission-id', 'transfers:write', 'transfers', 'write', 'Create and update transfers', 1),
    ('api-keys-read-permission-id', 'api_keys:read', 'api_keys', 'read', 'Read API key information', 1),
    ('api-keys-write-permission-id', 'api_keys:write', 'api_keys', 'write', 'Create and update API keys', 1),
    ('api-keys-delete-permission-id', 'api_keys:delete', 'api_keys', 'delete', 'Delete API keys', 1),
    ('analytics-read-permission-id', 'analytics:read', 'analytics', 'read', 'Read analytics data', 1),
    
    -- Viewer permissions
    ('viewer-projects-read-permission-id', 'projects:read', 'projects', 'read', 'Read project information', 1),
    ('viewer-accounts-read-permission-id', 'accounts:read', 'accounts', 'read', 'Read account information', 1),
    ('viewer-transfers-read-permission-id', 'transfers:read', 'transfers', 'read', 'Read transfer information', 1),
    ('viewer-analytics-read-permission-id', 'analytics:read', 'analytics', 'read', 'Read analytics data', 1),
    
    -- Support permissions
    ('support-users-read-permission-id', 'users:read', 'users', 'read', 'Read user information', 1),
    ('support-accounts-read-permission-id', 'accounts:read', 'accounts', 'read', 'Read account information', 1),
    ('support-transfers-read-permission-id', 'transfers:read', 'transfers', 'read', 'Read transfer information', 1),
    ('compliance-read-permission-id', 'compliance:read', 'compliance', 'read', 'Read compliance information', 1),
    ('compliance-write-permission-id', 'compliance:write', 'compliance', 'write', 'Update compliance information', 1),
    ('kyc-read-permission-id', 'kyc:read', 'kyc', 'read', 'Read KYC information', 1),
    ('kyc-write-permission-id', 'kyc:write', 'kyc', 'write', 'Update KYC information', 1);

-- Assign permissions to roles
-- Admin gets all permissions
INSERT OR IGNORE INTO role_permissions (role_id, permission_id) VALUES
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
    ('admin-role-id', 'kyc-write-permission-id');

-- Developer permissions
INSERT OR IGNORE INTO role_permissions (role_id, permission_id) VALUES
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
    ('developer-role-id', 'analytics-read-permission-id');

-- Viewer permissions
INSERT OR IGNORE INTO role_permissions (role_id, permission_id) VALUES
    ('viewer-role-id', 'viewer-projects-read-permission-id'),
    ('viewer-role-id', 'viewer-accounts-read-permission-id'),
    ('viewer-role-id', 'viewer-transfers-read-permission-id'),
    ('viewer-role-id', 'viewer-analytics-read-permission-id');

-- Support permissions
INSERT OR IGNORE INTO role_permissions (role_id, permission_id) VALUES
    ('support-role-id', 'support-users-read-permission-id'),
    ('support-role-id', 'support-accounts-read-permission-id'),
    ('support-role-id', 'support-transfers-read-permission-id'),
    ('support-role-id', 'compliance-read-permission-id'),
    ('support-role-id', 'compliance-write-permission-id'),
    ('support-role-id', 'kyc-read-permission-id'),
    ('support-role-id', 'kyc-write-permission-id');
