// api.jsx
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://webdev-production-4c80.up.railway.app/',
  withCredentials: true, // ✅ Include cookies in *every* request
});

// ✅ LOGIN: use this to get the token + set-cookie on login
export const login = async (email, password) => {
  try {
    const response = await api.post(
      '/token',
      new URLSearchParams({
        username: email,
        password: password,
      }),
      {
        withCredentials: true, // ✅ CRITICAL: browser accepts the cookie
      }
    );
    return response.data;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

// ✅ Fetch subscriptions (example protected route)
export const fetchSubscriptions = async () => {
  try {
    const response = await api.get('/subscriptions/');
    return response.data;
  } catch (error) {
    console.error('Error fetching subscriptions:', error);
    throw error;
  }
};

export default api;
