import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Privacy from './pages/Privacy';

const App = () => {
  const location = useLocation(); // ✅ Keep this inside the Router context
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
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/privacy" element={<Privacy />} />
      </Routes>
    </>
  );
};

export default App;
