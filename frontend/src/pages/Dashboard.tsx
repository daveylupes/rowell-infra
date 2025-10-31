import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { DashboardLayout } from "@/components/DashboardLayout";
import { 
  Users, 
  ArrowUpRight, 
  TrendingUp,
  Activity,
  CreditCard,
  Loader2
} from "lucide-react";
import { useDashboardData, useTransactions, useTransfers } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDistanceToNow } from "date-fns";

const Dashboard = () => {
  const dashboardData = useDashboardData();
  const { data: recentTransactions, isLoading: transactionsLoading } = useTransactions({ limit: 5 });
  const { data: recentTransfers, isLoading: transfersLoading } = useTransfers({ limit: 5 });

  // Extract metrics from dashboard data
  // Each query result has a .data property with the actual data
  // Safely extract data, ensuring we have arrays
  const accountsData = Array.isArray(dashboardData.accounts?.data) ? dashboardData.accounts.data : [];
  const transfersData = Array.isArray(dashboardData.transfers?.data) ? dashboardData.transfers.data : [];
  
  // Remittance flows API returns {flows: [...], pagination: {...}, ...}
  // So we need to access .data.flows instead of .data
  const remittanceFlowsResponse = dashboardData.remittanceFlows?.data;
  const remittanceFlowsData = Array.isArray(remittanceFlowsResponse)
    ? remittanceFlowsResponse 
    : (remittanceFlowsResponse && typeof remittanceFlowsResponse === 'object' && 'flows' in remittanceFlowsResponse && Array.isArray(remittanceFlowsResponse.flows))
    ? remittanceFlowsResponse.flows 
    : [];
  
  const totalAccounts = accountsData.length;
  const totalTransfers = transfersData.length;
  const totalVolume = remittanceFlowsData.length > 0
    ? remittanceFlowsData.reduce((sum, flow: any) => {
        const volume = parseFloat(flow?.total_volume_usd || "0") || 0;
        return sum + volume;
      }, 0)
    : 0;
  
  // Calculate success rate from transfers
  const successfulTransfers = transfersData.filter((t: any) => t?.status === 'success').length;
  const successRate = totalTransfers > 0 ? ((successfulTransfers / totalTransfers) * 100).toFixed(1) : "0.0";

  // Hedera-specific metrics
  const hederaAccounts = accountsData.filter((acc: any) => acc.network?.toLowerCase() === 'hedera').length;
  const hederaTransfers = transfersData.filter((t: any) => t.network?.toLowerCase() === 'hedera').length;
  const hederaTransactions = recentTransactions?.filter((tx: any) => tx.network?.toLowerCase() === 'hedera') || [];
  const stellarAccounts = accountsData.filter((acc: any) => acc.network?.toLowerCase() === 'stellar').length;
  const stellarTransfers = transfersData.filter((t: any) => t.network?.toLowerCase() === 'stellar').length;

  const isLoading = dashboardData.isLoading || transactionsLoading || transfersLoading;
  const hasError = dashboardData.isError;

  return (
    <DashboardLayout title="Dashboard" description="Monitor your accounts, transactions, and analytics in real-time">
      {/* Overview Section */}
      <section className="mb-16">
          <div className="max-w-4xl mx-auto text-center mb-12">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">Overview</h2>
            <p className="mt-4 text-base text-gray-600 dark:text-gray-300">Key metrics and performance indicators</p>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-32 rounded-xl" />
              ))}
            </div>
          ) : hasError ? (
            <div className="text-center py-8">
              <p className="text-red-500">Failed to load dashboard data. Please try again later.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
              {/* Hedera Accounts - Featured */}
              <div className="bg-gradient-to-br from-purple-500/10 to-blue-500/10 dark:from-purple-500/20 dark:to-blue-500/20 p-6 rounded-xl border-2 border-purple-400/30 dark:border-purple-400/40 text-center shadow-lg">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 mx-auto mb-4">
                  <Users className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">Hedera Accounts</h3>
                <p className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 dark:from-purple-400 dark:to-blue-400 bg-clip-text text-transparent">{hederaAccounts.toLocaleString()}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">of {totalAccounts} total</p>
              </div>
              <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary mx-auto mb-4">
                  <CreditCard className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Transaction Volume</h3>
                <p className="text-3xl font-bold text-primary">${totalVolume.toLocaleString(undefined, { maximumFractionDigits: 0 })}</p>
              </div>
              <div className="bg-background-light dark:bg-primary/10 p-6 rounded-xl border border-primary/20 dark:border-primary/20 text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-primary/20 text-primary mx-auto mb-4">
                  <TrendingUp className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Success Rate</h3>
                <p className="text-3xl font-bold text-primary">{successRate}%</p>
              </div>
            </div>
          )}
        </section>

        {/* Analytics Section */}
        <section className="mb-16">
          <div className="max-w-4xl mx-auto text-center mb-12">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">Real-time Analytics</h2>
            <p className="mt-4 text-base text-gray-600 dark:text-gray-300">Live transaction monitoring and network performance</p>
          </div>
            
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Transactions</h3>
                    <p className="text-3xl font-bold text-primary mt-2">{recentTransactions?.length || 0}</p>
                  </div>
                  <div className="flex items-center gap-1 text-sm font-medium text-green-500">
                    <Activity className="h-4 w-4" />
                  </div>
                </div>
                <div className="h-48 bg-primary/5 rounded-lg flex items-center justify-center">
                  {transactionsLoading ? (
                    <Loader2 className="h-8 w-8 text-primary animate-spin" />
                  ) : recentTransactions && recentTransactions.length > 0 ? (
                    <div className="w-full text-left space-y-2">
                      {hederaTransactions.length > 0 ? (
                        hederaTransactions.slice(0, 3).map((tx: any, idx: number) => (
                          <div key={idx} className="text-sm text-gray-600 dark:text-gray-300 flex items-center gap-2">
                            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-purple-700 dark:text-purple-300 border border-purple-400/30">
                              HBAR
                            </span>
                            <span>{tx.asset_code} - {tx.amount}</span>
                          </div>
                        ))
                      ) : (
                        recentTransactions.slice(0, 3).map((tx, idx) => (
                          <div key={idx} className="text-sm text-gray-600 dark:text-gray-300">
                            {tx.network} - {tx.asset_code} - {tx.amount}
                          </div>
                        ))
                      )}
                    </div>
                  ) : (
                    <div className="text-center">
                      <Activity className="h-12 w-12 text-primary mx-auto mb-2" />
                      <p className="text-sm text-gray-600 dark:text-gray-300">No recent transactions</p>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="bg-background-light dark:bg-background-dark p-6 rounded-xl border border-primary/20 dark:border-primary/20">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Network Status</h3>
                    <p className="text-3xl font-bold text-primary mt-2">99%</p>
                  </div>
                  <div className="flex items-center gap-1 text-sm font-medium text-green-500">
                    <span>Healthy</span>
                    <ArrowUpRight className="h-4 w-4" />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  {/* Hedera - Featured First */}
                  <div className="text-center p-3 rounded-lg bg-gradient-to-br from-purple-500/10 to-blue-500/10 dark:from-purple-500/20 dark:to-blue-500/20 border border-purple-400/30 dark:border-purple-400/40">
                    <div className="h-20 bg-purple-500/20 dark:bg-purple-500/30 rounded-lg flex items-end justify-center mb-2">
                      <div className="w-full bg-gradient-to-t from-purple-600 to-blue-600 rounded-lg" style={{height: "98%"}}></div>
                    </div>
                    <p className="text-sm font-bold text-gray-900 dark:text-white">Hedera</p>
                    <p className="text-xs text-purple-600 dark:text-purple-400 font-medium">{hederaTransfers} transfers</p>
                  </div>
                  <div className="text-center">
                    <div className="h-20 bg-primary/20 rounded-lg flex items-end justify-center mb-2">
                      <div className="w-full bg-primary rounded-lg" style={{height: "95%"}}></div>
                    </div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-300">Stellar</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{stellarTransfers} transfers</p>
                  </div>
                </div>
              </div>
            </div>
        </section>

        {/* Quick Actions Section */}
        <section className="mb-16">
          <div className="max-w-4xl mx-auto text-center mb-12">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">Quick Actions</h2>
            <p className="mt-4 text-base text-gray-600 dark:text-gray-300">Common tasks and shortcuts</p>
          </div>
          
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <Link to="/accounts">
              <Button className="w-full rounded-lg bg-primary px-4 py-3 text-sm font-bold text-white hover:bg-primary/90">
                Create Account
              </Button>
            </Link>
            <Link to="/transfers">
              <Button className="w-full rounded-lg bg-primary/20 dark:bg-primary/20 text-primary dark:text-white px-4 py-3 text-sm font-bold hover:bg-primary/30 dark:hover:bg-primary/30">
                Send Transfer
              </Button>
            </Link>
            <Link to="/documentation">
              <Button className="w-full rounded-lg bg-primary/20 dark:bg-primary/20 text-primary dark:text-white px-4 py-3 text-sm font-bold hover:bg-primary/30 dark:hover:bg-primary/30">
                View Documentation
              </Button>
            </Link>
            <Link to="/support">
              <Button className="w-full rounded-lg bg-primary/20 dark:bg-primary/20 text-primary dark:text-white px-4 py-3 text-sm font-bold hover:bg-primary/30 dark:hover:bg-primary/30">
                Get Support
              </Button>
            </Link>
          </div>
        </section>

        {/* Recent Activity Section */}
        <section className="mb-16">
          <div className="max-w-4xl mx-auto text-center mb-12">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">Recent Activity</h2>
            <p className="mt-4 text-base text-gray-600 dark:text-gray-300">Latest transactions and account activities</p>
          </div>
            
            <div className="bg-background-light dark:bg-background-dark rounded-xl border border-primary/20 dark:border-primary/20 overflow-hidden">
              {isLoading ? (
                <div className="p-6 space-y-4">
                  {[1, 2, 3].map((i) => (
                    <Skeleton key={i} className="h-12 w-full" />
                  ))}
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-primary/10 dark:divide-primary/20">
                    <thead className="bg-primary/5 dark:bg-primary/10">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">Activity</th>
                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">Timestamp</th>
                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-gray-400" scope="col">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-primary/10 dark:divide-primary/20">
                      {recentTransfers && recentTransfers.length > 0 ? (
                        recentTransfers.slice(0, 5).map((transfer, idx) => (
                          <tr key={idx}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                              Transfer {transfer.transaction_hash.slice(0, 8)}... 
                              {transfer.from_account ? ` from ${transfer.from_account.slice(0, 8)}...` : ''}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
                              {transfer.created_at ? formatDistanceToNow(new Date(transfer.created_at), { addSuffix: true }) : 'N/A'}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                                transfer.status === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                                transfer.status === 'pending' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                                'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                              }`}>
                                {transfer.status}
                              </span>
                            </td>
                          </tr>
                        ))
                      ) : recentTransactions && recentTransactions.length > 0 ? (
                        recentTransactions
                          .sort((a: any, b: any) => {
                            // Sort Hedera transactions first
                            if (a.network?.toLowerCase() === 'hedera' && b.network?.toLowerCase() !== 'hedera') return -1;
                            if (a.network?.toLowerCase() !== 'hedera' && b.network?.toLowerCase() === 'hedera') return 1;
                            return 0;
                          })
                          .slice(0, 5).map((tx, idx) => (
                          <tr key={idx} className={tx.network?.toLowerCase() === 'hedera' ? 'bg-purple-50/50 dark:bg-purple-900/10' : ''}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                              {tx.network?.toLowerCase() === 'hedera' && (
                                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gradient-to-r from-purple-500/20 to-blue-500/20 text-purple-700 dark:text-purple-300 border border-purple-400/30 mr-2">
                                  HBAR
                                </span>
                              )}
                              Transaction {tx.transaction_hash.slice(0, 8)}... ({tx.network})
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
                              {tx.created_at ? formatDistanceToNow(new Date(tx.created_at), { addSuffix: true }) : 'N/A'}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                                tx.status === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                                tx.status === 'pending' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                                'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                              }`}>
                                {tx.status}
                              </span>
                            </td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan={3} className="px-6 py-8 text-center text-sm text-gray-500 dark:text-gray-400">
                            No recent activity
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
        </section>
    </DashboardLayout>
  );
};

export default Dashboard;
