// src/App.jsx  (app sub-domain)
import React from "react";
import { Routes, Route, useLocation, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";

import Navbar        from "./components/Navbar";
import PrivateRoute  from "./components/PrivateRoute";

import Login         from "./pages/Login";
import Signup        from "./pages/Signup";
import Product       from "./pages/Product";
import ResetPassword from "./pages/ResetPassword";
import ForgotPassword from "./pages/ForgotPassword";

const App = () => {
  const { loading }   = useAuth();       // user state no longer needed here
  const location      = useLocation();

  if (loading) return <p className="text-center text-white">Loading…</p>;

  const hideNavbarRoutes = ["/startup"];
  const shouldHideNavbar = hideNavbarRoutes.includes(location.pathname);

  return (
    <>
      {!shouldHideNavbar && <Navbar />}
      <Routes>
        <Route path="/login"          element={<Login />} />
        <Route path="/signup"         element={<Signup />} />
        <Route path="/product"        element={<PrivateRoute><Product /></PrivateRoute>} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/verify-email" element={<Navigate to="/product" /> } /> 
      </Routes>
    </>
  );
};

export default App;
