/**
 * Transfer Progress Component
 * Shows multi-step progress indicator for transfer execution
 */

import { CheckCircle2, Circle, Loader2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export type TransferStatus = 
  | "idle" 
  | "validating" 
  | "submitting" 
  | "pending" 
  | "success" 
  | "failed";

interface TransferProgressProps {
  status: TransferStatus;
  error?: string;
  className?: string;
}

interface Step {
  id: string;
  label: string;
  status: "pending" | "active" | "completed" | "error";
}

export function TransferProgress({ status, error, className }: TransferProgressProps) {
  const getSteps = (): Step[] => {
    switch (status) {
      case "idle":
        return [
          { id: "validate", label: "Validating", status: "pending" },
          { id: "submit", label: "Submitting to Blockchain", status: "pending" },
          { id: "complete", label: "Transaction Complete", status: "pending" },
        ];
      case "validating":
        return [
          { id: "validate", label: "Validating", status: "active" },
          { id: "submit", label: "Submitting to Blockchain", status: "pending" },
          { id: "complete", label: "Transaction Complete", status: "pending" },
        ];
      case "submitting":
      case "pending":
        return [
          { id: "validate", label: "Validating", status: "completed" },
          { id: "submit", label: "Submitting to Blockchain", status: "active" },
          { id: "complete", label: "Transaction Complete", status: "pending" },
        ];
      case "success":
        return [
          { id: "validate", label: "Validating", status: "completed" },
          { id: "submit", label: "Submitting to Blockchain", status: "completed" },
          { id: "complete", label: "Transaction Complete", status: "completed" },
        ];
      case "failed":
        return [
          { id: "validate", label: "Validating", status: error ? "error" : "completed" },
          { id: "submit", label: "Submitting to Blockchain", status: error ? "error" : "pending" },
          { id: "complete", label: "Transaction Complete", status: "pending" },
        ];
      default:
        return [];
    }
  };

  const steps = getSteps();

  const getStepIcon = (stepStatus: Step["status"]) => {
    switch (stepStatus) {
      case "completed":
        return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      case "active":
        return <Loader2 className="h-5 w-5 text-primary animate-spin" />;
      case "error":
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Circle className="h-5 w-5 text-muted-foreground" />;
    }
  };

  const getStepLabelColor = (stepStatus: Step["status"]) => {
    switch (stepStatus) {
      case "completed":
        return "text-green-600 dark:text-green-400";
      case "active":
        return "text-primary font-semibold";
      case "error":
        return "text-red-600 dark:text-red-400";
      default:
        return "text-muted-foreground";
    }
  };

  if (status === "idle") {
    return null;
  }

  return (
    <div className={cn("space-y-4", className)}>
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold">Transfer Progress</h3>
        {status === "active" && (
          <span className="text-xs text-muted-foreground">Processing...</span>
        )}
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-center gap-4">
            {/* Step Icon */}
            <div className="flex-shrink-0">{getStepIcon(step.status)}</div>

            {/* Step Content */}
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <p className={cn("text-sm", getStepLabelColor(step.status))}>
                  {step.label}
                </p>
                {step.status === "active" && (
                  <span className="text-xs text-muted-foreground">
                    {step.id === "validate" && "Checking balance..."}
                    {step.id === "submit" && "Broadcasting transaction..."}
                    {step.id === "complete" && "Confirming on blockchain..."}
                  </span>
                )}
              </div>

              {/* Progress Line */}
              {index < steps.length - 1 && (
                <div className="mt-2 ml-2.5 w-0.5 h-8">
                  <div
                    className={cn(
                      "h-full transition-colors",
                      step.status === "completed"
                        ? "bg-green-500"
                        : step.status === "active"
                        ? "bg-primary"
                        : "bg-muted"
                    )}
                  />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {error && (
        <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}
    </div>
  );
}

