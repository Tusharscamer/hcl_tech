import React from 'react';
import { useAuth } from '../../store/authStore';
import { 
  LayoutDashboard, 
  MessageSquareCode, 
  ArrowLeftRight, 
  ShieldAlert, 
  FileText
} from 'lucide-react';

export default function Sidebar({ activeTab, onTabChange }) {
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin';

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'chat', label: 'AI Assistant', icon: MessageSquareCode, badge: 'Live' },
    { id: 'transactions', label: 'Transactions & Dues', icon: ArrowLeftRight },
  ];

  if (isAdmin) {
    navItems.push({
      id: 'admin',
      label: 'Admin & Oversight',
      icon: ShieldAlert,
      badge: 'Staff'
    });
  }

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col min-h-screen border-r border-slate-800">
      <div className="p-5 border-b border-slate-800/80">
        <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Navigation</p>
      </div>

      <nav className="p-3 space-y-1.5 flex-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? 'bg-sky-600 text-white shadow-lg shadow-sky-600/30'
                  : 'hover:bg-slate-800/60 hover:text-white text-slate-400'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    isActive ? 'bg-white/20 text-white' : 'bg-slate-800 text-sky-400'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Mode / User Info Banner */}
      <div className="p-4 m-3 bg-slate-800/60 rounded-xl border border-slate-700/50">
        <p className="text-xs font-semibold text-slate-200">Active Account</p>
        <p className="text-[11px] text-slate-400 mt-0.5">{user?.name || 'Customer'}</p>
        <div className="mt-2.5 pt-2 border-t border-slate-700/50 flex items-center justify-between text-[11px]">
          <span className="text-slate-400">ID: {user?.customer_id}</span>
          <span className="text-emerald-400 font-medium">KYC Verified</span>
        </div>
      </div>
    </aside>
  );
}
