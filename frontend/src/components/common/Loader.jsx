import React from 'react';
import { Loader2 } from 'lucide-react';

export default function Loader({ text = 'Loading banking data...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 space-y-3">
      <Loader2 className="w-8 h-8 text-sky-600 animate-spin" />
      <p className="text-xs font-medium text-slate-500">{text}</p>
    </div>
  );
}
