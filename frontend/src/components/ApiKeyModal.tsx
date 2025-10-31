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
import { 
  AlertTriangle, 
  Copy, 
  Eye, 
  EyeOff,
  CheckCircle2,
  Shield
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { toast } from 'sonner';

interface ApiKeyModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  apiKey: string;
  keyName: string;
}

export function ApiKeyModal({
  open,
  onOpenChange,
  apiKey,
  keyName,
}: ApiKeyModalProps) {
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!open) {
      setShowKey(false);
      setCopied(false);
    }
  }, [open]);

  const handleCopyKey = async () => {
    try {
      await navigator.clipboard.writeText(apiKey);
      setCopied(true);
      toast.success('API key copied to clipboard', {
        description: '⚠️ Store it securely - you won\'t see it again',
      });
      
      setTimeout(() => {
        setCopied(false);
      }, 3000);
    } catch (error) {
      toast.error('Failed to copy to clipboard');
    }
  };

  const maskKey = (key: string) => {
    if (!showKey) {
      return '•'.repeat(Math.min(key.length, 50));
    }
    if (key.length > 30) {
      return `${key.slice(0, 12)}${'•'.repeat(key.length - 24)}${key.slice(-12)}`;
    }
    return key;
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5 text-yellow-600" />
            Your New API Key
          </DialogTitle>
          <DialogDescription>
            Save this API key immediately - you won't be able to see it again after closing this dialog.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Security Warning */}
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              <strong>IMPORTANT:</strong> This is your only chance to copy this API key. Make sure to save it securely. 
              The full key will never be shown again for security reasons.
            </AlertDescription>
          </Alert>

          {/* Key Info */}
          <div className="space-y-2">
            <Label>API Key Name</Label>
            <div className="p-4 bg-gray-100 dark:bg-gray-900 rounded-lg">
              <p className="font-semibold text-deep-teal dark:text-white">{keyName}</p>
            </div>
          </div>

          {/* API Key Display */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>Your API Key</Label>
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
            <div className="flex items-center gap-2">
              <div className="flex-1 p-4 bg-gray-900 rounded-lg border border-gray-700">
                <code className="font-mono text-sm text-gray-300 break-all select-all">
                  {maskKey(apiKey)}
                </code>
              </div>
              <Button
                variant="outline"
                onClick={handleCopyKey}
                className="h-auto px-4"
              >
                <Copy className="h-4 w-4 mr-2" />
                {copied ? 'Copied!' : 'Copy'}
              </Button>
            </div>
          </div>

          <Alert>
            <CheckCircle2 className="h-4 w-4" />
            <AlertDescription className="text-sm">
              <strong>Usage Example:</strong>
              <pre className="mt-2 p-3 bg-gray-900 text-gray-300 rounded text-xs overflow-x-auto">
{`curl -X POST https://api.rowellinfra.com/api/v1/accounts/create \\
   -H "Authorization: Bearer ${apiKey.slice(0, 20)}..." \\
   -H "Content-Type: application/json" \\
   -d '{"network": "hedera"}'`}
              </pre>
            </AlertDescription>
          </Alert>

          <div className="flex justify-end gap-2 pt-4 border-t">
            <Button onClick={() => onOpenChange(false)} className="bg-gradient-to-r from-accent-start to-accent-end text-white">
              I've Saved This Key
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

