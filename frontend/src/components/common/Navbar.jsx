import React, { useState, useEffect } from 'react';
import { useAuth } from '../../store/authStore';
import { ShieldCheck, LogOut, User, Landmark, Database, AlertCircle } from 'lucide-react';
import { bankingApi } from '../../services/bankingApi';

export default function Navbar() {
  const { user, logout } = useAuth();
  const [dbStatus, setDbStatus] = useState(null);

  useEffect(() => {
    let mounted = true;
    bankingApi.getDbStatus()
      .then(res => {
        if (mounted && res?.data) {
          setDbStatus(res.data);
        }
      })
      .catch(() => {});
    return () => { mounted = false; };
  }, []);

  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-30 shadow-sm">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-100">
          <Landmark className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-slate-800 leading-tight">Apex Bank</h1>
          <p className="text-xs text-slate-400 font-medium tracking-wide">AI DAILY BANKING ASSISTANT</p>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {dbStatus?.is_connected ? (
          <div 
            title={`Connected to MongoDB Atlas: ${dbStatus.database || 'apex_daily_banking'}`}
            className="hidden sm:flex items-center space-x-2 bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-semibold border border-emerald-200 shadow-sm"
          >
            <Database className="w-3.5 h-3.5 text-emerald-600" />
            <span>MongoDB Atlas Connected</span>
          </div>
        ) : dbStatus?.status === 'placeholder_password' ? (
          <div 
            title="Atlas URI detected with <db_password> placeholder. Replace <db_password> with your Atlas password in backend/.env to connect directly to the cloud cluster."
            className="hidden sm:flex items-center space-x-2 bg-amber-50 text-amber-800 px-3 py-1 rounded-full text-xs font-semibold border border-amber-300 shadow-sm"
          >
            <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
            <span>Atlas: Replace &lt;db_password&gt; in .env</span>
          </div>
        ) : (
          <div className="hidden sm:flex items-center space-x-2 bg-slate-50 text-slate-700 px-3 py-1 rounded-full text-xs font-semibold border border-slate-200">
            <ShieldCheck className="w-3.5 h-3.5 text-slate-500" />
            <span>Core Banking Active</span>
          </div>
        )}

        {user && (
          <div className="flex items-center space-x-3 pl-4 border-l border-slate-200">
            <div className="flex items-center space-x-2 text-right">
              <div className="w-8 h-8 rounded-full bg-slate-100 text-sky-700 flex items-center justify-center font-bold text-xs border border-slate-200">
                {user.name.charAt(0)}
              </div>
              <div className="hidden md:block">
                <p className="text-xs font-semibold text-slate-800">{user.name}</p>
                <p className="text-[10px] text-slate-400 font-medium capitalize">{user.role} • {user.customer_id}</p>
              </div>
            </div>

            <button
              onClick={logout}
              title="Logout"
              className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
