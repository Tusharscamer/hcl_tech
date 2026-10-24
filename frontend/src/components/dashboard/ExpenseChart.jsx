import React from 'react';
import { PieChart, TrendingUp, Utensils, Car, ShoppingBag, Receipt } from 'lucide-react';

const CATEGORY_COLORS = {
  Food: 'bg-amber-500',
  Transport: 'bg-blue-500',
  Shopping: 'bg-indigo-500',
  Bills: 'bg-rose-500',
  Electronics: 'bg-purple-500',
  General: 'bg-slate-500'
};

const CATEGORY_ICONS = {
  Food: Utensils,
  Transport: Car,
  Shopping: ShoppingBag,
  Bills: Receipt
};

export default function ExpenseChart({ expenseData }) {
  const breakdown = expenseData?.category_breakdown || [
    { category: 'Food', amount: 8500, percentage: 30.1 },
    { category: 'Transport', amount: 3200, percentage: 11.3 },
    { category: 'Shopping', amount: 12000, percentage: 42.6 },
    { category: 'Bills', amount: 4500, percentage: 16.0 }
  ];

  const totalSpent = expenseData?.total_spent || 28200;

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
      <div className="flex justify-between items-center mb-5">
        <div>
          <h3 className="font-bold text-slate-800 text-sm">Monthly Expense Analytics</h3>
          <p className="text-xs text-slate-400 mt-0.5">Categorized debit spending</p>
        </div>
        <div className="text-right">
          <span className="text-[10px] text-slate-400 uppercase font-semibold">Total Debited</span>
          <p className="text-base font-bold text-slate-800">₹{totalSpent.toLocaleString()}</p>
        </div>
      </div>

      {/* Progress Bars */}
      <div className="space-y-3.5">
        {breakdown.map((item, idx) => {
          const colorClass = CATEGORY_COLORS[item.category] || 'bg-sky-500';
          const Icon = CATEGORY_ICONS[item.category] || Receipt;
          return (
            <div key={idx} className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <div className="flex items-center space-x-2">
                  <div className={`w-2.5 h-2.5 rounded-full ${colorClass}`} />
                  <span className="font-semibold text-slate-700">{item.category}</span>
                </div>
                <div className="space-x-2 font-mono">
                  <span className="font-bold text-slate-800">₹{item.amount.toLocaleString()}</span>
                  <span className="text-slate-400 text-[11px]">({item.percentage}%)</span>
                </div>
              </div>

              <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${colorClass}`}
                  style={{ width: `${Math.min(100, item.percentage)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Insight Callout */}
      {expenseData?.insights && expenseData.insights.length > 0 && (
        <div className="mt-5 p-3 bg-sky-50 border border-sky-100 rounded-xl text-xs text-sky-800 flex items-start space-x-2">
          <TrendingUp className="w-4 h-4 text-sky-600 mt-0.5 flex-shrink-0" />
          <p>{expenseData.insights[0]}</p>
        </div>
      )}
    </div>
  );
}
