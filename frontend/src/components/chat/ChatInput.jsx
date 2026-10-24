import React, { useState } from 'react';
import { Send, Sparkles } from 'lucide-react';

const SUGGESTIONS = [
  "What is my current account balance?",
  "How much have I spent this month?",
  "How much money do I have available after paying all upcoming bills?",
  "Did my UPI payment to Amazon go through?",
  "When is my credit card payment due?",
  "What is my next EMI amount?",
  "What payments are due this week?",
  "I lost my debit card.",
  "I do not recognize this transaction.",
  "Am I eligible for a pre-approved loan?"
];

export default function ChatInput({ onSendMessage, disabled }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || disabled) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const handleSelectSuggestion = (text) => {
    if (disabled) return;
    onSendMessage(text);
  };

  return (
    <div className="border-t border-slate-200 bg-white p-4 space-y-3">
      {/* Quick Banking Use Case Prompts */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-1 scrollbar-none">
        <div className="flex items-center space-x-1 text-[11px] text-slate-400 flex-shrink-0 font-medium">
          <Sparkles className="w-3 h-3 text-sky-500" />
          <span>Quick queries:</span>
        </div>
        {SUGGESTIONS.map((s, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleSelectSuggestion(s)}
            disabled={disabled}
            className="text-[11px] bg-slate-50 hover:bg-sky-50 hover:text-sky-700 hover:border-sky-300 text-slate-600 px-3 py-1 rounded-full border border-slate-200 flex-shrink-0 transition-colors whitespace-nowrap"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Input Field */}
      <form onSubmit={handleSubmit} className="flex items-center space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about your accounts, bills, EMIs, or card security..."
          disabled={disabled}
          className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all"
        />

        <button
          type="submit"
          disabled={!input.trim() || disabled}
          className="bg-sky-600 hover:bg-sky-700 disabled:opacity-50 text-white p-2.5 rounded-xl shadow-md shadow-sky-200 transition-all flex items-center justify-center flex-shrink-0"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
