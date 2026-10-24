import React, { useState } from 'react';
import { useAuth } from '../store/authStore';
import { Landmark, ShieldCheck, Key, UserCheck } from 'lucide-react';

export default function Login() {
  const { login } = useAuth();
  const [username, setUsername] = useState('C1001');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const res = await login(username, password);
    setLoading(false);
    if (!res.success) {
      setError(res.message);
    }
  };

  const handleQuickLogin = (userType) => {
    if (userType === 'customer') {
      setUsername('C1001');
      setPassword('password123');
    } else {
      setUsername('A9001');
      setPassword('admin123');
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl p-8 shadow-2xl space-y-6">
        <div className="text-center space-y-2">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white mx-auto shadow-lg shadow-sky-600/30">
            <Landmark className="w-7 h-7" />
          </div>
          <h2 className="text-2xl font-black text-slate-800 tracking-tight">Apex Digital Bank</h2>
          <p className="text-xs text-slate-400 font-medium">AI-Powered Daily Banking Assistant</p>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-xl text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Customer / Officer ID</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. C1001 or A9001"
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all font-mono"
              required
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-all font-mono"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 rounded-xl shadow-lg shadow-sky-600/25 transition-all text-sm disabled:opacity-50"
          >
            {loading ? 'Authenticating...' : 'Sign In to Banking Portal'}
          </button>
        </form>

        {/* Demo Fast Login Pills */}
        <div className="pt-4 border-t border-slate-100">
          <p className="text-[11px] text-slate-400 text-center uppercase tracking-wider font-semibold mb-2.5">
            One-Click Demo Profiles
          </p>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleQuickLogin('customer')}
              className="p-2.5 rounded-xl border border-slate-200 hover:border-sky-500 hover:bg-sky-50 text-left transition-all"
            >
              <p className="text-xs font-bold text-slate-800">Aarav Sharma</p>
              <p className="text-[10px] text-slate-400 font-mono">C1001 (Customer)</p>
            </button>

            <button
              type="button"
              onClick={() => handleQuickLogin('admin')}
              className="p-2.5 rounded-xl border border-slate-200 hover:border-indigo-500 hover:bg-indigo-50 text-left transition-all"
            >
              <p className="text-xs font-bold text-slate-800">Vikram Malhotra</p>
              <p className="text-[10px] text-slate-400 font-mono">A9001 (Bank Officer)</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
