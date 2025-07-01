import React, { createContext, useContext, useState, useEffect } from 'react';
import api, { fetchSubscriptions } from '../api'; // Make sure this sends token automatically
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUser = async () => {
    try {
      const response = await api.get('/users/me/', {
        withCredentials: true, // ✅ Make sure cookie is sent
      });
      setUser(response.data);
    } catch (error) {
      console.error("Error fetching user:", error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    fetchUser(); // ✅ use after login
    window.location.href = 'https://www.re-mind.xyz/home';
  };

  const logout = async () => {
    try {
      await api.post('/logout', {}, { withCredentials: true });
    } catch (err) {
      console.warn("Logout failed silently.");
    }
    setUser(null);
    window.location.href = 'https://www.re-mind.xyz/home';
  };

  useEffect(() => {
    fetchUser(); // ✅ auto-fetch if cookie exists
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
