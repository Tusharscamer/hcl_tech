import { useState, useEffect } from 'react';
import { chatApi } from '../services/chatApi';

const SAVED_SESSION_KEY = 'apex_chat_session_id';

let chatState = {
  sessions: [],
  currentSessionId: localStorage.getItem(SAVED_SESSION_KEY) || null,
  messages: [],
  isLoading: false,
  isSessionsLoading: false,
  activeExecution: null,
  error: null
};

const listeners = new Set();

function emitChange() {
  for (const listener of listeners) {
    listener(chatState);
  }
}

export const chatStore = {
  getState: () => chatState,

  subscribe: (listener) => {
    listeners.add(listener);
    return () => listeners.delete(listener);
  },

  loadSessions: async () => {
    chatState = { ...chatState, isSessionsLoading: true };
    emitChange();

    try {
      const res = await chatApi.getSessions();
      if (res.success && Array.isArray(res.data)) {
        const sessions = res.data;
        let activeId = chatState.currentSessionId;

        // If stored active session doesn't exist in server list, pick the first
        if (!activeId || !sessions.find(s => s.session_id === activeId)) {
          activeId = sessions.length > 0 ? sessions[0].session_id : null;
        }

        chatState = {
          ...chatState,
          sessions,
          currentSessionId: activeId,
          isSessionsLoading: false
        };

        if (activeId) {
          localStorage.setItem(SAVED_SESSION_KEY, activeId);
          await chatStore.loadSessionMessages(activeId);
        } else {
          emitChange();
        }
      } else {
        chatState = { ...chatState, isSessionsLoading: false };
        emitChange();
      }
    } catch (err) {
      chatState = { ...chatState, isSessionsLoading: false, error: err.message };
      emitChange();
    }
  },

  loadSessionMessages: async (sessionId) => {
    chatState = { ...chatState, isLoading: true };
    emitChange();

    try {
      const res = await chatApi.getSession(sessionId);
      if (res.success && res.data) {
        const msgs = (res.data.messages || []).map(m => ({
          id: m.message_id || `msg-${Date.now()}`,
          sender: m.sender,
          text: m.text,
          answer_type: m.answer_type || 'conversational',
          tools_invoked: m.tools_invoked || [],
          systems_queried: m.systems_queried || [],
          trace_id: m.trace_id,
          requires_confirmation: m.requires_confirmation,
          action_type: m.action_type,
          action_payload: m.action_payload,
          structured_data: m.structured_data,
          timestamp: m.created_at ? new Date(m.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }));

        chatState = {
          ...chatState,
          currentSessionId: sessionId,
          messages: msgs,
          isLoading: false
        };
        localStorage.setItem(SAVED_SESSION_KEY, sessionId);
      } else {
        chatState = { ...chatState, isLoading: false };
      }
    } catch (err) {
      chatState = { ...chatState, isLoading: false, error: err.message };
    }
    emitChange();
  },

  selectSession: async (sessionId) => {
    if (chatState.currentSessionId === sessionId) return;
    await chatStore.loadSessionMessages(sessionId);
  },

  createNewSession: async (title = 'New Banking Conversation') => {
    chatState = { ...chatState, isLoading: true };
    emitChange();

    try {
      const res = await chatApi.createSession(title);
      if (res.success && res.data) {
        const newSession = res.data.session;
        const initialMsgs = (res.data.messages || []).map(m => ({
          id: m.message_id || `msg-${Date.now()}`,
          sender: m.sender,
          text: m.text,
          answer_type: m.answer_type || 'conversational',
          tools_invoked: m.tools_invoked || [],
          systems_queried: m.systems_queried || [],
          trace_id: m.trace_id,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }));

        chatState = {
          ...chatState,
          sessions: [newSession, ...chatState.sessions],
          currentSessionId: newSession.session_id,
          messages: initialMsgs,
          isLoading: false,
          error: null
        };
        localStorage.setItem(SAVED_SESSION_KEY, newSession.session_id);
      } else {
        chatState = { ...chatState, isLoading: false, error: res.message };
      }
    } catch (err) {
      chatState = { ...chatState, isLoading: false, error: err.message };
    }
    emitChange();
  },

  deleteSession: async (sessionId) => {
    try {
      const res = await chatApi.deleteSession(sessionId);
      if (res.success) {
        const remaining = chatState.sessions.filter(s => s.session_id !== sessionId);
        let nextActiveId = chatState.currentSessionId;

        if (chatState.currentSessionId === sessionId) {
          nextActiveId = remaining.length > 0 ? remaining[0].session_id : null;
        }

        chatState = {
          ...chatState,
          sessions: remaining,
          currentSessionId: nextActiveId
        };

        if (nextActiveId) {
          localStorage.setItem(SAVED_SESSION_KEY, nextActiveId);
          await chatStore.loadSessionMessages(nextActiveId);
        } else {
          localStorage.removeItem(SAVED_SESSION_KEY);
          // If no sessions remain, create a fresh one
          await chatStore.createNewSession();
        }
      }
    } catch (err) {
      chatState = { ...chatState, error: err.message };
      emitChange();
    }
  },

  sendMessage: async (userText) => {
    if (!userText.trim()) return;

    // Auto-create session if none active
    let activeSessionId = chatState.currentSessionId;
    if (!activeSessionId) {
      const res = await chatApi.createSession('New Banking Conversation');
      if (res.success && res.data) {
        activeSessionId = res.data.session.session_id;
        chatState.sessions = [res.data.session, ...chatState.sessions];
        chatState.currentSessionId = activeSessionId;
        localStorage.setItem(SAVED_SESSION_KEY, activeSessionId);
      }
    }

    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: userText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    chatState = {
      ...chatState,
      messages: [...chatState.messages, userMsg],
      isLoading: true,
      error: null,
      activeExecution: {
        step: 'Analyzing intent and planning tools...',
        tools: []
      }
    };
    emitChange();

    try {
      const res = await chatApi.sendMessage(userText, activeSessionId);
      if (res.success && res.data) {
        const d = res.data;
        const botMsg = {
          id: `bot-${Date.now()}`,
          sender: 'assistant',
          text: d.answer,
          answer_type: d.answer_type,
          tools_invoked: d.tools_invoked,
          systems_queried: d.systems_queried,
          trace_id: d.trace_id,
          requires_confirmation: d.requires_confirmation,
          action_type: d.action_type,
          action_payload: d.action_payload,
          structured_data: d.structured_data,
          latency_ms: d.latency_ms,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        // Update session list title/timestamp in state
        const updatedSessions = chatState.sessions.map(s => {
          if (s.session_id === activeSessionId) {
            const isFirst = !s.title || s.title === 'New Banking Conversation' || s.title === 'Daily Banking Chat';
            return {
              ...s,
              title: isFirst ? userText.slice(0, 36) + (userText.length > 36 ? '...' : '') : s.title,
              updated_at: new Date().toISOString(),
              message_count: (s.message_count || 0) + 2
            };
          }
          return s;
        });

        chatState = {
          ...chatState,
          sessions: updatedSessions,
          messages: [...chatState.messages, botMsg],
          isLoading: false,
          activeExecution: null
        };
      } else {
        chatState = {
          ...chatState,
          isLoading: false,
          activeExecution: null,
          error: res.message || 'Error processing request'
        };
      }
    } catch (err) {
      chatState = {
        ...chatState,
        isLoading: false,
        activeExecution: null,
        error: err.message
      };
    }
    emitChange();
  },

  confirmAction: async (actionType, actionPayload, confirmed) => {
    chatState = { ...chatState, isLoading: true };
    emitChange();

    try {
      const res = await chatApi.confirmAction(actionType, actionPayload, confirmed, chatState.currentSessionId);
      const outcome = res.success ? (res.data?.message || 'Action executed successfully under bank oversight.') : 'Action failed.';
      const confirmMsg = {
        id: `action-${Date.now()}`,
        sender: 'assistant',
        text: outcome,
        answer_type: 'action_completed',
        tools_invoked: [actionType.toLowerCase()],
        trace_id: res.data?.approval_id || 'ACT-CONFIRMED',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      chatState = {
        ...chatState,
        messages: [...chatState.messages, confirmMsg],
        isLoading: false
      };
    } catch (err) {
      chatState = {
        ...chatState,
        isLoading: false,
        error: err.message
      };
    }
    emitChange();
  },

  clearChat: async () => {
    if (chatState.currentSessionId) {
      await chatStore.deleteSession(chatState.currentSessionId);
    } else {
      await chatStore.createNewSession();
    }
  }
};

export function useChat() {
  const [state, setState] = useState(chatStore.getState());

  useEffect(() => {
    const unsub = chatStore.subscribe(setState);
    // Load sessions initially if not yet loaded
    if (state.sessions.length === 0 && !state.isSessionsLoading) {
      chatStore.loadSessions();
    }
    return unsub;
  }, []);

  return {
    ...state,
    loadSessions: chatStore.loadSessions,
    selectSession: chatStore.selectSession,
    createNewSession: chatStore.createNewSession,
    deleteSession: chatStore.deleteSession,
    sendMessage: chatStore.sendMessage,
    confirmAction: chatStore.confirmAction,
    clearChat: chatStore.clearChat
  };
}
