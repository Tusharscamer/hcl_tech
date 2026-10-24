import { request } from './api';

export const authApi = {
  login: async (usernameOrId, password) => {
    return await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        username_or_id: usernameOrId,
        password: password
      })
    });
  },

  getCurrentUser: async () => {
    return await request('/auth/me');
  }
};
