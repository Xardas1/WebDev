import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Navbar from './components/Navbar';
import Signup from "./pages/Signup";
import Product from "./pages/Product";
import PrivateRoute from './components/PrivateRoute';
import ResetPassword from './pages/ResetPassword';
import ForgotPassword from './pages/ForgotPassword';

const App = () => {
  const { token, loading } = useAuth();
  const location = useLocation(); // ✅ Keep this inside the Router context

  if (loading) return <p className="text-center text-white ">Loading...</p>;

  const hideNavbarRoutes = ['/startup'];
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
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/product" element={<PrivateRoute> <Product /> </PrivateRoute> } />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
      </Routes>
    </>

  );
};

export default App;
