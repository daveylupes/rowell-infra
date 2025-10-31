import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useAnalyticsDashboard, useRemittanceFlows, useTransfers } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDistanceToNow } from "date-fns";
import { Loader2, TrendingUp, ArrowUpRight, CheckCircle } from "lucide-react";
import { DashboardLayout } from "@/components/DashboardLayout";

const Analytics = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'volume' | 'countries' | 'fees'>('overview');
  const { data: dashboard, isLoading: dashboardLoading } = useAnalyticsDashboard({ period_type: 'monthly' });
  const { data: remittanceFlowsResponse } = useRemittanceFlows({ limit: 5 });
  const { data: recentTransfers } = useTransfers({ limit: 5 });
  
  // Remittance flows API returns {flows: [...], pagination: {...}, ...}
  const remittanceFlows = Array.isArray(remittanceFlowsResponse?.flows) 
    ? remittanceFlowsResponse.flows 
    : Array.isArray(remittanceFlowsResponse) 
    ? remittanceFlowsResponse 
    : [];

  // Calculate metrics
  const totalVolume = dashboard?.total_volume_usd 
    ? parseFloat(dashboard.total_volume_usd).toLocaleString(undefined, { maximumFractionDigits: 0 })
    : '0';
  const totalTransfers = dashboard?.total_transactions || 0;
  const successRate = dashboard?.success_rate 
    ? (dashboard.success_rate * 100).toFixed(1)
    : '99.8';
  const avgFee = dashboard?.avg_fee_usd || '2.50';

  // Top countries from remittance flows
  const topCountries = Array.isArray(remittanceFlows) ? remittanceFlows.slice(0, 3) : [];

  const countryFlags: Record<string, string> = {
    'NG': '🇳🇬',
    'KE': '🇰🇪',
    'GH': '🇬🇭',
    'ZA': '🇿🇦',
    'UG': '🇺🇬',
    'TZ': '🇹🇿',
  };

  const countryNames: Record<string, string> = {
    'NG': 'Nigeria',
    'KE': 'Kenya',
    'GH': 'Ghana',
    'ZA': 'South Africa',
    'UG': 'Uganda',
    'TZ': 'Tanzania',
  };

  return (
    <DashboardLayout title="Analytics" description="Track your transfer performance and insights">
      {/* Navigation Tabs */}
        <div className="border-b border-black/10 dark:border-white/10 mb-6">
          <nav className="flex gap-8">
            <button
              onClick={() => setActiveTab('overview')}
              className={`py-3 border-b-2 transition-colors ${
                activeTab === 'overview'
                  ? 'border-primary text-primary font-semibold'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('volume')}
              className={`py-3 border-b-2 transition-colors ${
                activeTab === 'volume'
                  ? 'border-primary text-primary font-semibold'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
              }`}
            >
              Volume
            </button>
            <button
              onClick={() => setActiveTab('countries')}
              className={`py-3 border-b-2 transition-colors ${
                activeTab === 'countries'
                  ? 'border-primary text-primary font-semibold'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
              }`}
            >
              Countries
            </button>
            <button
              onClick={() => setActiveTab('fees')}
              className={`py-3 border-b-2 transition-colors ${
                activeTab === 'fees'
                  ? 'border-primary text-primary font-semibold'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
              }`}
            >
              Fees
            </button>
          </nav>
        </div>

        {/* Analytics Content */}
        <div className="space-y-8">
          {/* Key Metrics */}
          {dashboardLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[1, 2, 3, 4].map((i) => (
                <Skeleton key={i} className="h-32 rounded-xl" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-background-light/50 dark:bg-background-dark/50 p-6 rounded-xl shadow-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Total Volume</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">${totalVolume}</p>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                    <TrendingUp className="h-6 w-6 text-primary" />
                  </div>
                </div>
                <p className="text-sm text-green-600 mt-2">From analytics dashboard</p>
              </div>

              <div className="bg-background-light/50 dark:bg-background-dark/50 p-6 rounded-xl shadow-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Total Transfers</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalTransfers.toLocaleString()}</p>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                    <span className="material-symbols-outlined text-primary">swap_horiz</span>
                  </div>
                </div>
                <p className="text-sm text-green-600 mt-2">Active transfers</p>
              </div>

              <div className="bg-background-light/50 dark:bg-background-dark/50 p-6 rounded-xl shadow-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Success Rate</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{successRate}%</p>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                    <CheckCircle className="h-6 w-6 text-primary" />
                  </div>
                </div>
                <p className="text-sm text-green-600 mt-2">High reliability</p>
              </div>

              <div className="bg-background-light/50 dark:bg-background-dark/50 p-6 rounded-xl shadow-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Avg. Fee</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">${avgFee}</p>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                    <span className="material-symbols-outlined text-primary">attach_money</span>
                  </div>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">0.25% of amount</p>
              </div>
            </div>
          )}

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Volume Chart */}
            <div className="bg-background-light/50 dark:bg-background-dark/50 p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Remittance Flows</h3>
              {dashboardLoading ? (
                <Skeleton className="h-64 w-full rounded-lg" />
              ) : Array.isArray(remittanceFlows) && remittanceFlows.length > 0 ? (
                <div className="space-y-4">
                  {remittanceFlows.slice(0, 5).map((flow: any, idx: number) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white">
                          {flow.from_country} → {flow.to_country}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {flow.transaction_count} transactions
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900 dark:text-white">
                          ${parseFloat(flow.total_volume_usd || '0').toLocaleString(undefined, { maximumFractionDigits: 0 })}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="h-64 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500 dark:text-gray-400">No remittance flow data available</p>
                </div>
              )}
            </div>

            {/* Country Distribution */}
            <div className="bg-background-light/50 dark:bg-background-dark/50 p-6 rounded-xl shadow-lg">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Top Countries</h3>
              {dashboardLoading ? (
                <Skeleton className="h-64 w-full rounded-lg" />
              ) : topCountries.length > 0 ? (
                <div className="space-y-4">
                  {topCountries.map((flow, idx) => (
                    <div key={idx} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{countryFlags[flow.to_country] || '🌍'}</span>
                        <span className="text-gray-900 dark:text-white">
                          {countryNames[flow.to_country] || flow.to_country}
                        </span>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900 dark:text-white">
                          ${parseFloat(flow.total_volume_usd || '0').toLocaleString(undefined, { maximumFractionDigits: 0 })}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {flow.transaction_count} transactions
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="space-y-4">
                  <p className="text-gray-500 dark:text-gray-400">No country data available</p>
                </div>
              )}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-background-light/50 dark:bg-background-dark/50 p-6 rounded-xl shadow-lg">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Activity</h3>
            {dashboardLoading ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            ) : recentTransfers && recentTransfers.length > 0 ? (
              <div className="space-y-4">
                {recentTransfers.slice(0, 5).map((transfer, idx) => (
                  <div key={idx} className="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-0">
                    <div className="flex items-center gap-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        transfer.status === 'success' ? 'bg-green-100 dark:bg-green-900' :
                        transfer.status === 'pending' ? 'bg-yellow-100 dark:bg-yellow-900' :
                        'bg-red-100 dark:bg-red-900'
                      }`}>
                        {transfer.status === 'success' ? (
                          <CheckCircle className="h-4 w-4 text-green-600 dark:text-green-400" />
                        ) : (
                          <Loader2 className="h-4 w-4 text-yellow-600 dark:text-yellow-400 animate-spin" />
                        )}
                      </div>
                      <div>
                        <p className="text-gray-900 dark:text-white">
                          Transfer {transfer.transaction_hash.slice(0, 8)}...
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {transfer.amount} {transfer.asset_code}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {transfer.created_at ? formatDistanceToNow(new Date(transfer.created_at), { addSuffix: true }) : 'N/A'}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 dark:text-gray-400">No recent activity</p>
            )}
          </div>
        </div>
    </DashboardLayout>
  );
};

export default Analytics;
