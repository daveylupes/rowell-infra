/**
 * Protected Route Component for authentication and authorization
 */

import React, { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent } from '@/components/ui/card';
import { AlertCircle, Lock } from 'lucide-react';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredPermission?: string;
  requiredRole?: string;
  fallback?: ReactNode;
  redirectTo?: string;
}

export function ProtectedRoute({
  children,
  requiredPermission,
  requiredRole,
  fallback,
  redirectTo = '/login',
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user, hasPermission, hasRole } = useAuth();
  const location = useLocation();

  // Show loading state while checking authentication
  if (isLoading) {
    return fallback || <LoadingFallback />;
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Check role requirement
  if (requiredRole && !hasRole(requiredRole)) {
    return <UnauthorizedFallback requiredRole={requiredRole} />;
  }

  // Check permission requirement
  if (requiredPermission && !hasPermission(requiredPermission)) {
    return <UnauthorizedFallback requiredPermission={requiredPermission} />;
  }

  // User is authenticated and authorized
  return <>{children}</>;
}

// Loading fallback component
function LoadingFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardContent className="p-6">
          <div className="space-y-4">
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
            <div className="text-center">
              <h3 className="text-lg font-semibold">Loading...</h3>
              <p className="text-gray-600">Checking authentication</p>
            </div>
            <div className="space-y-2">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Unauthorized fallback component
function UnauthorizedFallback({ 
  requiredRole, 
  requiredPermission 
}: { 
  requiredRole?: string; 
  requiredPermission?: string; 
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <Card className="w-full max-w-md">
        <CardContent className="p-6">
          <div className="text-center space-y-4">
            <div className="flex justify-center">
              <div className="rounded-full bg-red-100 p-3">
                <Lock className="h-6 w-6 text-red-600" />
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Access Denied
              </h3>
              <p className="text-gray-600 mt-2">
                {requiredRole 
                  ? `You need the "${requiredRole}" role to access this page.`
                  : requiredPermission
                  ? `You need the "${requiredPermission}" permission to access this page.`
                  : 'You do not have permission to access this page.'
                }
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-2">
              <button
                onClick={() => window.history.back()}
                className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Go Back
              </button>
              <button
                onClick={() => window.location.href = '/dashboard'}
                className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Go to Dashboard
              </button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

// Public route component (redirects authenticated users)
export function PublicRoute({ 
  children, 
  redirectTo = '/dashboard' 
}: { 
  children: ReactNode; 
  redirectTo?: string; 
}) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  // Show loading state while checking authentication
  if (isLoading) {
    return <LoadingFallback />;
  }

  // Redirect authenticated users away from public pages
  if (isAuthenticated) {
    const from = location.state?.from?.pathname || redirectTo;
    return <Navigate to={from} replace />;
  }

  return <>{children}</>;
}

// Admin route component
export function AdminRoute({ children }: { children: ReactNode }) {
  return (
    <ProtectedRoute requiredRole="admin">
      {children}
    </ProtectedRoute>
  );
}

// Developer route component
export function DeveloperRoute({ children }: { children: ReactNode }) {
  return (
    <ProtectedRoute requiredRole="developer">
      {children}
    </ProtectedRoute>
  );
}

// Support route component
export function SupportRoute({ children }: { children: ReactNode }) {
  return (
    <ProtectedRoute requiredRole="support">
      {children}
    </ProtectedRoute>
  );
}
