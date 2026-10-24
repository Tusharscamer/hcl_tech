import { useState, useEffect } from 'react';
import { authApi } from '../services/authApi';

let authState = {
  user: JSON.parse(localStorage.getItem('apex_user') || 'null'),
  token: localStorage.getItem('apex_token') || null,
  isAuthenticated: !!localStorage.getItem('apex_token')
};

const listeners = new Set();

function emitChange() {
  for (const listener of listeners) {
    listener(authState);
  }
}

export const authStore = {
  getState: () => authState,

  subscribe: (listener) => {
    listeners.add(listener);
    return () => listeners.delete(listener);
  },

  login: async (username, password) => {
    const res = await authApi.login(username, password);
    if (res.success && res.data) {
      const { access_token, customer_id, name, role, email } = res.data;
      const user = { customer_id, name, role, email };
      localStorage.setItem('apex_token', access_token);
      localStorage.setItem('apex_user', JSON.stringify(user));
      authState = {
        user,
        token: access_token,
        isAuthenticated: true
      };
      emitChange();
      return { success: true };
    }
    return { success: false, message: res.message || 'Login failed' };
  },

  logout: () => {
    localStorage.removeItem('apex_token');
    localStorage.removeItem('apex_user');
    authState = {
      user: null,
      token: null,
      isAuthenticated: false
    };
    emitChange();
  }
};

export function useAuth() {
  const [state, setState] = useState(authStore.getState());

  useEffect(() => {
    return authStore.subscribe(setState);
  }, []);

  return {
    ...state,
    login: authStore.login,
    logout: authStore.logout
  };
}
