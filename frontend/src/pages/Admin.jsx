import React, { useState, useEffect } from 'react';
import { bankingApi } from '../services/bankingApi';
import ApprovalQueue from '../components/admin/ApprovalQueue';
import AuditLogs from '../components/admin/AuditLogs';
import Loader from '../components/common/Loader';
import ErrorMessage from '../components/common/ErrorMessage';
import { ShieldCheck, Activity, Users, CheckCircle, RefreshCw } from 'lucide-react';

export default function Admin() {
  const [approvals, setApprovals] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeAdminTab, setActiveAdminTab] = useState('approvals');

  const loadAdminData = async () => {
    try {
      setLoading(true);
      const [apprRes, logRes] = await Promise.all([
        bankingApi.getApprovals(),
        bankingApi.getAuditLogs()
      ]);
      if (apprRes.success) setApprovals(apprRes.data);
      if (logRes.success) setLogs(logRes.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAdminData();
  }, []);

  const handleDecide = async (approvalId, decision, notes) => {
    try {
      const res = await bankingApi.decideApproval(approvalId, decision, notes);
      if (res.success) {
        setApprovals(prev => prev.map(a => {
          if (a.approval_id === approvalId) {
            return { ...a, status: decision, review_notes: notes };
          }
          return a;
        }));
      }
    } catch (err) {
      alert('Failed to process approval: ' + err.message);
    }
  };

  if (loading) return <Loader text="Loading Bank Operations & Audit Console..." />;
  if (error) return <ErrorMessage message={error} />;

  const pendingCount = approvals.filter(a => a.status === 'PENDING').length;

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800">Bank Operations & Risk Console</h2>
          <p className="text-xs text-slate-400 mt-0.5">Human-in-the-Loop oversight & compliance audibility</p>
        </div>

        <button
          onClick={loadAdminData}
          className="flex items-center space-x-1.5 text-xs font-semibold text-slate-600 bg-white border border-slate-200 px-3 py-2 rounded-xl shadow-sm hover:bg-slate-50 transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Queue</span>
        </button>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase">Pending Approvals</p>
            <p className="text-2xl font-black text-slate-800 mt-0.5">{pendingCount}</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center font-bold">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase">Total Audit Traces</p>
            <p className="text-2xl font-black text-slate-800 mt-0.5">{logs.length}</p>
          </div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
            <CheckCircle className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase">Avg Response Time</p>
            <p className="text-2xl font-black text-slate-800 mt-0.5">
              {(logs.reduce((acc, l) => acc + (l.latency_ms || 1.2), 0) / Math.max(1, logs.length)).toFixed(1)} ms
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200 space-x-4 text-xs font-bold">
        <button
          onClick={() => setActiveAdminTab('approvals')}
          className={`pb-3 px-1 border-b-2 transition-all flex items-center space-x-2 ${
            activeAdminTab === 'approvals'
              ? 'border-sky-600 text-sky-600'
              : 'border-transparent text-slate-400 hover:text-slate-700'
          }`}
        >
          <span>Human-in-the-Loop Approvals</span>
          {pendingCount > 0 && (
            <span className="bg-amber-100 text-amber-800 px-1.5 py-0.2 rounded-full text-[10px]">
              {pendingCount}
            </span>
          )}
        </button>

        <button
          onClick={() => setActiveAdminTab('audit')}
          className={`pb-3 px-1 border-b-2 transition-all ${
            activeAdminTab === 'audit'
              ? 'border-sky-600 text-sky-600'
              : 'border-transparent text-slate-400 hover:text-slate-700'
          }`}
        >
          Observability Audit Logs
        </button>
      </div>

      {/* Tab Content */}
      {activeAdminTab === 'approvals' ? (
        <ApprovalQueue approvals={approvals} onDecide={handleDecide} />
      ) : (
        <AuditLogs logs={logs} />
      )}
    </div>
  );
}
