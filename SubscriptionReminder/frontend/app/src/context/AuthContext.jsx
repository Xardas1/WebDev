import React, { createContext, useContext, useState, useEffect } from 'react';
import api, { fetchSubscriptions } from '../api'; // Make sure this sends token automatically
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // ✅ Improved login function with navigation
  const login = (newToken) => {
    console.log("Logging in with token:", newToken);
    setToken(newToken);
    localStorage.setItem('token', newToken);
    fetchUser(newToken);
    window.location.href = 'https://www.re-mind.xyz/home';
  };

  // ✅ Improved logout function with redirection
  const logout = () => {
    console.log("Logging out");
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    window.location.href = 'https://www.re-mind.xyz/home';
    // Redirect to login page after logout
  };

  // ✅ Fetch user data from the server
  const fetchUser = async (currentToken) => {
    console.log('Fetching user with token:', currentToken);

    if (!currentToken) {
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
      setLoading(false);
      window.location.href = 'https://www.re-mind.xyz/home';
      return;
    }

    try {
      const response = await api.get('/users/me/', {
        headers: {
          Authorization: `Bearer ${currentToken}`,  // Include the token in the request header
        },
      });
      console.log('User fetched:', response.data);
      setUser(response.data);
    } catch (error) {
      console.error('Invalid token or error fetching user:', error.response?.data || error.message);
      setUser(null);
      setToken(null);
      localStorage.removeItem('token');
      window.location.href = 'https://www.re-mind.xyz/home';

    } finally {
      setLoading(false);
    }
  };

  // ✅ Auto-fetch user on app load
  useEffect(() => {
    const storedToken = localStorage.getItem('token');

    if (storedToken) {
      fetchUser(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
