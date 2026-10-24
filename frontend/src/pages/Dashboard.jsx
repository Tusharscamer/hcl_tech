import React, { useState, useEffect } from 'react';
import { bankingApi } from '../services/bankingApi';
import BalanceCard from '../components/dashboard/BalanceCard';
import ExpenseChart from '../components/dashboard/ExpenseChart';
import UpcomingPayments from '../components/dashboard/UpcomingPayments';
import RecentTransactions from '../components/dashboard/RecentTransactions';
import Loader from '../components/common/Loader';
import ErrorMessage from '../components/common/ErrorMessage';
import { MessageSquare, ShieldAlert, Sparkles, CreditCard } from 'lucide-react';

export default function Dashboard({ onNavigateToChat }) {
  const [balance, setBalance] = useState(null);
  const [remainingFunds, setRemainingFunds] = useState(null);
  const [expenses, setExpenses] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [bills, setBills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        setLoading(true);
        const [balRes, remRes, expRes, txnRes, billRes] = await Promise.all([
          bankingApi.getBalance(),
          bankingApi.getRemainingFunds(),
          bankingApi.getExpenseAnalytics(),
          bankingApi.getTransactions(10),
          bankingApi.getBills()
        ]);

        if (balRes.success) setBalance(balRes.data);
        if (remRes.success) setRemainingFunds(remRes.data);
        if (expRes.success) setExpenses(expRes.data);
        if (txnRes.success) setTransactions(txnRes.data);
        if (billRes.success) setBills(billRes.data);
      } catch (err) {
        setError(err.message || 'Failed to load banking dashboard data.');
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  if (loading) return <Loader text="Retrieving live account servicing data..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Top Banner with Quick Assistant Action */}
      <div className="bg-gradient-to-r from-sky-600 to-indigo-700 rounded-2xl p-6 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-lg shadow-sky-600/15">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-sky-200" />
            <span className="text-xs font-semibold uppercase tracking-wider text-sky-200">AI Daily Banking Concierge</span>
          </div>
          <h2 className="text-xl font-bold">Have questions about your bills, spending, or EMI?</h2>
          <p className="text-xs text-sky-100">Ask in plain natural language. Zero hallucinations with deterministic calculations.</p>
        </div>

        <button
          onClick={onNavigateToChat}
          className="bg-white hover:bg-slate-50 text-sky-700 px-5 py-2.5 rounded-xl font-bold text-xs shadow-md transition-all flex items-center space-x-2 flex-shrink-0"
        >
          <MessageSquare className="w-4 h-4" />
          <span>Launch AI Assistant</span>
        </button>
      </div>

      {/* Primary Financial Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <BalanceCard balanceData={balance} remainingFundsData={remainingFunds} />
        </div>
        <div>
          <UpcomingPayments bills={bills} />
        </div>
      </div>

      {/* Analytics & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ExpenseChart expenseData={expenses} />
        <RecentTransactions transactions={transactions} />
      </div>
    </div>
  );
}
