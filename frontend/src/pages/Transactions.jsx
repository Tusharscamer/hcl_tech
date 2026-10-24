import React, { useState, useEffect } from 'react';
import { bankingApi } from '../services/bankingApi';
import Loader from '../components/common/Loader';
import ErrorMessage from '../components/common/ErrorMessage';
import { 
  ArrowDownLeft, 
  ArrowUpRight, 
  AlertTriangle, 
  ShieldCheck, 
  Search,
  Filter
} from 'lucide-react';

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [disputeStatus, setDisputeStatus] = useState({});

  useEffect(() => {
    async function loadTxns() {
      try {
        setLoading(true);
        const res = await bankingApi.getTransactions(50);
        if (res.success) {
          setTransactions(res.data);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadTxns();
  }, []);

  const handleRaiseDispute = async (txnId) => {
    try {
      const res = await bankingApi.raiseDispute(txnId, 'Customer flagged charge via Transaction Portal');
      if (res.success) {
        setDisputeStatus(prev => ({
          ...prev,
          [txnId]: res.data?.dispute_id || 'DISPUTED'
        }));
      }
    } catch (err) {
      alert('Failed to submit dispute: ' + err.message);
    }
  };

  const filtered = transactions.filter(t => {
    if (filter === 'DEBIT' && t.type !== 'DEBIT') return false;
    if (filter === 'CREDIT' && t.type !== 'CREDIT') return false;
    if (filter === 'FLAGGED' && t.status !== 'FLAGGED') return false;
    if (search) {
      const q = search.toLowerCase();
      return (
        t.merchant.toLowerCase().includes(q) ||
        t.category.toLowerCase().includes(q) ||
        (t.reference_number || '').toLowerCase().includes(q)
      );
    }
    return true;
  });

  if (loading) return <Loader text="Loading ledger and transaction histories..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Transaction History & Statements</h2>
        <p className="text-xs text-slate-400 mt-0.5">Audited core banking records</p>
      </div>

      {/* Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-3 justify-between items-center bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by merchant, category, ref..."
            className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div className="flex items-center space-x-1.5 w-full sm:w-auto">
          {['ALL', 'DEBIT', 'CREDIT', 'FLAGGED'].map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                filter === tab
                  ? 'bg-sky-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Transactions Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-500 uppercase font-semibold text-[10px] tracking-wider border-b border-slate-200">
            <tr>
              <th className="py-3 px-4">Merchant & Details</th>
              <th className="py-3 px-4">Channel</th>
              <th className="py-3 px-4">Category</th>
              <th className="py-3 px-4">Date</th>
              <th className="py-3 px-4 text-right">Amount</th>
              <th className="py-3 px-4 text-center">Safety Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {filtered.map((txn, idx) => {
              const isDebit = txn.type === 'DEBIT';
              const isFlagged = txn.status === 'FLAGGED';
              const hasDisputed = disputeStatus[txn.transaction_id];

              return (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-3 px-4">
                    <div className="flex items-center space-x-2.5">
                      <div
                        className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                          isFlagged
                            ? 'bg-amber-100 text-amber-700'
                            : isDebit
                            ? 'bg-slate-100 text-slate-600'
                            : 'bg-emerald-100 text-emerald-700'
                        }`}
                      >
                        {isDebit ? <ArrowDownLeft className="w-4 h-4 text-rose-500" /> : <ArrowUpRight className="w-4 h-4 text-emerald-600" />}
                      </div>
                      <div>
                        <p className="font-bold text-slate-800">{txn.merchant}</p>
                        <p className="text-[10px] text-slate-400 font-mono">{txn.reference_number || txn.transaction_id}</p>
                      </div>
                    </div>
                  </td>

                  <td className="py-3 px-4 font-mono text-[11px] text-slate-600">
                    {txn.channel}
                  </td>

                  <td className="py-3 px-4">
                    <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[11px]">
                      {txn.category}
                    </span>
                  </td>

                  <td className="py-3 px-4 text-slate-500 text-[11px]">
                    {new Date(txn.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}
                  </td>

                  <td className="py-3 px-4 text-right font-mono font-bold text-xs">
                    <span className={isDebit ? 'text-slate-800' : 'text-emerald-600'}>
                      {isDebit ? '-' : '+'}₹{txn.amount.toLocaleString()}
                    </span>
                  </td>

                  <td className="py-3 px-4 text-center">
                    {hasDisputed ? (
                      <span className="text-[11px] text-emerald-600 font-bold bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">
                        Dispute Ticket #{hasDisputed}
                      </span>
                    ) : isFlagged ? (
                      <button
                        onClick={() => handleRaiseDispute(txn.transaction_id)}
                        className="bg-amber-600 hover:bg-amber-700 text-white px-2.5 py-1 rounded-lg text-[11px] font-semibold flex items-center space-x-1 mx-auto shadow-sm"
                      >
                        <AlertTriangle className="w-3 h-3" />
                        <span>Dispute Charge</span>
                      </button>
                    ) : (
                      <span className="text-[11px] text-slate-400 font-medium">Verified</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
