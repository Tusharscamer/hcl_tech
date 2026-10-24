import React from 'react';
import { Wallet, ArrowUpRight, ShieldCheck, Sparkles } from 'lucide-react';

export default function BalanceCard({ balanceData, remainingFundsData }) {
  const totalAvail = balanceData?.total_available_balance ?? 170000;
  const ledger = balanceData?.total_ledger_balance ?? 173500;
  const remaining = remainingFundsData?.estimated_remaining_funds ?? 135352;
  const obligations = remainingFundsData?.total_obligations ?? 34648;

  return (
    <div className="bg-gradient-to-br from-slate-900 via-sky-950 to-indigo-950 rounded-2xl p-6 text-white shadow-xl relative overflow-hidden">
      <div className="absolute right-0 top-0 translate-x-8 -translate-y-8 w-56 h-56 rounded-full bg-sky-500/10 blur-3xl pointer-events-none" />

      <div className="flex justify-between items-start mb-6">
        <div>
          <span className="text-[11px] font-semibold tracking-wider uppercase text-sky-400">Total Net Liquidity</span>
          <h2 className="text-3xl font-extrabold mt-1 tracking-tight">₹{totalAvail.toLocaleString()}</h2>
          <p className="text-xs text-slate-400 mt-0.5">Ledger balance: ₹{ledger.toLocaleString()}</p>
        </div>
        <div className="p-3 bg-white/10 backdrop-blur-md rounded-xl border border-white/10">
          <Wallet className="w-6 h-6 text-sky-300" />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/10">
        <div className="bg-white/5 backdrop-blur-sm p-3.5 rounded-xl border border-white/5">
          <div className="flex items-center space-x-1.5 text-[11px] text-amber-300 font-semibold mb-1">
            <span>Upcoming Obligations</span>
          </div>
          <p className="text-lg font-bold text-amber-200">-₹{obligations.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 mt-0.5">EMIs, Card & Utilities</p>
        </div>

        <div className="bg-white/5 backdrop-blur-sm p-3.5 rounded-xl border border-white/5">
          <div className="flex items-center space-x-1.5 text-[11px] text-emerald-300 font-semibold mb-1">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            <span>Estimated Remaining</span>
          </div>
          <p className="text-lg font-bold text-emerald-300">₹{remaining.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 mt-0.5">Safe to spend or save</p>
        </div>
      </div>
    </div>
  );
}
