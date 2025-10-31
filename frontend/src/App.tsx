import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute, PublicRoute, AdminRoute, DeveloperRoute, SupportRoute } from "@/components/auth/ProtectedRoute";
import Landing from "./pages/Landing";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import DeveloperDashboard from "./pages/DeveloperDashboard";
import AccountManagement from "./pages/AccountManagement";
import Accounts from "./pages/Accounts";
import Transfers from "./pages/Transfers";
import Analytics from "./pages/Analytics";
import Product from "./pages/Product";
import Pricing from "./pages/Pricing";
import Support from "./pages/Support";
import Documentation from "./pages/Documentation";
import ApiReference from "./pages/ApiReference";
import QuickStartGuide from "./pages/QuickStartGuide";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <BrowserRouter>
          <AuthProvider>
            <Toaster />
            <Sonner />
            <Routes>
            {/* Public routes */}
            <Route path="/" element={<PublicRoute><Landing /></PublicRoute>} />
            <Route path="/product" element={<PublicRoute><Product /></PublicRoute>} />
            <Route path="/pricing" element={<PublicRoute><Pricing /></PublicRoute>} />
            <Route path="/support" element={<PublicRoute><Support /></PublicRoute>} />
            <Route path="/documentation" element={<PublicRoute><Documentation /></PublicRoute>} />
            <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
            <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
            
            {/* Protected routes */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            
            <Route path="/developer-dashboard" element={
              <DeveloperRoute>
                <DeveloperDashboard />
              </DeveloperRoute>
            } />
            
            <Route path="/account-management" element={
              <ProtectedRoute requiredPermission="accounts:read">
                <AccountManagement />
              </ProtectedRoute>
            } />
            
            <Route path="/accounts" element={
              <ProtectedRoute requiredPermission="accounts:read">
                <Accounts />
              </ProtectedRoute>
            } />
            
            <Route path="/transfers" element={
              <ProtectedRoute requiredPermission="transfers:read">
                <Transfers />
              </ProtectedRoute>
            } />
            
            <Route path="/analytics" element={
              <ProtectedRoute requiredPermission="analytics:read">
                <Analytics />
              </ProtectedRoute>
            } />
            
            <Route path="/api-reference" element={
              <ProtectedRoute>
                <ApiReference />
              </ProtectedRoute>
            } />
            
            <Route path="/quickstart" element={
              <ProtectedRoute>
                <QuickStartGuide />
              </ProtectedRoute>
            } />
            
            {/* Admin routes */}
            <Route path="/admin/*" element={
              <AdminRoute>
                <div>Admin Panel - Coming Soon</div>
              </AdminRoute>
            } />
            
            {/* Support routes */}
            <Route path="/support-dashboard" element={
              <SupportRoute>
                <div>Support Dashboard - Coming Soon</div>
              </SupportRoute>
            } />
            
            {/* Catch-all route */}
            <Route path="*" element={<NotFound />} />
          </Routes>
          </AuthProvider>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
);

export default App;
