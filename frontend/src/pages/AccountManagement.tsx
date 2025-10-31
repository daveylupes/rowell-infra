import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useAccounts, useAccountBalances } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { Search, AlertCircle, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/card";
import { DashboardLayout } from "@/components/DashboardLayout";

const AccountManagement = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const { data: accounts, isLoading, isError, refetch } = useAccounts();

  // Filter accounts based on search query
  const filteredAccounts = accounts?.filter(account => 
    account.account_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    account.network.toLowerCase().includes(searchQuery.toLowerCase()) ||
    account.country_code?.toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  // Country flags mapping
  const countryFlags: Record<string, string> = {
    'NG': '🇳🇬',
    'KE': '🇰🇪', 
    'ZA': '🇿🇦',
    'GH': '🇬🇭',
    'UG': '🇺🇬',
    'TZ': '🇹🇿',
    'ET': '🇪🇹',
    'EG': '🇪🇬',
    'MA': '🇲🇦',
    'TN': '🇹🇳'
  };

  const countryNames: Record<string, string> = {
    'NG': 'Nigeria',
    'KE': 'Kenya',
    'ZA': 'South Africa', 
    'GH': 'Ghana',
    'UG': 'Uganda',
    'TZ': 'Tanzania',
    'ET': 'Ethiopia',
    'EG': 'Egypt',
    'MA': 'Morocco',
    'TN': 'Tunisia'
  };

  // Handle errors
  if (isError) {
    return (
      <DashboardLayout title="Account Management" description="Manage your accounts across different countries and networks">
        <Card className="w-full max-w-md mx-auto">
          <div className="p-6 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold mb-2">Connection Error</h2>
            <p className="text-muted-foreground mb-4">
              Unable to load accounts. Please check your connection and try again.
            </p>
            <Button onClick={() => refetch()} className="w-full">
              <RefreshCw className="h-4 w-4 mr-2" />
              Retry
            </Button>
          </div>
        </Card>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Account Management" description="Manage your accounts across different countries and networks">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
        <div>
          <Link to="/accounts">
            <Button className="flex items-center justify-center gap-2 rounded-lg h-10 px-4 bg-gradient-to-r from-accent-start to-accent-end text-white text-sm font-bold shadow-lg hover:shadow-xl transition-shadow">
              <span className="material-symbols-outlined">add</span>
              <span>Create Account</span>
            </Button>
          </Link>
        </div>
      </div>

      {/* Accounts Table */}
          <div className="bg-surface-light dark:bg-surface-dark p-4 sm:p-6 rounded-lg border border-border-light dark:border-border-dark">
            <div className="flex flex-col lg:flex-row gap-4 mb-6">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-subtle-light dark:text-subtle-dark" />
                <input
                  className="form-input w-full rounded-lg text-text-light dark:text-text-dark bg-background-light dark:bg-background-dark border-border-light dark:border-border-dark focus:ring-primary focus:border-primary pl-10 h-11"
                  placeholder="Search accounts by network, currency..."
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>

            {isLoading ? (
              <div className="space-y-4">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            ) : filteredAccounts.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-500 dark:text-gray-400 mb-4">
                  {searchQuery ? 'No accounts match your search' : 'No accounts found'}
                </p>
                <Link to="/accounts">
                  <Button className="bg-primary text-white">
                    Create Your First Account
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="bg-background-light dark:bg-background-dark">
                      <th className="p-4 text-sm font-medium text-subtle-light dark:text-subtle-dark uppercase tracking-wider">Country</th>
                      <th className="p-4 text-sm font-medium text-subtle-light dark:text-subtle-dark uppercase tracking-wider">Account ID</th>
                      <th className="p-4 text-sm font-medium text-subtle-light dark:text-subtle-dark uppercase tracking-wider">Network</th>
                      <th className="p-4 text-sm font-medium text-subtle-light dark:text-subtle-dark uppercase tracking-wider">Status</th>
                      <th className="p-4 text-sm font-medium text-subtle-light dark:text-subtle-dark uppercase tracking-wider text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border-light dark:divide-border-dark">
                    {filteredAccounts.map((account) => (
                      <tr key={account.id} className="hover:bg-background-light/50 dark:hover:bg-background-dark/50 transition-colors">
                        <td className="p-4 align-middle">
                          <div className="flex items-center gap-3">
                            <span className="text-2xl">{countryFlags[account.country_code] || '🌍'}</span>
                            <div>
                              <p className="font-medium text-text-light dark:text-text-dark">
                                {countryNames[account.country_code] || account.country_code}
                              </p>
                              <p className="text-sm text-subtle-light dark:text-subtle-dark">{account.country_code}</p>
                            </div>
                          </div>
                        </td>
                        <td className="p-4 align-middle">
                          <div className="font-mono text-sm text-text-light dark:text-text-dark">
                            {account.account_id.slice(0, 12)}...
                          </div>
                          <div className="text-xs text-subtle-light dark:text-subtle-dark">
                            {account.account_type}
                          </div>
                        </td>
                        <td className="p-4 align-middle">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/20 text-primary">
                            {account.network}
                          </span>
                          <div className="text-xs text-subtle-light dark:text-subtle-dark mt-1">
                            {account.environment}
                          </div>
                        </td>
                        <td className="p-4 align-middle">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            account.is_active 
                              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                          }`}>
                            {account.is_active ? 'Active' : 'Inactive'}
                          </span>
                          {account.is_verified && (
                            <div className="mt-1">
                              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                                Verified
                              </span>
                            </div>
                          )}
                        </td>
                        <td className="p-4 align-middle text-right">
                          <Link to={`/accounts/${account.id}`}>
                            <Button variant="ghost" size="sm" className="text-primary hover:text-primary/80">
                              View Details
                            </Button>
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
    </DashboardLayout>
  );
};

export default AccountManagement;
