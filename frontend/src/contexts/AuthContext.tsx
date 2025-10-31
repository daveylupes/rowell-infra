/**
 * Authentication Context for managing user authentication state
 */

import React, { createContext, useContext, useReducer, useEffect, useCallback, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

// Types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  company?: string;
  phone?: string;
  country_code?: string;
  is_active: boolean;
  is_verified: boolean;
  email_verified_at?: string;
  last_login?: string;
  created_at: string;
  updated_at?: string;
  roles: Role[];
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  is_active: boolean;
  permissions: Permission[];
}

export interface Permission {
  id: string;
  name: string;
  resource: string;
  action: string;
  description?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  user_type: 'user' | 'developer';
  company?: string;
  phone?: string;
  country_code?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: { user: User; tokens: AuthTokens } }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'AUTH_LOGOUT' }
  | { type: 'AUTH_REFRESH'; payload: AuthTokens }
  | { type: 'AUTH_UPDATE_USER'; payload: User }
  | { type: 'AUTH_CLEAR_ERROR' }
  | { type: 'AUTH_LOADING_COMPLETE' };

interface AuthContextType {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  hasPermission: (permission: string) => boolean;
  hasRole: (role: string) => boolean;
  clearError: () => void;
}

// Initial state
const initialState: AuthState = {
  user: null,
  tokens: null,
  isAuthenticated: false,
  isLoading: true, // Start with loading true to check auth state
  error: null,
};

// Reducer
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        tokens: action.payload.tokens,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'AUTH_FAILURE':
      return {
        ...state,
        user: null,
        tokens: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case 'AUTH_LOGOUT':
      return {
        ...state,
        user: null,
        tokens: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case 'AUTH_LOADING_COMPLETE':
      return {
        ...state,
        isLoading: false,
      };
    case 'AUTH_REFRESH':
      return {
        ...state,
        tokens: action.payload,
        isLoading: false,
        error: null,
      };
    case 'AUTH_UPDATE_USER':
      return {
        ...state,
        user: action.payload,
        error: null,
      };
    case 'AUTH_CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
}

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Storage keys
const STORAGE_KEYS = {
  ACCESS_TOKEN: 'rowell_access_token',
  REFRESH_TOKEN: 'rowell_refresh_token',
  USER: 'rowell_user',
} as const;

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Auth provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const navigate = useNavigate();

  // Load authentication state from storage on mount
  useEffect(() => {
    const loadAuthState = async () => {
      try {
        const accessToken = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
        const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
        const userStr = localStorage.getItem(STORAGE_KEYS.USER);

        if (accessToken && refreshToken && userStr) {
          const user = JSON.parse(userStr);
          const tokens = {
            access_token: accessToken,
            refresh_token: refreshToken,
            token_type: 'bearer',
            expires_in: 900, // 15 minutes
          };

          // Verify token is still valid by fetching user info
          try {
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
              headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
              },
            });

            if (response.ok) {
              const currentUser = await response.json();
              console.log('Auth state loaded - User:', currentUser);
              console.log('Auth state loaded - Roles:', currentUser.roles);
              console.log('Auth state loaded - Permissions:', currentUser.roles?.flatMap((r: any) => r.permissions?.map((p: any) => p.name) || []));
              
              // Update stored user data with fresh data from backend
              localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(currentUser));
              
              dispatch({
                type: 'AUTH_SUCCESS',
                payload: { user: currentUser, tokens },
              });
            } else {
              // Token is invalid, try to refresh
              await refreshTokenFromStorage();
            }
          } catch (error) {
            // Network error, try to refresh
            await refreshTokenFromStorage();
          }
        } else {
          // No tokens found, set loading to false
          dispatch({ type: 'AUTH_LOADING_COMPLETE' });
        }
      } catch (error) {
        console.error('Failed to load auth state:', error);
        clearAuthStorage();
        dispatch({ type: 'AUTH_LOADING_COMPLETE' });
      }
    };

    loadAuthState();
  }, []);

  // Auto-refresh token before expiration
  useEffect(() => {
    if (!state.tokens) return;

    const refreshInterval = setInterval(async () => {
      try {
        await refreshToken();
      } catch (error) {
        console.error('Auto-refresh failed:', error);
        logout();
      }
    }, 14 * 60 * 1000); // Refresh every 14 minutes

    return () => clearInterval(refreshInterval);
  }, [state.tokens]);

  // Helper function to refresh token from storage
  const refreshTokenFromStorage = async () => {
    const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
    if (!refreshToken) {
      clearAuthStorage();
      dispatch({ type: 'AUTH_LOADING_COMPLETE' });
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.ok) {
        const tokens = await response.json();
        saveAuthStorage(tokens);
        dispatch({ type: 'AUTH_REFRESH', payload: tokens });
      } else {
        clearAuthStorage();
        dispatch({ type: 'AUTH_LOGOUT' });
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      clearAuthStorage();
      dispatch({ type: 'AUTH_LOGOUT' });
    }
  };

  // Helper function to save auth data to storage
  const saveAuthStorage = (tokens: AuthTokens, user?: User) => {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.access_token);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh_token);
    if (user) {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    }
  };

  // Helper function to clear auth data from storage
  const clearAuthStorage = () => {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  };

  // Login function
  const login = async (data: LoginData) => {
    dispatch({ type: 'AUTH_START' });

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        // Get user info
        const userResponse = await fetch(`${API_BASE_URL}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${result.access_token}`,
            'Content-Type': 'application/json',
          },
        });

        if (userResponse.ok) {
          const user = await userResponse.json();
          console.log('Login - User data:', user);
          console.log('Login - Roles:', user.roles);
          console.log('Login - Permissions:', user.roles?.flatMap((r: any) => r.permissions?.map((p: any) => p.name) || []));
          
          saveAuthStorage(result, user);
          dispatch({
            type: 'AUTH_SUCCESS',
            payload: { user, tokens: result },
          });
          toast.success('Login successful!');
        } else {
          throw new Error('Failed to fetch user information');
        }
      } else {
        throw new Error(result.detail || 'Login failed');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Login failed';
      dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
      toast.error(errorMessage);
      throw error;
    }
  };

  // Register function
  const register = async (data: RegisterData) => {
    dispatch({ type: 'AUTH_START' });

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        // Backend now returns user and tokens for auto-login
        const tokens = result.tokens || {
          access_token: result.access_token,
          refresh_token: result.refresh_token,
          token_type: result.token_type || 'bearer',
          expires_in: result.expires_in || 900,
        };

        // Auto-login after registration
        if (tokens.access_token) {
          // Fetch fresh user data from /auth/me to ensure roles/permissions are loaded
          try {
            const userResponse = await fetch(`${API_BASE_URL}/auth/me`, {
              headers: {
                'Authorization': `Bearer ${tokens.access_token}`,
                'Content-Type': 'application/json',
              },
            });

            if (userResponse.ok) {
              const user = await userResponse.json();
              console.log('User data loaded:', user);
              console.log('User roles:', user.roles);
              console.log('User permissions:', user.roles?.flatMap((r: any) => r.permissions?.map((p: any) => p.name) || []));
              
              saveAuthStorage(tokens, user);
              dispatch({
                type: 'AUTH_SUCCESS',
                payload: { user, tokens },
              });
              toast.success('Registration successful! You have been logged in.');
              navigate('/dashboard', { replace: true });
            } else {
              // Fallback to user from registration response
              const user = result.user || result;
              console.warn('Failed to fetch user from /auth/me, using registration response:', user);
              saveAuthStorage(tokens, user);
              dispatch({
                type: 'AUTH_SUCCESS',
                payload: { user, tokens },
              });
              toast.success('Registration successful! You have been logged in.');
              navigate('/dashboard', { replace: true });
            }
          } catch (error) {
            console.error('Failed to fetch user from /auth/me:', error);
            // Fallback to user from registration response
            const user = result.user || result;
            saveAuthStorage(tokens, user);
            dispatch({
              type: 'AUTH_SUCCESS',
              payload: { user, tokens },
            });
            toast.success('Registration successful! You have been logged in.');
            navigate('/dashboard', { replace: true });
          }
        } else {
          // Fallback: just show success message
          dispatch({ type: 'AUTH_CLEAR_ERROR' });
          toast.success('Registration successful! Please check your email for verification.');
        }
      } else {
        throw new Error(result.detail || 'Registration failed');
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Registration failed';
      dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
      toast.error(errorMessage);
      throw error;
    }
  };

  // Logout function
  const logout = async () => {
    try {
      if (state.tokens?.refresh_token) {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh_token: state.tokens.refresh_token }),
        });
      }
    } catch (error) {
      console.error('Logout request failed:', error);
    } finally {
      clearAuthStorage();
      dispatch({ type: 'AUTH_LOGOUT' });
      toast.success('Logged out successfully');
      navigate('/'); // Redirect to home page after logout
    }
  };

  // Refresh token function
  const refreshToken = async () => {
    if (!state.tokens?.refresh_token) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: state.tokens.refresh_token }),
      });

      const result = await response.json();

      if (response.ok) {
        saveAuthStorage(result);
        dispatch({ type: 'AUTH_REFRESH', payload: result });
      } else {
        throw new Error('Token refresh failed');
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      logout();
      throw error;
    }
  };

  // Permission checking function
  const hasPermission = (permission: string): boolean => {
    if (!state.user || !state.user.roles) {
      console.log('hasPermission: No user or roles', { user: state.user, permission });
      return false;
    }
    
    // Check all roles for the permission
    const hasPerm = state.user.roles.some(role => {
      if (!role.is_active || !role.permissions) {
        console.log('hasPermission: Role inactive or no permissions', { role, permission });
        return false;
      }
      
      return role.permissions.some(perm => {
        // Check if permission is active (default to true if not provided)
        const isActive = perm.is_active !== undefined ? perm.is_active : true;
        const matches = perm.name === permission;
        console.log('hasPermission: Checking permission', { permName: perm.name, permission, isActive, matches });
        return isActive && matches;
      });
    });
    
    console.log('hasPermission result:', { permission, hasPerm, roles: state.user.roles });
    return hasPerm;
  };

  // Role checking function
  const hasRole = (role: string): boolean => {
    if (!state.user || !state.user.roles) {
      console.log('hasRole: No user or roles', { user: state.user, role });
      return false;
    }
    
    // Check if user has the role (case-insensitive check)
    const hasRoleResult = state.user.roles.some(r => {
      const matches = r.is_active && r.name.toLowerCase() === role.toLowerCase();
      console.log('hasRole: Checking role', { roleName: r.name, requiredRole: role, isActive: r.is_active, matches });
      return matches;
    });
    
    console.log('hasRole result:', { role, hasRoleResult, roles: state.user.roles });
    return hasRoleResult;
  };

  // Clear error function - memoized to prevent infinite loops
  const clearError = useCallback(() => {
    dispatch({ type: 'AUTH_CLEAR_ERROR' });
  }, []);

  // Context value - functions are stable enough for this use case
  // Only clearError is memoized to prevent infinite loops in useEffect dependencies
  const value: AuthContextType = {
    user: state.user,
    tokens: state.tokens,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    error: state.error,
    login,
    register,
    logout,
    refreshToken,
    hasPermission,
    hasRole,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Custom hook for permission checking
export function usePermissions() {
  const { hasPermission, hasRole, user } = useAuth();
  
  return {
    hasPermission,
    hasRole,
    permissions: user?.roles.flatMap(role => 
      role.permissions.map(perm => perm.name)
    ) || [],
    roles: user?.roles.map(role => role.name) || [],
  };
}
