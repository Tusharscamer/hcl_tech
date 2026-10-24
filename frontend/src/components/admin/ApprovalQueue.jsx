import React from 'react';
import ApprovalCard from './ApprovalCard';
import { ShieldCheck, Inbox } from 'lucide-react';

export default function ApprovalQueue({ approvals = [], onDecide }) {
  const pending = approvals.filter(a => a.status === 'PENDING');
  const completed = approvals.filter(a => a.status !== 'PENDING');

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <h3 className="font-bold text-slate-800 text-base">Pending HITL Approval Queue</h3>
            <span className="bg-amber-100 text-amber-800 text-xs px-2.5 py-0.5 rounded-full font-bold">
              {pending.length} Action{pending.length !== 1 ? 's' : ''}
            </span>
          </div>
        </div>

        {pending.length === 0 ? (
          <div className="bg-white rounded-2xl p-8 border border-slate-200 text-center space-y-2">
            <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <p className="text-sm font-bold text-slate-800">All Queue Items Reviewed</p>
            <p className="text-xs text-slate-400">No sensitive actions currently awaiting bank officer approval.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {pending.map((item) => (
              <ApprovalCard key={item.approval_id} item={item} onDecide={onDecide} />
            ))}
          </div>
        )}
      </div>

      {completed.length > 0 && (
        <div className="pt-4">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Recently Reviewed</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 opacity-75">
            {completed.slice(0, 4).map((item) => (
              <ApprovalCard key={item.approval_id} item={item} onDecide={onDecide} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
