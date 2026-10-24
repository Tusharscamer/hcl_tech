const BASE_URL = '/api';

export async function request(endpoint, options = {}) {
  const token = localStorage.getItem('apex_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...(options.headers || {})
  };

  const config = {
    ...options,
    headers
  };

  try {
    const res = await fetch(`${BASE_URL}${endpoint}`, config);
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(`API request failed for ${endpoint}:`, err);
    return {
      success: false,
      message: err.message || 'Network error connecting to banking services'
    };
  }
}
