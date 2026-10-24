import React from 'react';
import { ArrowDownLeft, ArrowUpRight, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function RecentTransactions({ transactions = [], onVerifyFraud }) {
  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="font-bold text-slate-800 text-sm">Recent Activity</h3>
          <p className="text-xs text-slate-400 mt-0.5">Live account feed</p>
        </div>
      </div>

      <div className="divide-y divide-slate-100">
        {transactions.slice(0, 7).map((txn, idx) => {
          const isDebit = txn.type === 'DEBIT';
          const isFlagged = txn.status === 'FLAGGED';

          return (
            <div key={idx} className="py-3 flex items-center justify-between first:pt-0 last:pb-0">
              <div className="flex items-center space-x-3">
                <div
                  className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 ${
                    isFlagged
                      ? 'bg-amber-100 text-amber-700 border border-amber-300'
                      : isDebit
                      ? 'bg-slate-100 text-slate-600'
                      : 'bg-emerald-100 text-emerald-700'
                  }`}
                >
                  {isFlagged ? (
                    <AlertTriangle className="w-4 h-4 text-amber-600" />
                  ) : isDebit ? (
                    <ArrowDownLeft className="w-4 h-4 text-rose-500" />
                  ) : (
                    <ArrowUpRight className="w-4 h-4 text-emerald-600" />
                  )}
                </div>

                <div>
                  <div className="flex items-center space-x-2">
                    <p className="text-xs font-bold text-slate-800">{txn.merchant}</p>
                    {isFlagged && (
                      <span className="text-[10px] bg-amber-100 text-amber-800 font-bold px-1.5 py-0.2 rounded border border-amber-200">
                        FLAGGED
                      </span>
                    )}
                  </div>
                  <div className="flex items-center space-x-2 text-[11px] text-slate-400 mt-0.5">
                    <span>{txn.channel}</span>
                    <span>•</span>
                    <span>{txn.category}</span>
                    <span>•</span>
                    <span className="font-mono text-[10px]">{txn.reference_number || txn.transaction_id}</span>
                  </div>
                </div>
              </div>

              <div className="text-right">
                <p
                  className={`text-xs font-bold font-mono ${
                    isFlagged
                      ? 'text-amber-700'
                      : isDebit
                      ? 'text-slate-800'
                      : 'text-emerald-600'
                  }`}
                >
                  {isDebit ? '-' : '+'}₹{txn.amount.toLocaleString()}
                </p>
                <p className="text-[10px] text-slate-400 mt-0.5">
                  {new Date(txn.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
