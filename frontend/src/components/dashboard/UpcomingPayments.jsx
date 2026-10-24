import React from 'react';
import { Calendar, Bell, CheckCircle2, Clock } from 'lucide-react';

export default function UpcomingPayments({ bills = [] }) {
  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="font-bold text-slate-800 text-sm">Smart Bill Reminders</h3>
          <p className="text-xs text-slate-400 mt-0.5">Upcoming EMIs & Subscriptions</p>
        </div>
        <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
          <Bell className="w-4 h-4" />
        </div>
      </div>

      <div className="divide-y divide-slate-100">
        {bills.map((bill, idx) => (
          <div key={idx} className="py-3 flex items-center justify-between first:pt-0 last:pb-0">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-500">
                <Calendar className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-800">{bill.biller_name}</p>
                <div className="flex items-center space-x-2 text-[11px] text-slate-400">
                  <span>Due: {bill.due_date}</span>
                  {bill.auto_pay && (
                    <span className="text-emerald-600 font-semibold">• Auto-Pay ON</span>
                  )}
                </div>
              </div>
            </div>

            <div className="text-right">
              <p className="text-xs font-bold text-slate-800 font-mono">₹{bill.amount.toLocaleString()}</p>
              <span className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-medium">
                {bill.category}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
