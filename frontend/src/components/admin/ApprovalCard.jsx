import React, { useState } from 'react';
import { ShieldAlert, Check, X, Clock, User } from 'lucide-react';

export default function ApprovalCard({ item, onDecide }) {
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleAction = async (decision) => {
    setSubmitting(true);
    await onDecide(item.approval_id, decision, notes || `Decided as ${decision} by operations`);
    setSubmitting(false);
  };

  const isPending = item.status === 'PENDING';

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm space-y-4">
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-600">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-slate-800 text-sm">{item.title}</h4>
            <div className="flex items-center space-x-2 text-xs text-slate-400 mt-0.5">
              <span>Customer: {item.customer_id}</span>
              <span>•</span>
              <span className="font-mono">{item.approval_id}</span>
            </div>
          </div>
        </div>

        <span
          className={`px-2.5 py-1 rounded-full text-xs font-bold uppercase ${
            item.status === 'APPROVED'
              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
              : item.status === 'REJECTED'
              ? 'bg-rose-50 text-rose-700 border border-rose-200'
              : 'bg-amber-50 text-amber-700 border border-amber-200 animate-pulse'
          }`}
        >
          {item.status}
        </span>
      </div>

      {item.data && (
        <div className="bg-slate-50 p-3 rounded-xl text-xs space-y-1 text-slate-600 border border-slate-100 font-mono">
          <p><span className="text-slate-400">Transaction ID:</span> {item.data.transaction_id}</p>
          <p><span className="text-slate-400">Amount:</span> ₹{item.data.amount?.toLocaleString()}</p>
          <p><span className="text-slate-400">Reason:</span> {item.data.reason}</p>
        </div>
      )}

      {isPending ? (
        <div className="space-y-3 pt-2 border-t border-slate-100">
          <input
            type="text"
            placeholder="Officer verification notes (optional)..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-800 focus:outline-none focus:border-sky-500"
          />

          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleAction('APPROVED')}
              disabled={submitting}
              className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded-xl text-xs font-semibold flex items-center justify-center space-x-1.5 shadow-sm shadow-emerald-200 transition-colors"
            >
              <Check className="w-3.5 h-3.5" />
              <span>Authorize & Approve</span>
            </button>
            <button
              onClick={() => handleAction('REJECTED')}
              disabled={submitting}
              className="flex-1 bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 py-2 rounded-xl text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors"
            >
              <X className="w-3.5 h-3.5" />
              <span>Decline</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="pt-2 border-t border-slate-100 text-xs text-slate-400 flex items-center justify-between">
          <span>Reviewed by: {item.reviewed_by || 'Officer'}</span>
          <span>{item.review_notes}</span>
        </div>
      )}
    </div>
  );
}
