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
    await fetchUser(); // ✅ ensure it's awaited
    window.location.href = "/product";
  };

  const logout = async () => {
    try {
      console.log("🔄 Logging out...");
      
      // Call backend logout endpoint
      await api.post("/logout", {}, { withCredentials: true });
      console.log("✅ Backend logout successful");
      
      // Clear user state immediately
      setUser(null);
      console.log("✅ User state cleared");
      
      // Clear any local cookies manually (backup)
      document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.re-mind.xyz";
      document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      console.log("✅ Cookies cleared manually");
      
      // Redirect to home page
      console.log("🔄 Redirecting to home...");
      window.location.href = "https://www.re-mind.xyz/home";
      
    } catch (error) {
      console.error("❌ Logout error:", error);
      
      // Even if backend fails, clear local state and cookies
      setUser(null);
      document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.re-mind.xyz";
      document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      
      // Still redirect
      window.location.href = "https://www.re-mind.xyz/home";
    }
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
