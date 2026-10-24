import React from 'react';
import ToolExecution from './ToolExecution';
import { 
  Bot, 
  User, 
  ShieldAlert, 
  CheckCircle, 
  Clock, 
  CreditCard, 
  Sparkles,
  TrendingDown,
  AlertTriangle
} from 'lucide-react';

export default function ChatMessage({ message, onConfirmAction }) {
  const isUser = message.sender === 'user';

  return (
    <div className={`flex items-start space-x-3 mb-4 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm ${
          isUser
            ? 'bg-sky-600 text-white'
            : 'bg-gradient-to-tr from-sky-700 to-indigo-700 text-white'
        }`}
      >
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      <div className={`max-w-2xl w-full ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`p-4 rounded-2xl text-sm leading-relaxed shadow-sm ${
            isUser
              ? 'bg-sky-600 text-white rounded-tr-none'
              : 'bg-white border border-slate-200/80 text-slate-800 rounded-tl-none'
          }`}
        >
          {/* Metadata pill for assistant response */}
          {!isUser && message.answer_type && (
            <div className="flex items-center space-x-2 mb-2 pb-2 border-b border-slate-100 text-[11px]">
              <span className={`px-2 py-0.5 rounded-full font-semibold uppercase text-[10px] ${
                message.answer_type === 'calculated' ? 'bg-indigo-50 text-indigo-700 border border-indigo-200' :
                message.answer_type === 'action_required' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                message.answer_type === 'action_completed' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                'bg-slate-100 text-slate-600'
              }`}>
                {message.answer_type}
              </span>
              <span className="font-mono text-slate-400">{message.trace_id}</span>
            </div>
          )}

          <p className="whitespace-pre-line">{message.text}</p>

          {/* Tool Execution Details */}
          {!isUser && message.tools_invoked && message.tools_invoked.length > 0 && (
            <ToolExecution 
              tools={message.tools_invoked} 
              systems={message.systems_queried}
              traceId={message.trace_id}
              latencyMs={message.latency_ms}
            />
          )}

          {/* Structured Account & Bank Statement Summary Widget */}
          {!isUser && message.structured_data?.type === 'account_summary' && (
            <div className="mt-3 p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2.5">
              <div className="flex justify-between items-center border-b border-slate-200 pb-2">
                <div>
                  <p className="text-xs font-bold text-slate-800 uppercase tracking-wide">Account & Statement Summary</p>
                  <p className="text-[10px] text-slate-400 font-mono">Account: {message.structured_data.primary_account}</p>
                </div>
                <div className="text-right">
                  <p className="text-[10px] text-slate-400">Available Balance</p>
                  <p className="font-bold text-sky-700 text-sm">₹{message.structured_data.available_balance.toLocaleString()}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-center text-xs">
                <div className="bg-emerald-50 p-2 rounded-lg border border-emerald-200">
                  <p className="text-[10px] text-emerald-700 font-medium">Recent Credits</p>
                  <p className="font-bold text-emerald-800 text-xs mt-0.5">+₹{message.structured_data.total_credits.toLocaleString()}</p>
                </div>
                <div className="bg-rose-50 p-2 rounded-lg border border-rose-200">
                  <p className="text-[10px] text-rose-700 font-medium">Recent Debits</p>
                  <p className="font-bold text-rose-800 text-xs mt-0.5">-₹{message.structured_data.total_debits.toLocaleString()}</p>
                </div>
              </div>

              {message.structured_data.recent_transactions && message.structured_data.recent_transactions.length > 0 && (
                <div className="pt-1 space-y-1.5">
                  <p className="text-[11px] font-semibold text-slate-600">Recent Statement Entries:</p>
                  <div className="divide-y divide-slate-200/60 max-h-48 overflow-y-auto">
                    {message.structured_data.recent_transactions.slice(0, 5).map((t, idx) => {
                      const isCredit = t.type === 'CREDIT';
                      return (
                        <div key={idx} className="py-1.5 flex justify-between items-center text-[11px]">
                          <div>
                            <p className="font-medium text-slate-800">{t.merchant}</p>
                            <p className="text-[10px] text-slate-400 font-mono">{t.channel} • {t.category}</p>
                          </div>
                          <span className={`font-mono font-bold ${isCredit ? 'text-emerald-600' : 'text-slate-800'}`}>
                            {isCredit ? '+' : '-'}₹{t.amount.toLocaleString()}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Structured Remaining Funds Widget */}
          {!isUser && message.structured_data?.type === 'remaining_funds_breakdown' && (
            <div className="mt-3 p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <p className="text-xs font-bold text-slate-700 uppercase tracking-wide">Deterministic Breakdown</p>
              <div className="grid grid-cols-3 gap-2 text-center text-xs pt-1">
                <div className="bg-white p-2 rounded-lg border border-slate-200">
                  <p className="text-[10px] text-slate-400">Available Balance</p>
                  <p className="font-bold text-slate-800 text-sm mt-0.5">₹{message.structured_data.available_balance.toLocaleString()}</p>
                </div>
                <div className="bg-rose-50 p-2 rounded-lg border border-rose-200">
                  <p className="text-[10px] text-rose-600">Upcoming Dues</p>
                  <p className="font-bold text-rose-700 text-sm mt-0.5">-₹{message.structured_data.total_obligations.toLocaleString()}</p>
                </div>
                <div className="bg-emerald-50 p-2 rounded-lg border border-emerald-200">
                  <p className="text-[10px] text-emerald-700">Estimated Left</p>
                  <p className="font-bold text-emerald-800 text-sm mt-0.5">₹{message.structured_data.estimated_remaining_funds.toLocaleString()}</p>
                </div>
              </div>

              {message.structured_data.obligations && (
                <div className="pt-2 text-[11px] space-y-1">
                  <p className="font-semibold text-slate-600">Upcoming Obligations:</p>
                  {message.structured_data.obligations.map((o, idx) => (
                    <div key={idx} className="flex justify-between items-center text-slate-600 border-b border-slate-200/50 pb-1">
                      <span>• {o.title} (Due: {o.due_date})</span>
                      <span className="font-semibold">₹{o.amount.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Action Required: Confirmation Box (Human-in-the-Loop Safeguard) */}
          {!isUser && message.answer_type === 'action_required' && message.structured_data && (
            <div className="mt-3 p-3.5 bg-amber-50/70 border border-amber-200 rounded-xl space-y-2.5">
              <div className="flex items-center space-x-2 text-amber-800 font-semibold text-xs">
                <ShieldAlert className="w-4 h-4 text-amber-600" />
                <span>Security Confirmation Required</span>
              </div>
              <p className="text-xs text-amber-900">{message.structured_data.prompt || 'Confirm to proceed with this high-risk banking action.'}</p>
              
              <div className="flex items-center space-x-2 pt-1">
                <button
                  onClick={() => onConfirmAction(message.structured_data.action, message.structured_data, true)}
                  className="px-3.5 py-1.5 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold shadow-sm transition-colors"
                >
                  Confirm & Execute
                </button>
                <button
                  onClick={() => onConfirmAction(message.structured_data.action, message.structured_data, false)}
                  className="px-3.5 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-lg text-xs font-semibold transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>

        <p className={`text-[10px] text-slate-400 mt-1 px-1 ${isUser ? 'text-right' : ''}`}>
          {message.timestamp}
        </p>
      </div>
    </div>
  );
}
