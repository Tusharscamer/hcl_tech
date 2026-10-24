import React from 'react';
import { Cpu, CheckCircle2, Sparkles, Server } from 'lucide-react';

export default function ToolExecution({ tools = [], systems = [], traceId, latencyMs }) {
  if (!tools || tools.length === 0) return null;

  // Find if AI model was queried
  const aiModel = systems.find(s => s.toLowerCase().includes('gemini') || s.toLowerCase().includes('ai'));
  const backendSystems = systems.filter(s => s !== aiModel);

  return (
    <div className="my-2.5 p-3.5 bg-slate-900 text-slate-300 rounded-xl text-xs border border-slate-800 shadow-inner space-y-2">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center space-x-2">
          <Cpu className="w-3.5 h-3.5 text-sky-400" />
          <span className="font-semibold text-slate-200">AI Tool Orchestrator</span>
        </div>
        <div className="flex items-center space-x-2 text-[10px] text-slate-400">
          <span className="bg-slate-800 px-1.5 py-0.5 rounded font-mono text-sky-300">{traceId}</span>
          {latencyMs && <span>{latencyMs.toFixed(0)}ms</span>}
        </div>
      </div>

      <div className="space-y-1.5">
        <div className="flex items-center space-x-1.5 flex-wrap gap-y-1">
          <span className="text-[11px] text-slate-400">Deterministic Tools:</span>
          {tools.map((t, idx) => (
            <span key={idx} className="bg-sky-950 text-sky-300 border border-sky-800/80 px-2 py-0.5 rounded text-[11px] font-mono flex items-center space-x-1">
              <CheckCircle2 className="w-2.5 h-2.5 text-emerald-400" />
              <span>{t}()</span>
            </span>
          ))}
        </div>

        <div className="flex flex-wrap items-center justify-between pt-1 border-t border-slate-800/80 gap-1 text-[11px]">
          {backendSystems.length > 0 && (
            <div className="flex items-center space-x-1.5 text-slate-400">
              <Server className="w-3 h-3 text-slate-500" />
              <span>{backendSystems.join(' • ')}</span>
            </div>
          )}

          {aiModel && (
            <div className="flex items-center space-x-1 bg-indigo-950 text-indigo-300 border border-indigo-700/60 px-2 py-0.5 rounded-full font-medium text-[10px]">
              <Sparkles className="w-2.5 h-2.5 text-indigo-400" />
              <span>{aiModel}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
