import { request } from './api';

export const chatApi = {
  sendMessage: async (message, sessionId = null) => {
    return await request('/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        session_id: sessionId
      })
    });
  },

  getSessions: async () => {
    return await request('/chat/sessions');
  },

  createSession: async (title = 'New Banking Conversation') => {
    return await request('/chat/sessions', {
      method: 'POST',
      body: JSON.stringify({ title })
    });
  },

  getSession: async (sessionId) => {
    return await request(`/chat/sessions/${sessionId}`);
  },

  deleteSession: async (sessionId) => {
    return await request(`/chat/sessions/${sessionId}`, {
      method: 'DELETE'
    });
  },

  confirmAction: async (actionType, actionPayload, confirmed = true, sessionId = null) => {
    return await request('/chat/confirm-action', {
      method: 'POST',
      body: JSON.stringify({
        action_type: actionType,
        action_payload: actionPayload,
        confirmed: confirmed,
        session_id: sessionId
      })
    });
  }
};
