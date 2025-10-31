import { useState } from "react";
import { Button } from "@/components/ui/button";
import { DashboardLayout } from "@/components/DashboardLayout";
import { useDeveloperDashboard, useCreateAPIKey, useCreateProject } from "@/hooks/use-api";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogDescription } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { formatDistanceToNow } from "date-fns";
import { Copy, Trash2, Eye, EyeOff, Loader2 } from "lucide-react";
import { ApiKeyModal } from "@/components/ApiKeyModal";

const DeveloperDashboard = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'keys' | 'usage' | 'logs'>('overview');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);
  const [newKeyData, setNewKeyData] = useState<{ api_key: string; key_name: string } | null>(null);
  const [selectedProjectId, setSelectedProjectId] = useState<string>('');
  const [formData, setFormData] = useState({
    key_name: '',
    rate_limit: 1000,
    permissions: [] as string[],
  });

  const { data: dashboard, isLoading, refetch } = useDeveloperDashboard();
  const createKeyMutation = useCreateAPIKey();
  const createProjectMutation = useCreateProject();

  const apiKeys = dashboard?.api_keys || [];
  const projects = dashboard?.projects || [];
  const stats = dashboard?.stats || {
    total_projects: 0,
    total_api_keys: 0,
    active_api_keys: 0,
    total_usage: 0,
  };

  // Calculate today's requests (mock - would come from API)
  const requestsToday = Math.floor(stats.total_usage * 0.1) || 1247;
  const rateLimitUsage = requestsToday > stats.total_api_keys * 1000 ? 45 : Math.floor((requestsToday / (stats.total_api_keys * 1000 || 1000)) * 100);

  const handleCreateKey = async () => {
    if (!formData.key_name) {
      toast.error('Please enter a key name');
      return;
    }

    if (formData.permissions.length === 0) {
      toast.error('Please select at least one permission');
      return;
    }

    try {
      let projectId = selectedProjectId;

      // Auto-create a default project if none exists
      if (projects.length === 0 || !projectId) {
        toast.info('Creating default project first...');
        const newProject = await createProjectMutation.mutateAsync({
          name: 'Default Project',
          description: 'Default project for API keys',
          primary_network: 'hedera',
          environment: 'testnet',
        });
        projectId = newProject.id;
        setSelectedProjectId(projectId);
        // Wait a moment for the dashboard to refresh
        await new Promise(resolve => setTimeout(resolve, 500));
        await refetch();
      }

      if (!projectId) {
        toast.error('Failed to create or select project');
        return;
      }

      const result = await createKeyMutation.mutateAsync({
        projectId: projectId,
        request: {
          key_name: formData.key_name,
          permissions: formData.permissions,
          rate_limit: formData.rate_limit,
        },
      });

      setNewKeyData({
        api_key: result.api_key,
        key_name: result.key_name,
      });
      setIsCreateDialogOpen(false);
      setIsKeyModalOpen(true);
      setFormData({
        key_name: '',
        rate_limit: 1000,
        permissions: [],
      });
      setSelectedProjectId('');
      refetch();
    } catch (error) {
      // Error handled by mutation
    }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`${label} copied to clipboard`);
  };

  const togglePermission = (permission: string) => {
    setFormData(prev => ({
      ...prev,
      permissions: prev.permissions.includes(permission)
        ? prev.permissions.filter(p => p !== permission)
        : [...prev.permissions, permission],
    }));
  };

  const getStatusBadge = (key: any) => {
    if (!key.is_active) {
      return <span className="px-2 py-1 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 text-xs rounded-full font-medium">Revoked</span>;
    }
    if (key.expires_at && new Date(key.expires_at) < new Date()) {
      return <span className="px-2 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 text-xs rounded-full font-medium">Expired</span>;
    }
    return <span className="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs rounded-full font-medium">Active</span>;
  };

  // Mock usage logs - would come from API in production
  const mockLogs = [
    { id: '1', api_key_id: apiKeys[0]?.id || '', endpoint: '/api/v1/transfers/create', method: 'POST', status_code: 200, response_time_ms: 45, timestamp: new Date(Date.now() - 2 * 60000).toISOString() },
    { id: '2', api_key_id: apiKeys[0]?.id || '', endpoint: '/api/v1/accounts', method: 'GET', status_code: 200, response_time_ms: 23, timestamp: new Date(Date.now() - 5 * 60000).toISOString() },
    { id: '3', api_key_id: apiKeys[0]?.id || '', endpoint: '/api/v1/transfers/create', method: 'POST', status_code: 429, response_time_ms: 0, timestamp: new Date(Date.now() - 10 * 60000).toISOString(), error_message: 'Rate limit exceeded' },
  ];

  return (
    <DashboardLayout title="API Key Management" description="Manage and generate your programmatic access keys here">
      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
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
            onClick={() => setActiveTab('keys')}
            className={`py-3 border-b-2 transition-colors ${
              activeTab === 'keys'
                ? 'border-primary text-primary font-semibold'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
            }`}
          >
            API Keys
          </button>
          <button
            onClick={() => setActiveTab('usage')}
            className={`py-3 border-b-2 transition-colors ${
              activeTab === 'usage'
                ? 'border-primary text-primary font-semibold'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
            }`}
          >
            Usage
          </button>
          <button
            onClick={() => setActiveTab('logs')}
            className={`py-3 border-b-2 transition-colors ${
              activeTab === 'logs'
                ? 'border-primary text-primary font-semibold'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-primary hover:border-primary'
            }`}
          >
            Logs
          </button>
        </nav>
      </div>

      {/* Content based on active tab */}
      {isLoading ? (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} className="h-32 rounded-xl" />
            ))}
          </div>
          <Skeleton className="h-64 rounded-xl" />
        </div>
      ) : activeTab === 'overview' ? (
        <div className="space-y-8">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white dark:bg-gray-800/50 p-6 rounded-xl shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">API Keys</p>
                  <p className="text-2xl font-bold text-deep-teal dark:text-white">{stats.total_api_keys}</p>
                </div>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary">vpn_key</span>
                </div>
              </div>
              <p className="text-sm text-green-600 dark:text-green-400 mt-2">{stats.active_api_keys} active</p>
            </div>

            <div className="bg-white dark:bg-gray-800/50 p-6 rounded-xl shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Requests Today</p>
                  <p className="text-2xl font-bold text-deep-teal dark:text-white">{requestsToday.toLocaleString()}</p>
                </div>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary">trending_up</span>
                </div>
              </div>
              <p className="text-sm text-green-600 dark:text-green-400 mt-2">+15.3% from yesterday</p>
            </div>

            <div className="bg-white dark:bg-gray-800/50 p-6 rounded-xl shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Rate Limit</p>
                  <p className="text-2xl font-bold text-deep-teal dark:text-white">{stats.total_api_keys > 0 ? `${stats.total_api_keys * 1000}/h` : '1,000/h'}</p>
                </div>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary">speed</span>
                </div>
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">Current usage: {rateLimitUsage}%</p>
            </div>

            <div className="bg-white dark:bg-gray-800/50 p-6 rounded-xl shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Success Rate</p>
                  <p className="text-2xl font-bold text-deep-teal dark:text-white">99.8%</p>
                </div>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary">check_circle</span>
                </div>
              </div>
              <p className="text-sm text-green-600 dark:text-green-400 mt-2">+0.2% from last week</p>
            </div>
          </div>

          {/* API Usage Overview Card */}
          <div className="flex flex-col rounded-xl shadow-[0_4px_12px_rgba(0,0,0,0.05)] bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 p-6 gap-6">
            <h2 className="text-deep-teal dark:text-white text-lg font-bold leading-tight tracking-[-0.015em]">API Usage Overview</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 -mt-4">Last 30 Days</p>
            <div className="flex flex-col gap-2">
              <p className="text-sm text-gray-500 dark:text-gray-400">Success Rate</p>
              <p className="text-4xl font-bold from-accent-start to-accent-end bg-gradient-to-r text-transparent bg-clip-text">99.8%</p>
            </div>
            <div className="w-full h-32 bg-gray-100 dark:bg-gray-900 rounded-lg flex items-center justify-center">
              <svg className="w-full h-full text-gray-300 dark:text-gray-600" fill="none" preserveAspectRatio="none" viewBox="0 0 100 40" xmlns="http://www.w3.org/2000/svg">
                <path d="M0 30 C 10 10, 20 10, 30 20 S 50 40, 60 25 S 80 0, 90 15 S 100 20, 100 20" stroke="url(#lineGradient)" strokeWidth="2" vectorEffect="non-scaling-stroke"></path>
                <defs>
                  <linearGradient gradientUnits="userSpaceOnUse" id="lineGradient" x1="0" x2="100" y1="0" y2="0">
                    <stop stopColor="#10b981"></stop>
                    <stop offset="1" stopColor="#06b6d4"></stop>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div className="flex flex-col gap-2 pt-4 border-t border-gray-200 dark:border-gray-700">
              <p className="text-sm text-gray-500 dark:text-gray-400">Total Requests</p>
              <p className="text-2xl font-bold text-deep-teal dark:text-white">{stats.total_usage.toLocaleString()}</p>
            </div>
          </div>
        </div>
      ) : activeTab === 'keys' ? (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-deep-teal dark:text-white">Your Programmatic Access</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage and generate your API keys</p>
            </div>
            <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
              <DialogTrigger asChild>
                <Button className="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-5 bg-gradient-to-r from-accent-start to-accent-end text-white text-sm font-bold leading-normal shadow-lg hover:shadow-xl transition-shadow">
                  <span className="truncate">Generate New API Key</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle>Create New API Key</DialogTitle>
                  <DialogDescription>
                    Generate a new API key for your project. You'll only see the key once, so make sure to copy it.
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label htmlFor="key_name">Key Name *</Label>
                    <Input
                      id="key_name"
                      placeholder="e.g., Production Key, Test Key"
                      value={formData.key_name}
                      onChange={(e) => setFormData(prev => ({ ...prev, key_name: e.target.value }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="project">Project *</Label>
                    <Select value={selectedProjectId} onValueChange={setSelectedProjectId}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a project" />
                      </SelectTrigger>
                      <SelectContent>
                        {projects.length > 0 ? (
                          projects.map((project) => (
                            <SelectItem key={project.id} value={project.id}>
                              {project.name} ({project.environment})
                            </SelectItem>
                          ))
                        ) : (
                          <SelectItem value="no-projects" disabled>No projects available</SelectItem>
                        )}
                      </SelectContent>
                    </Select>
                    {projects.length === 0 && (
                      <div className="space-y-2">
                        <p className="text-xs text-gray-500">No projects yet. A default project will be created automatically when you generate an API key.</p>
                        <p className="text-xs text-blue-600 dark:text-blue-400">💡 Tip: You can create projects manually later in the developer dashboard</p>
                      </div>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="rate_limit">Rate Limit (requests/hour)</Label>
                    <Input
                      id="rate_limit"
                      type="number"
                      min="1"
                      max="10000"
                      value={formData.rate_limit}
                      onChange={(e) => setFormData(prev => ({ ...prev, rate_limit: parseInt(e.target.value) || 1000 }))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Permissions *</Label>
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                      {[
                        { id: 'accounts:read', label: 'Read Accounts' },
                        { id: 'accounts:write', label: 'Create/Update Accounts' },
                        { id: 'transfers:read', label: 'Read Transfers' },
                        { id: 'transfers:write', label: 'Create Transfers' },
                        { id: 'analytics:read', label: 'Read Analytics' },
                      ].map((perm) => (
                        <div key={perm.id} className="flex items-center space-x-2">
                          <Checkbox
                            id={perm.id}
                            checked={formData.permissions.includes(perm.id)}
                            onCheckedChange={() => togglePermission(perm.id)}
                          />
                          <Label htmlFor={perm.id} className="text-sm font-normal cursor-pointer">
                            {perm.label}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                  <Button
                    onClick={handleCreateKey}
                    disabled={createKeyMutation.isPending || createProjectMutation.isPending}
                    className="w-full bg-gradient-to-r from-accent-start to-accent-end text-white"
                  >
                    {createKeyMutation.isPending || createProjectMutation.isPending ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        {createProjectMutation.isPending ? 'Creating project...' : 'Creating API key...'}
                      </>
                    ) : (
                      'Generate API Key'
                    )}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* API Keys List */}
          {apiKeys.length === 0 ? (
            <div className="bg-white dark:bg-gray-800/50 p-12 rounded-xl border border-gray-200 dark:border-gray-700 text-center">
              <span className="material-symbols-outlined text-6xl text-gray-300 dark:text-gray-600 mb-4">vpn_key</span>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No API Keys Yet</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                Generate your first API key to start using the Rowell Infra API
              </p>
              <Button
                onClick={() => setIsCreateDialogOpen(true)}
                className="bg-gradient-to-r from-accent-start to-accent-end text-white"
              >
                Generate New API Key
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              {apiKeys.map((key) => (
                <div
                  key={key.id}
                  className="flex flex-col rounded-lg bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 p-4"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                        key.is_active
                          ? 'bg-green-100 dark:bg-green-900'
                          : 'bg-red-100 dark:bg-red-900'
                      }`}>
                        <span className={`material-symbols-outlined ${
                          key.is_active ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {key.is_active ? 'check' : 'block'}
                        </span>
                      </div>
                      <div>
                        <h4 className="font-medium text-deep-teal dark:text-white">{key.key_name}</h4>
                        <code className="text-sm text-gray-500 dark:text-gray-400 font-mono">
                          {key.key_prefix}...
                        </code>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      {getStatusBadge(key)}
                      <Button
                        variant="outline"
                        size="sm"
                        className="h-8 w-8 p-0"
                        onClick={() => copyToClipboard(key.key_prefix, 'Key prefix')}
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  <div className="mt-4 flex flex-wrap items-center gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <div className="flex h-7 shrink-0 items-center justify-center gap-x-2 rounded-full bg-gray-200 dark:bg-gray-700 px-3">
                      <p className="text-sm font-medium text-gray-600 dark:text-gray-300">
                        Rate Limit: {key.rate_limit}/h
                      </p>
                    </div>
                    {key.last_used && (
                      <div className="flex h-7 shrink-0 items-center justify-center gap-x-2 rounded-full bg-gray-200 dark:bg-gray-700 px-3">
                        <p className="text-sm font-medium text-gray-600 dark:text-gray-300">
                          Last Used: {formatDistanceToNow(new Date(key.last_used), { addSuffix: true })}
                        </p>
                      </div>
                    )}
                    <div className="flex h-7 shrink-0 items-center justify-center gap-x-2 rounded-full bg-gray-200 dark:bg-gray-700 px-3">
                      <p className="text-sm font-medium text-gray-600 dark:text-gray-300">
                        Usage: {key.usage_count.toLocaleString()}
                      </p>
                    </div>
                    <div className="flex-grow"></div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Revoke Key
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : activeTab === 'usage' ? (
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800/50 p-6 rounded-xl shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-deep-teal dark:text-white mb-4">API Usage (Last 7 Days)</h3>
            <div className="h-64 bg-gray-100 dark:bg-gray-900 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <p className="text-gray-500 dark:text-gray-400 mb-2">Usage Chart</p>
                <p className="text-sm text-gray-400 dark:text-gray-500">Visualization coming soon</p>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800/50 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
              <h4 className="font-semibold text-deep-teal dark:text-white mb-4">Requests by Endpoint</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-300">/api/v1/transfers/create</span>
                  <span className="text-sm font-medium text-deep-teal dark:text-white">45%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-300">/api/v1/accounts</span>
                  <span className="text-sm font-medium text-deep-teal dark:text-white">30%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-300">/api/v1/analytics</span>
                  <span className="text-sm font-medium text-deep-teal dark:text-white">25%</span>
                </div>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800/50 p-6 rounded-xl border border-gray-200 dark:border-gray-700">
              <h4 className="font-semibold text-deep-teal dark:text-white mb-4">Usage Summary</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Total Requests</span>
                  <span className="text-sm font-medium text-deep-teal dark:text-white">{stats.total_usage.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Success Rate</span>
                  <span className="text-sm font-medium text-green-600 dark:text-green-400">99.8%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-300">Avg Response Time</span>
                  <span className="text-sm font-medium text-deep-teal dark:text-white">34ms</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-white dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-deep-teal dark:text-white">Recent API Calls</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Monitor your API request logs in real-time</p>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {mockLogs.map((log) => (
              <div key={log.id} className="flex items-center justify-between py-4 px-6 hover:bg-gray-50 dark:hover:bg-gray-900/50 transition-colors">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    log.status_code < 400
                      ? 'bg-green-100 dark:bg-green-900'
                      : 'bg-red-100 dark:bg-red-900'
                  }`}>
                    <span className={`material-symbols-outlined text-sm ${
                      log.status_code < 400 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {log.status_code < 400 ? 'check' : 'close'}
                    </span>
                  </div>
                  <div>
                    <p className="text-deep-teal dark:text-white font-medium">
                      {log.method} {log.endpoint}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {log.status_code} {log.status_code === 200 ? 'OK' : log.status_code === 429 ? 'Rate Limited' : 'Error'} • {log.response_time_ms}ms
                      {log.error_message && ` • ${log.error_message}`}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {formatDistanceToNow(new Date(log.timestamp), { addSuffix: true })}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* API Key Modal */}
      {newKeyData && (
        <ApiKeyModal
          open={isKeyModalOpen}
          onOpenChange={(open) => {
            setIsKeyModalOpen(open);
            if (!open) {
              setNewKeyData(null);
            }
          }}
          apiKey={newKeyData.api_key}
          keyName={newKeyData.key_name}
        />
      )}
    </DashboardLayout>
  );
};

export default DeveloperDashboard;
