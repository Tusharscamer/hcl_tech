import { request } from './api';

export const bankingApi = {
  getBalance: async () => {
    return await request('/banking/balance');
  },

  getRemainingFunds: async () => {
    return await request('/banking/remaining-funds');
  },

  getTransactions: async (limit = 20) => {
    return await request(`/transactions?limit=${limit}`);
  },

  getExpenseAnalytics: async () => {
    return await request('/transactions/expenses');
  },

  getCards: async () => {
    return await request('/cards');
  },

  blockCard: async (cardType, cardId, reason) => {
    return await request('/cards/block', {
      method: 'POST',
      body: JSON.stringify({ card_type: cardType, card_id: cardId, reason })
    });
  },

  getLoans: async () => {
    return await request('/loans');
  },

  getLoanEligibility: async () => {
    return await request('/loans/eligibility');
  },

  getBills: async () => {
    return await request('/payments/bills');
  },

  verifyFraud: async (transactionId) => {
    return await request('/fraud/verify', {
      method: 'POST',
      body: JSON.stringify({ transaction_id: transactionId })
    });
  },

  raiseDispute: async (transactionId, reason) => {
    return await request('/fraud/dispute', {
      method: 'POST',
      body: JSON.stringify({ transaction_id: transactionId, reason })
    });
  },

  getApprovals: async () => {
    return await request('/admin/approvals');
  },

  decideApproval: async (approvalId, decision, notes) => {
    return await request(`/admin/approvals/${approvalId}/decision`, {
      method: 'POST',
      body: JSON.stringify({ decision, notes })
    });
  },

  getAuditLogs: async () => {
    return await request('/admin/audit-logs');
  },

  getDbStatus: async () => {
    return await request('/banking/db-status');
  }
};
