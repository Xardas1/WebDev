// src/context/AuthContext.jsx
import React, { createContext, useContext, useEffect, useState } from "react";
import api from "../api";                  // axios instance with withCredentials: true

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser]   = useState(null);
  const [loading, setLoading] = useState(true);

  /* -------------------------- helpers -------------------------- */

  // hit /users/me/ — succeeds only if the cookie is present & valid
  const fetchUser = async () => {
    try {
      const res = await api.get("/users/me/", { withCredentials: true });
      setUser(res.data);
    } catch (err) {
      setUser(null);                       // not logged in
    } finally {
      setLoading(false);
    }
  };

  // called right after /token sets the cookie
  const login = () => {
    fetchUser();
    window.location.href = "https://www.re-mind.xyz/home";
  };

  const logout = async () => {
    // optional backend endpoint that deletes the cookie
    try {
      await api.post("/logout", {}, { withCredentials: true });
    } catch (err) {
      console.warn("Logout endpoint failed (ignored).");
    }
    setUser(null);
    window.location.href = "https://www.re-mind.xyz/home";
  };

  /* -------------------------- bootstrap ------------------------ */

  // on first render, try to read the cookie
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
