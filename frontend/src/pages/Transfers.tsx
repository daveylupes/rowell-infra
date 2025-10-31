import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useTransfers, useCreateTransfer, useAccounts } from "@/hooks/use-api";
import { toast } from "sonner";
import { Skeleton } from "@/components/ui/skeleton";
import { formatDistanceToNow } from "date-fns";
import { Loader2, CheckCircle2, XCircle, Clock } from "lucide-react";
import { DashboardLayout } from "@/components/DashboardLayout";

const Transfers = () => {
  const [activeTab, setActiveTab] = useState<'send' | 'history'>('send');
  const [formData, setFormData] = useState({
    from_account: '',
    to_account: '',
    asset_code: 'HBAR',
    amount: '',
    network: 'hedera',
    environment: 'testnet',
    memo: '',
    from_country: '',
    to_country: ''
  });

  const { data: transfers, isLoading: transfersLoading, refetch: refetchTransfers } = useTransfers({ limit: 20 });
  const { data: accounts } = useAccounts();
  const createTransferMutation = useCreateTransfer();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.from_account || !formData.to_account || !formData.amount) {
      toast.error('Please fill in all required fields');
      return;
    }

    try {
      await createTransferMutation.mutateAsync({
        from_account: formData.from_account,
        to_account: formData.to_account,
        asset_code: formData.asset_code,
        amount: formData.amount,
        network: formData.network as 'stellar' | 'hedera',
        environment: formData.environment as 'testnet' | 'mainnet',
        memo: formData.memo || undefined,
        from_country: formData.from_country || undefined,
        to_country: formData.to_country || undefined,
      });
      
      // Reset form
      setFormData({
        from_account: '',
        to_account: '',
        asset_code: 'HBAR',
        amount: '',
        network: 'hedera',
        environment: 'testnet',
        memo: '',
        from_country: '',
        to_country: ''
      });
      
      // Switch to history tab
      setActiveTab('history');
      refetchTransfers();
    } catch (error) {
      // Error handling is done in the mutation
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle2 className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />;
      case 'pending':
        return <Clock className="h-4 w-4 text-yellow-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  const countries = [
    { code: "NG", name: "Nigeria" },
    { code: "KE", name: "Kenya" },
    { code: "GH", name: "Ghana" },
    { code: "ZA", name: "South Africa" },
    { code: "UG", name: "Uganda" },
    { code: "TZ", name: "Tanzania" },
  ];

  return (
    <DashboardLayout title="Transfers" description="Send money across Africa quickly and securely">
      {/* Navigation Tabs */}
        <div className="border-b border-black/10 dark:border-white/10 mb-6">
          <nav className="flex gap-8">
            <button
              onClick={() => setActiveTab('send')}
              className={`py-3 border-b-2 transition-colors ${
                activeTab === 'send'
                  ? 'border-primary text-primary font-semibold'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
              }`}
            >
              Send
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`py-3 border-b-2 transition-colors ${
                activeTab === 'history'
                  ? 'border-primary text-primary font-semibold'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
              }`}
            >
              History
            </button>
          </nav>
        </div>

        {/* Content */}
        {activeTab === 'send' ? (
          <div className="max-w-xl mx-auto bg-background-light/50 dark:bg-background-dark/50 p-8 rounded-xl shadow-lg">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" htmlFor="from_account">
                  From Account *
                </label>
                <select
                  id="from_account"
                  value={formData.from_account}
                  onChange={(e) => setFormData({ ...formData, from_account: e.target.value })}
                  className="w-full bg-white dark:bg-black/20 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:ring-primary focus:border-primary text-gray-900 dark:text-white p-3"
                  required
                >
                  <option value="">Select source account</option>
                  {accounts?.map((account) => {
                    // Safely convert account_id to string and handle edge cases
                    let displayId = account.account_id;
                    if (typeof displayId !== 'string') {
                      displayId = String(displayId);
                    }
                    // If it's a Java object string, try to extract just the ID
                    if (displayId.includes('<com.hedera')) {
                      displayId = 'Invalid Account';
                    }
                    return (
                      <option key={account.id} value={account.account_id}>
                        {displayId}
                      </option>
                    );
                  })}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" htmlFor="to_account">
                  To Account *
                </label>
                <input
                  id="to_account"
                  type="text"
                  value={formData.to_account}
                  onChange={(e) => setFormData({ ...formData, to_account: e.target.value })}
                  className="w-full bg-white dark:bg-black/20 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:ring-primary focus:border-primary text-gray-900 dark:text-white p-3"
                  placeholder="Enter destination account ID"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" htmlFor="amount">
                    Amount *
                  </label>
                  <input
                    id="amount"
                    type="number"
                    step="0.0000001"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                    className="w-full bg-white dark:bg-black/20 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:ring-primary focus:border-primary text-gray-900 dark:text-white p-3"
                    placeholder="0.00"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" htmlFor="asset_code">
                    Asset *
                  </label>
                  <select
                    id="asset_code"
                    value={formData.asset_code}
                    onChange={(e) => setFormData({ ...formData, asset_code: e.target.value })}
                    className="w-full bg-white dark:bg-black/20 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:ring-primary focus:border-primary text-gray-900 dark:text-white p-3"
                    required
                  >
                    <option value="HBAR">HBAR</option>
                    <option value="USDC">USDC</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" htmlFor="network">
                    Network *
                  </label>
                  <select
                    id="network"
                    value={formData.network}
                    onChange={(e) => setFormData({ ...formData, network: e.target.value })}
                    className="w-full bg-white dark:bg-black/20 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:ring-primary focus:border-primary text-gray-900 dark:text-white p-3"
                    required
                  >
                    <option value="hedera">Hedera</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" htmlFor="environment">
                    Environment *
                  </label>
                  <select
                    id="environment"
                    value={formData.environment}
                    onChange={(e) => setFormData({ ...formData, environment: e.target.value })}
                    className="w-full bg-white dark:bg-black/20 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:ring-primary focus:border-primary text-gray-900 dark:text-white p-3"
                    required
                  >
                    <option value="testnet">Testnet</option>
                    <option value="mainnet">Mainnet</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" htmlFor="memo">
                  Memo (Optional)
                </label>
                <input
                  id="memo"
                  type="text"
                  value={formData.memo}
                  onChange={(e) => setFormData({ ...formData, memo: e.target.value })}
                  className="w-full bg-white dark:bg-black/20 border border-gray-300 dark:border-gray-700 rounded-lg shadow-sm focus:ring-primary focus:border-primary text-gray-900 dark:text-white p-3"
                  placeholder="Transfer memo"
                />
              </div>

              <div className="flex justify-end pt-4">
                <Button
                  type="submit"
                  disabled={createTransferMutation.isPending}
                  className="w-full sm:w-auto bg-primary text-white font-semibold py-3 px-8 rounded-lg hover:bg-primary/90 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {createTransferMutation.isPending ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      Continue
                      <span className="material-symbols-outlined">arrow_forward</span>
                    </>
                  )}
                </Button>
              </div>
            </form>
          </div>
        ) : (
          <div className="bg-background-light/50 dark:bg-background-dark/50 rounded-xl shadow-lg overflow-hidden">
            {transfersLoading ? (
              <div className="p-6 space-y-4">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Skeleton key={i} className="h-16 w-full" />
                ))}
              </div>
            ) : transfers && transfers.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-32">
                        Transaction
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Accounts
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-28">
                        Amount
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-24">
                        Network
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-24">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-32">
                        Date
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                    {transfers.map((transfer) => (
                      <tr key={transfer.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                        <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                          <div className="font-mono text-xs break-all">{transfer.transaction_hash.slice(0, 16)}...</div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                          <div className="flex flex-col gap-1">
                            <div className="font-mono text-xs">
                              <span className="text-gray-700 dark:text-gray-300 font-medium">From:</span> {transfer.from_account || 'N/A'}
                            </div>
                            <div className="font-mono text-xs">
                              <span className="text-gray-700 dark:text-gray-300 font-medium">To:</span> {transfer.to_account || 'N/A'}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                          {transfer.amount} {transfer.asset_code}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          <span className="px-2 py-1 text-xs font-medium rounded bg-primary/10 text-primary">
                            {transfer.network}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center gap-2">
                            {getStatusIcon(transfer.status)}
                            <span className={`text-sm font-medium ${
                              transfer.status === 'success' ? 'text-green-600 dark:text-green-400' :
                              transfer.status === 'failed' ? 'text-red-600 dark:text-red-400' :
                              'text-yellow-600 dark:text-yellow-400'
                            }`}>
                              {transfer.status}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                          {transfer.created_at ? formatDistanceToNow(new Date(transfer.created_at), { addSuffix: true }) : 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="p-12 text-center">
                <p className="text-gray-500 dark:text-gray-400">No transfers found</p>
                <Button
                  onClick={() => setActiveTab('send')}
                  className="mt-4 bg-primary text-white"
                >
                  Create First Transfer
                </Button>
              </div>
            )}
          </div>
        )}
    </DashboardLayout>
  );
};

export default Transfers;
