// src/context/AuthContext.jsx
import React, { createContext, useContext, useEffect, useState } from "react";
import api from "../api"; // axios instance with withCredentials: true

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  /* ---------------- helpers ---------------- */

  const fetchUser = async () => {
    setLoading(true); // ✅ ensure loading is triggered again on fetch
    try {
      const res = await api.get("/users/me/", { withCredentials: true });
      setUser(res.data);
    } catch {
      setUser(null); // not logged in
    } finally {
      setLoading(false);
    }
  };

  const login = async () => {
    await fetchUser(); // ✅ ensure it’s awaited
    window.location.href = "https://www.re-mind.xyz/home";
  };

  const logout = async () => {
    try {
      await api.post("/logout", {}, { withCredentials: true });
    } catch {
      // silently ignore
    }
    setUser(null);
    window.location.href = "https://www.re-mind.xyz/home";
  };

  /* ------------- bootstrap ------------- */
  useEffect(() => {
    fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
