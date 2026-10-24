import React from 'react';
import { Activity, Clock, CheckCircle2, AlertCircle } from 'lucide-react';

export default function AuditLogs({ logs = [] }) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-5 border-b border-slate-200 flex justify-between items-center bg-slate-50/50">
        <div>
          <h3 className="font-bold text-slate-800 text-sm">Observability & Audit Trail</h3>
          <p className="text-xs text-slate-400 mt-0.5">Immutable record of queries, tools invoked, and latencies</p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-semibold text-slate-600 bg-white border border-slate-200 px-3 py-1.5 rounded-lg shadow-sm">
          <Activity className="w-3.5 h-3.5 text-sky-600" />
          <span>{logs.length} Logged Traces</span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-500 uppercase font-semibold text-[10px] tracking-wider border-b border-slate-200">
            <tr>
              <th className="py-3 px-4">Trace ID</th>
              <th className="py-3 px-4">Customer</th>
              <th className="py-3 px-4">User Query</th>
              <th className="py-3 px-4">Intent</th>
              <th className="py-3 px-4">Deterministic Tools</th>
              <th className="py-3 px-4">Latency</th>
              <th className="py-3 px-4">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
            {logs.map((log, idx) => (
              <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                <td className="py-3 px-4 font-bold text-sky-700 whitespace-nowrap">
                  {log.trace_id}
                </td>
                <td className="py-3 px-4 text-slate-600 whitespace-nowrap">
                  {log.customer_id}
                </td>
                <td className="py-3 px-4 text-slate-800 font-sans max-w-xs truncate" title={log.user_query}>
                  {log.user_query}
                </td>
                <td className="py-3 px-4">
                  <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-sans text-[10px] font-bold">
                    {log.intent}
                  </span>
                </td>
                <td className="py-3 px-4 text-slate-600">
                  <div className="flex flex-wrap gap-1">
                    {log.tools_invoked?.map((t, i) => (
                      <span key={i} className="bg-sky-50 text-sky-700 border border-sky-200 px-1.5 py-0.2 rounded text-[10px]">
                        {t}()
                      </span>
                    ))}
                  </div>
                </td>
                <td className="py-3 px-4 text-slate-600 whitespace-nowrap">
                  {log.latency_ms?.toFixed(1)} ms
                </td>
                <td className="py-3 px-4 whitespace-nowrap">
                  <span className="inline-flex items-center space-x-1 text-emerald-600 font-bold">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>{log.status}</span>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
