// api.jsx
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://remind.fly.dev',
  withCredentials: true, // ✅ Send cookies automatically
});

// ✅ POST /token → logs user in, cookie is set by server
export const loginWithCredentials = async (email, password) => {
  try {
    const response = await api.post(
      '/token',
      new URLSearchParams({
        username: email,
        password: password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

// ✅ Example of protected request
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
