// src/context/AuthContext.jsx
import React, { createContext, useContext, useEffect, useState } from "react";
import api from "../api";                // axios instance with withCredentials: true

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser]   = useState(null);
  const [loading, setLoading] = useState(true);

  /* ---------------- helpers ---------------- */

  const fetchUser = async () => {
    try {
      const res = await api.get("/users/me/", { withCredentials: true });
      setUser(res.data);
    } catch {
      setUser(null);                     // not logged in
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    fetchUser();                         // cookie already set by /token
    window.location.href = "https://www.re-mind.xyz/home";
  };

  const logout = async () => {
    try {
      await api.post("/logout", {}, { withCredentials: true });
    } catch {
      /* ignore */ 
    }
    setUser(null);
    window.location.href = "https://www.re-mind.xyz/home";
  };

  /* ------------- bootstrap ------------- */

  useEffect(() => { fetchUser(); }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
