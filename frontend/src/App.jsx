import React, { useState } from 'react';
import { useAuth } from './store/authStore';
import Navbar from './components/common/Navbar';
import Sidebar from './components/common/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Transactions from './pages/Transactions';
import Admin from './pages/Admin';

export default function App() {
  const { isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
        <main className="flex-1 overflow-y-auto min-h-[calc(100vh-4rem)]">
          {activeTab === 'dashboard' && <Dashboard onNavigateToChat={() => setActiveTab('chat')} />}
          {activeTab === 'chat' && <Chat />}
          {activeTab === 'transactions' && <Transactions />}
          {activeTab === 'admin' && <Admin />}
        </main>
      </div>
    </div>
  );
}
