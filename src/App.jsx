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

const App = () => {
  const { token, loading } = useAuth();
  const location = useLocation(); // ✅ Keep this inside the Router context

  if (loading) return <p className="text-center text-white mt-8">Loading...</p>;

  const hideNavbarRoutes = ['/login', '/register'];
  const shouldHideNavbar = hideNavbarRoutes.includes(location.pathname);

  return (



        <>
      {!shouldHideNavbar&& (
        <div className="flex justify-center items-center gap-6 p-5 bg-[#FFFFFF] text-white">
          <a href="/dashboard" className="hover:underline">Dashboard</a>
          <a href="/features" className="hover:underline">Features</a>
          <a href="/pricing" className="hover:underline">Pricing</a>
          <a href="/faq" className="hover:underline"></a>
        </div>
      )}
      {!shouldHideNavbar && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/features" element={<Features />} />
        <Route path="/faq" element={<FAQ />} />
        <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>



  );
};

export default App;
