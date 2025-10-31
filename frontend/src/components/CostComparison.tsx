/**
 * Cost Comparison Component
 * Shows traditional fees vs Rowell fees side-by-side
 */

import { AlertCircle, TrendingDown } from "lucide-react";
import { cn } from "@/lib/utils";

interface CostComparisonProps {
  amount: number;
  traditionalFeePercent?: number; // e.g., 8 for 8%
  rowellFeePercent?: number; // e.g., 0.1 for 0.1%
  traditionalMinimumFee?: number;
  rowellMinimumFee?: number;
  className?: string;
}

export function CostComparison({
  amount,
  traditionalFeePercent = 8,
  rowellFeePercent = 0.1,
  traditionalMinimumFee = 5,
  rowellMinimumFee = 0.01,
  className,
}: CostComparisonProps) {
  // Calculate fees
  const traditionalFee = Math.max(
    (amount * traditionalFeePercent) / 100,
    traditionalMinimumFee
  );
  const rowellFee = Math.max(
    (amount * rowellFeePercent) / 100,
    rowellMinimumFee
  );

  const savings = traditionalFee - rowellFee;
  const savingsPercent = ((savings / traditionalFee) * 100).toFixed(1);

  if (amount <= 0) {
    return null;
  }

  return (
    <div className={cn("space-y-3", className)}>
      <div className="flex items-center gap-2">
        <TrendingDown className="h-4 w-4 text-green-500" />
        <h4 className="text-sm font-semibold">Cost Comparison</h4>
      </div>

      <div className="grid grid-cols-2 gap-4 p-4 bg-muted/50 rounded-lg border">
        {/* Traditional */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-3 w-3 text-orange-500" />
            <span className="text-xs font-medium text-muted-foreground">
              Traditional
            </span>
          </div>
          <div>
            <p className="text-2xl font-bold text-orange-600 dark:text-orange-400">
              ${traditionalFee.toFixed(2)}
            </p>
            <p className="text-xs text-muted-foreground">
              {traditionalFeePercent}% fee
            </p>
          </div>
          <p className="text-xs text-muted-foreground">
            Receives: ${(amount - traditionalFee).toFixed(2)}
          </p>
        </div>

        {/* Rowell */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <TrendingDown className="h-3 w-3 text-green-500" />
            <span className="text-xs font-medium text-primary">Rowell</span>
          </div>
          <div>
            <p className="text-2xl font-bold text-green-600 dark:text-green-400">
              ${rowellFee.toFixed(2)}
            </p>
            <p className="text-xs text-muted-foreground">
              {rowellFeePercent}% fee
            </p>
          </div>
          <p className="text-xs text-muted-foreground">
            Receives: ${(amount - rowellFee).toFixed(2)}
          </p>
        </div>
      </div>

      {/* Savings */}
      <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-green-700 dark:text-green-300">
            You Save
          </span>
          <span className="text-lg font-bold text-green-600 dark:text-green-400">
            ${savings.toFixed(2)} ({savingsPercent}%)
          </span>
        </div>
      </div>
    </div>
  );
}

