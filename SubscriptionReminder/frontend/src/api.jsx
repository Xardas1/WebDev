// api.jsx
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://webdev-r5ae.onrender.com',
  withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Fetch subscriptions function
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
