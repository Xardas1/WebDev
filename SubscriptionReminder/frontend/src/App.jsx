import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Features from './pages/Features';
import FAQ from './pages/FAQ';
import NotFound from './pages/NotFound';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Signup from "./pages/Signup";
import Pricing from "./pages/Pricing";
import Product from "./pages/Product";
import PrivateRoute from './components/PrivateRoute';
import ResetPassword from './pages/ResetPassword';
import ForgotPassword from './pages/ForgotPassword';
import Privacy from './pages/Privacy';

const App = () => {
  const { token, loading } = useAuth();
  const location = useLocation(); // ✅ Keep this inside the Router context

  if (loading) return <p className="text-center text-white ">Loading...</p>;

  const hideNavbarRoutes = ['/startup', '/register'];
  const shouldHideNavbar = hideNavbarRoutes.includes(location.pathname);

  return (
        <>
      {!shouldHideNavbar&& (
        <div className="flex justify-center items-center gap-6 text-white">
          <a href="/faq" className="hover:underline"></a>
        </div>
      )}

      {!shouldHideNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
        <Route path="/features" element={<Features />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/faq" element={<FAQ />} />
        <Route path="*" element={<NotFound />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/product" element={<PrivateRoute> <Product /> </PrivateRoute> } />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
      </Routes>
    </>

  );
};

export default App;
