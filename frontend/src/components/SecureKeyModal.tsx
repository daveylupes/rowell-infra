/**
 * Secure Key Download Modal
 * Handles secure display and download of private keys after account creation
 */

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { 
  AlertTriangle, 
  Copy, 
  Download, 
  Eye, 
  EyeOff, 
  CheckCircle2,
  Shield
} from 'lucide-react';
import { apiClient } from '@/lib/api';
import { toast } from 'sonner';

interface SecureKeyModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  accountId: string;
  token: string;
  network: string;
  accountType: string;
}

export function SecureKeyModal({
  open,
  onOpenChange,
  accountId,
  token,
  network,
  accountType,
}: SecureKeyModalProps) {
  const [privateKey, setPrivateKey] = useState<string | null>(null);
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);
  const [hasConfirmed, setHasConfirmed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [keyRetrieved, setKeyRetrieved] = useState(false);

  // Reset state when modal closes
  useEffect(() => {
    if (!open) {
      setPrivateKey(null);
      setShowKey(false);
      setCopied(false);
      setHasConfirmed(false);
      setKeyRetrieved(false);
    }
  }, [open]);

  const handleRetrieveKey = async () => {
    if (!hasConfirmed) {
      toast.error('Please confirm that you understand the security warning');
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.retrieveAccountKey(accountId, token);
      setPrivateKey(response.private_key);
      setKeyRetrieved(true);
      toast.success('Private key retrieved successfully');
    } catch (error: any) {
      toast.error('Failed to retrieve private key', {
        description: error.message || 'Token may be invalid or expired',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCopyKey = async () => {
    if (!privateKey) return;

    try {
      await navigator.clipboard.writeText(privateKey);
      setCopied(true);
      toast.success('Private key copied to clipboard', {
        description: '⚠️ Store it securely - clipboard will be cleared',
      });
      
      // Clear clipboard after 30 seconds
      setTimeout(() => {
        navigator.clipboard.writeText('');
        setCopied(false);
      }, 30000);
    } catch (error) {
      toast.error('Failed to copy to clipboard');
    }
  };

  const handleDownloadKey = () => {
    if (!privateKey) return;

    const blob = new Blob([privateKey], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${accountId}_${network}_private_key.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast.success('Private key downloaded', {
      description: 'Store this file securely and delete it after saving',
    });
  };

  const maskKey = (key: string) => {
    if (!showKey) {
      return '•'.repeat(key.length);
    }
    // Show first 8 and last 8 characters, mask the middle
    if (key.length > 20) {
      return `${key.slice(0, 8)}${'•'.repeat(key.length - 16)}${key.slice(-8)}`;
    }
    return key;
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-yellow-600" />
            Secure Private Key Retrieval
          </DialogTitle>
          <DialogDescription>
            Your private key is stored securely. You can retrieve it once using the token provided.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Security Warning */}
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              <strong>SECURITY WARNING:</strong> Your private key provides full access to your
              account. Store it securely - it cannot be recovered. Never share it or commit it to
              version control.
            </AlertDescription>
          </Alert>

          {/* Account Info */}
          <div className="space-y-2">
            <Label>Account Information</Label>
            <div className="grid grid-cols-2 gap-4 p-4 bg-muted rounded-lg">
              <div>
                <p className="text-sm text-muted-foreground">Account ID</p>
                <p className="font-mono text-sm">{accountId}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Network</p>
                <p className="text-sm capitalize">{network}</p>
              </div>
            </div>
          </div>

          {/* Key Retrieval Section */}
          {!keyRetrieved ? (
            <div className="space-y-4">
              <div className="flex items-start space-x-2">
                <Checkbox
                  id="confirm-security"
                  checked={hasConfirmed}
                  onCheckedChange={(checked) => setHasConfirmed(checked as boolean)}
                />
                <Label
                  htmlFor="confirm-security"
                  className="text-sm font-normal cursor-pointer"
                >
                  I understand that:
                  <ul className="list-disc list-inside mt-2 space-y-1 text-muted-foreground">
                    <li>This key provides full access to my account</li>
                    <li>I must store it securely and never share it</li>
                    <li>This key can only be retrieved once</li>
                    <li>If I lose this key, I cannot recover my account</li>
                  </ul>
                </Label>
              </div>

              <Button
                onClick={handleRetrieveKey}
                disabled={!hasConfirmed || loading}
                className="w-full"
              >
                {loading ? 'Retrieving...' : 'Retrieve Private Key'}
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <Alert>
                <CheckCircle2 className="h-4 w-4" />
                <AlertDescription>
                  Private key retrieved successfully. Store it securely - this is your only chance
                  to see it.
                </AlertDescription>
              </Alert>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label>Your Private Key</Label>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowKey(!showKey)}
                  >
                    {showKey ? (
                      <>
                        <EyeOff className="h-4 w-4 mr-2" />
                        Hide
                      </>
                    ) : (
                      <>
                        <Eye className="h-4 w-4 mr-2" />
                        Show
                      </>
                    )}
                  </Button>
                </div>
                <div className="p-4 bg-muted rounded-lg border-2 border-dashed">
                  <p className="font-mono text-sm break-all select-all">
                    {privateKey ? maskKey(privateKey) : 'No key retrieved'}
                  </p>
                </div>
              </div>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  onClick={handleCopyKey}
                  className="flex-1"
                  disabled={!privateKey}
                >
                  <Copy className="h-4 w-4 mr-2" />
                  {copied ? 'Copied!' : 'Copy Key'}
                </Button>
                <Button
                  variant="outline"
                  onClick={handleDownloadKey}
                  className="flex-1"
                  disabled={!privateKey}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              </div>

              <Alert>
                <AlertDescription className="text-sm">
                  <strong>Next Steps:</strong>
                  <ol className="list-decimal list-inside mt-2 space-y-1">
                    <li>Copy or download the key above</li>
                    <li>Store it in a secure password manager</li>
                    <li>Delete this modal and clear your clipboard</li>
                    <li>Never commit this key to version control</li>
                  </ol>
                </AlertDescription>
              </Alert>
            </div>
          )}

          <div className="flex justify-end gap-2 pt-4 border-t">
            <Button variant="outline" onClick={() => onOpenChange(false)}>
              {keyRetrieved ? 'I\'ve Stored This Securely' : 'Cancel'}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

