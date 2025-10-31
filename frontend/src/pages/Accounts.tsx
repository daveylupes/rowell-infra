import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { Plus, Search, Eye, Edit, Copy, ExternalLink, AlertCircle, RefreshCw } from "lucide-react";
import { useState } from "react";
import { useAccounts, useCreateAccount, useAccountBalances } from "@/hooks/use-api";
import { formatDistanceToNow } from "date-fns";
import { toast } from "sonner";
import { SecureKeyModal } from "@/components/SecureKeyModal";
import { DashboardLayout } from "@/components/DashboardLayout";

// Component to display account balance
// Note: accountId here is the internal database ID (UUID), not the blockchain account_id
const AccountBalanceCell = ({ accountId, network }: { accountId: string; network: string }) => {
  const { data: balances, isLoading } = useAccountBalances(accountId);
  
  if (isLoading) {
    return <span className="text-muted-foreground">Loading...</span>;
  }
  
  if (!balances || balances.length === 0) {
    return <span className="text-muted-foreground">0 {network === 'hedera' ? 'HBAR' : 'XLM'}</span>;
  }
  
  const mainBalance = balances[0];
  return (
    <div className="flex flex-col">
      <span className="font-medium">{mainBalance.balance} {mainBalance.asset_code}</span>
      {mainBalance.balance_usd && (
        <span className="text-xs text-muted-foreground">${mainBalance.balance_usd}</span>
      )}
    </div>
  );
};

const Accounts = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterNetwork, setFilterNetwork] = useState<string>("all");
  const [filterCountry, setFilterCountry] = useState<string>("all");
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);
  const [newAccountKeyData, setNewAccountKeyData] = useState<{
    accountId: string;
    token: string;
    network: string;
    accountType: string;
  } | null>(null);
  const [createFormData, setCreateFormData] = useState({
    network: '',
    environment: 'testnet',
    account_type: '',
    country_code: '',
    region: ''
  });

  // Build API params from filters
  const apiParams = {
    network: filterNetwork !== "all" ? filterNetwork : undefined,
    country_code: filterCountry !== "all" ? filterCountry : undefined,
    limit: 1000, // Get enough to filter client-side
  };

  // API hooks - pass filters to API
  const { data: accountsResponse, isLoading, isError, refetch } = useAccounts(apiParams);
  const createAccountMutation = useCreateAccount();

  // Extract accounts array from response (handle both formats)
  const accounts = accountsResponse?.accounts || (Array.isArray(accountsResponse) ? accountsResponse : []) || [];

  // Apply client-side filtering for search and status (since API doesn't support search/status filtering yet)
  const filteredAccounts = accounts.filter(account => {
    // Search filter
    const matchesSearch = !searchQuery || 
      account.account_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      account.network.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (account.country_code && account.country_code.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (account.account_type && account.account_type.toLowerCase().includes(searchQuery.toLowerCase()));

    // Status filter
    const matchesStatus = filterStatus === "all" ||
      (filterStatus === "active" && account.is_active) ||
      (filterStatus === "pending" && account.kyc_status === "pending") ||
      (filterStatus === "suspended" && !account.is_active);

    return matchesSearch && matchesStatus;
  });

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

  const handleCreateAccount = async () => {
    if (!createFormData.network || !createFormData.account_type || !createFormData.country_code) {
      toast.error('Please fill in all required fields');
      return;
    }

    try {
      const newAccount = await createAccountMutation.mutateAsync(createFormData);
      
      // Close create dialog
      setIsCreateDialogOpen(false);
      setCreateFormData({
        network: '',
        environment: 'testnet',
        account_type: '',
        country_code: '',
        region: ''
      });

      // Show success message with HashScan link for Hedera accounts
      if (newAccount.network === 'hedera') {
        const explorerUrl = `https://hashscan.io/${newAccount.environment === 'mainnet' ? 'mainnet' : 'testnet'}/account/${newAccount.account_id}`;
        toast.success('Real Account Created on Blockchain!', {
          description: `View on HashScan: ${newAccount.account_id}`,
          action: {
            label: 'Open HashScan',
            onClick: () => window.open(explorerUrl, '_blank', 'noopener,noreferrer')
          },
          duration: 6000
        });
      } else {
        toast.success('Account created successfully');
      }

      // Open secure key modal if token is provided
      if (newAccount.key_retrieval_token) {
        setNewAccountKeyData({
          accountId: newAccount.id,  // Use internal UUID, not blockchain account_id
          token: newAccount.key_retrieval_token,
          network: newAccount.network,
          accountType: newAccount.account_type,
        });
        setIsKeyModalOpen(true);
      }

      // Refresh accounts list
      refetch();
    } catch (error) {
      // Error handling is done in the mutation
    }
  };

  // Handle errors
  if (isError) {
    return (
      <DashboardLayout title="Accounts" description="Manage your Hedera accounts across African markets">
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

  const countries = [
    { code: "NG", name: "Nigeria", flag: "🇳🇬" },
    { code: "KE", name: "Kenya", flag: "🇰🇪" },
    { code: "ZA", name: "South Africa", flag: "🇿🇦" },
    { code: "GH", name: "Ghana", flag: "🇬🇭" },
    { code: "UG", name: "Uganda", flag: "🇺🇬" },
    { code: "TZ", name: "Tanzania", flag: "🇹🇿" },
    { code: "ET", name: "Ethiopia", flag: "🇪🇹" },
    { code: "EG", name: "Egypt", flag: "🇪🇬" },
    { code: "MA", name: "Morocco", flag: "🇲🇦" },
    { code: "TN", name: "Tunisia", flag: "🇹🇳" }
  ];

  const truncateAddress = (address: string) => {
    if (address.length <= 20) return address;
    return `${address.slice(0, 8)}...${address.slice(-8)}`;
  };

  return (
    <DashboardLayout title="Accounts" description="Manage your Hedera accounts across African markets">
      <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
        <DialogTrigger asChild>
          <Button className="mb-6">
            <Plus className="h-4 w-4 mr-2" />
            Create Account
          </Button>
        </DialogTrigger>
                <DialogContent className="sm:max-w-md">
                  <DialogHeader>
                    <DialogTitle>Create New Account</DialogTitle>
                  </DialogHeader>
                  <div className="space-y-4 py-4">
                    <div className="space-y-2">
                      <Label htmlFor="network">Network *</Label>
                      <Select 
                        value={createFormData.network} 
                        onValueChange={(value) => setCreateFormData(prev => ({ ...prev, network: value }))}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select network" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="hedera">Hedera</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="environment">Environment</Label>
                      <Select 
                        value={createFormData.environment} 
                        onValueChange={(value) => setCreateFormData(prev => ({ ...prev, environment: value }))}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select environment" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="testnet">Testnet</SelectItem>
                          <SelectItem value="mainnet">Mainnet</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="type">Account Type *</Label>
                      <Select 
                        value={createFormData.account_type} 
                        onValueChange={(value) => setCreateFormData(prev => ({ ...prev, account_type: value }))}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="user">User</SelectItem>
                          <SelectItem value="merchant">Merchant</SelectItem>
                          <SelectItem value="anchor">Anchor</SelectItem>
                          <SelectItem value="ngo">NGO</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div className="space-y-2">
                      <Label htmlFor="country">Country *</Label>
                      <Select 
                        value={createFormData.country_code} 
                        onValueChange={(value) => setCreateFormData(prev => ({ ...prev, country_code: value }))}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select country" />
                        </SelectTrigger>
                        <SelectContent>
                          {countries.map((country) => (
                            <SelectItem key={country.code} value={country.code}>
                              {country.flag} {country.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <Button 
                      className="w-full" 
                      onClick={handleCreateAccount}
                      disabled={createAccountMutation.isPending}
                    >
                      {createAccountMutation.isPending ? (
                        <>
                          <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                          {createFormData.network === 'hedera' ? 'Creating on Blockchain (3-4s)...' : 'Creating...'}
                        </>
                      ) : (
                        'Create Account'
                      )}
                    </Button>
                    {createFormData.network === 'hedera' && (
                      <p className="text-xs text-muted-foreground text-center">
                        💡 Creating a real Hedera account. This takes 3-4 seconds and creates an account on the blockchain.
                      </p>
                    )}
                  </div>
                </DialogContent>
              </Dialog>

        {/* Filters and Search */}
        <Card className="card-rowell mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by account ID or country..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="flex gap-2">
              <Select value={filterNetwork} onValueChange={setFilterNetwork}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Network" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Networks</SelectItem>
                  <SelectItem value="hedera">Hedera</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="suspended">Suspended</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filterCountry} onValueChange={setFilterCountry}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="Country" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Countries</SelectItem>
                  {countries.map((country) => (
                    <SelectItem key={country.code} value={country.code}>
                      {country.flag} {country.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </Card>

        {/* Accounts Table */}
        <Card className="card-rowell">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Network</th>
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Account ID</th>
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Balance</th>
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Status</th>
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Country</th>
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Type</th>
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Created</th>
                  <th className="text-left py-4 px-4 font-medium text-muted-foreground">Actions</th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  // Loading skeleton
                  Array.from({ length: 5 }).map((_, index) => (
                    <tr key={index} className="border-b border-border">
                      <td className="py-4 px-4">
                        <Skeleton className="h-6 w-16" />
                      </td>
                      <td className="py-4 px-4">
                        <Skeleton className="h-6 w-32" />
                      </td>
                      <td className="py-4 px-4">
                        <Skeleton className="h-6 w-20" />
                      </td>
                      <td className="py-4 px-4">
                        <Skeleton className="h-6 w-16" />
                      </td>
                      <td className="py-4 px-4">
                        <Skeleton className="h-6 w-24" />
                      </td>
                      <td className="py-4 px-4">
                        <Skeleton className="h-6 w-16" />
                      </td>
                      <td className="py-4 px-4">
                        <Skeleton className="h-6 w-20" />
                      </td>
                      <td className="py-4 px-4">
                        <Skeleton className="h-8 w-24" />
                      </td>
                    </tr>
                  ))
                ) : filteredAccounts.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="py-12 text-center">
                      <div className="text-muted-foreground">
                        {searchQuery ? 'No accounts found matching your search.' : 'No accounts found. Create your first account to get started.'}
                      </div>
                    </td>
                  </tr>
                ) : (
                  filteredAccounts.map((account) => (
                    <tr key={account.id} className="border-b border-border hover:bg-muted/30">
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          <Badge className="bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-200 network-badge">
                            {account.network.charAt(0).toUpperCase() + account.network.slice(1)}
                          </Badge>
                          {account.network === 'hedera' && (
                            <Badge className="bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200 text-xs">
                              Real
                            </Badge>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          <code className="text-sm bg-muted px-2 py-1 rounded font-mono">
                            {account.network === 'hedera' && account.account_id.match(/^0\.0\.\d+$/) 
                              ? account.account_id 
                              : truncateAddress(account.account_id)}
                          </code>
                          <Button 
                            size="sm" 
                            variant="ghost" 
                            className="h-6 w-6 p-0"
                            onClick={() => {
                              navigator.clipboard.writeText(account.account_id);
                              toast.success('Account ID copied to clipboard');
                            }}
                            title="Copy Account ID"
                          >
                            <Copy className="h-3 w-3" />
                          </Button>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <AccountBalanceCell accountId={account.id} network={account.network} />
                      </td>
                      <td className="py-4 px-4">
                        <Badge 
                          className={`status-badge ${
                            account.is_active ? 'status-active' : 
                            account.kyc_status === 'pending' ? 'status-pending' : 
                            'bg-red-100 text-red-700'
                          }`}
                        >
                          {account.is_active ? 'active' : 'inactive'}
                        </Badge>
                      </td>
                      <td className="py-4 px-4">
                        <div className="country-display">
                          <span>{countryFlags[account.country_code] || '🌍'}</span>
                          <span>{countryNames[account.country_code] || account.country_code}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <span className="text-sm capitalize">{account.account_type}</span>
                      </td>
                      <td className="py-4 px-4">
                        <span className="text-sm text-muted-foreground">
                          {formatDistanceToNow(new Date(account.created_at), { addSuffix: true })}
                        </span>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          {account.network === 'hedera' && (
                            <Button 
                              size="sm" 
                              variant="ghost" 
                              className="h-8 w-8 p-0"
                              title="View on HashScan Explorer"
                              onClick={() => {
                                const explorerUrl = `https://hashscan.io/${account.environment === 'mainnet' ? 'mainnet' : 'testnet'}/account/${account.account_id}`;
                                window.open(explorerUrl, '_blank', 'noopener,noreferrer');
                              }}
                            >
                              <ExternalLink className="h-3 w-3" />
                            </Button>
                          )}
                          <Button 
                            size="sm" 
                            variant="ghost" 
                            className="h-8 w-8 p-0"
                            onClick={() => {
                              navigator.clipboard.writeText(account.account_id);
                              toast.success('Account ID copied to clipboard');
                            }}
                            title="Copy Account ID"
                          >
                            <Copy className="h-3 w-3" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          
          {/* Pagination */}
          <div className="flex items-center justify-between px-4 py-4 border-t border-border">
            <div className="text-sm text-muted-foreground">
              Showing {filteredAccounts.length} of {accounts.length} account{accounts.length !== 1 ? 's' : ''}
              {filteredAccounts.length !== accounts.length && ` (filtered from ${accounts.length} total)`}
            </div>
            {(filterNetwork !== "all" || filterCountry !== "all" || filterStatus !== "all" || searchQuery) && (
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => {
                  setFilterNetwork("all");
                  setFilterCountry("all");
                  setFilterStatus("all");
                  setSearchQuery("");
                }}
              >
                Clear Filters
              </Button>
            )}
          </div>
        </Card>

      {/* Secure Key Modal */}
      {newAccountKeyData && (
        <SecureKeyModal
          open={isKeyModalOpen}
          onOpenChange={(open) => {
            setIsKeyModalOpen(open);
            if (!open) {
              setNewAccountKeyData(null);
            }
          }}
          accountId={newAccountKeyData.accountId}
          token={newAccountKeyData.token}
          network={newAccountKeyData.network}
          accountType={newAccountKeyData.accountType}
        />
      )}
    </DashboardLayout>
  );
};

export default Accounts;