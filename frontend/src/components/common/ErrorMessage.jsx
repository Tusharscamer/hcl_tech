import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function ErrorMessage({ message = 'An error occurred while fetching information.' }) {
  return (
    <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 flex items-start space-x-3 text-rose-700 text-xs">
      <AlertCircle className="w-4 h-4 text-rose-500 mt-0.5 flex-shrink-0" />
      <div className="flex-1">
        <p className="font-semibold text-rose-800">Banking Notice</p>
        <p className="mt-0.5 text-rose-600">{message}</p>
      </div>
    </div>
  );
}
