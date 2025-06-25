import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // ✅ Import useAuth

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth(); // ✅ Access auth context

    const navLinks = [
    { href: 'https://reminded.vercel.app/home', label: 'Home' },
    { href: 'https://app-reminded.vercel.app/product', label: 'Demo'},
  ];



  return (
    <nav className="bg-transparent text-black top-0 z-50 text-base w-full">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between relative">

        {/* Left: Logo */}
        <div className="flex-shrink-0">
          <span className="font-bold text-2xl">Re:Mind</span>
        </div>

        {/* Center: Nav links */}
        <div className="absolute left-1/2 transform -translate-x-1/2 flex gap-8">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-gray-600 hover:text-neutral-800 text-xl transition"
            >
              {link.label}
            </a>
          ))}
        </div>

        {/* Right: Auth buttons or greeting */}
        <div className="flex gap-4 items-center">
          {user ? (
            <>
              <span className="text-sm font-semibold text-gray-700">
                Hello, {user.username}
              </span>
              <button
                onClick={logout}
                className="text-sm px-3 py-2 border rounded-md hover:bg-gray-200 transition"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <a
                href="https://app-reminded.vercel.app/login"
                className="font-semibold text-sm border border-gray-300 rounded-md px-4 py-2 text-gray-800 hover:bg-gray-200 transition cursor-pointer"
              >
                Login
              </a>

              <a
                href="https://app-reminded.vercel.app/signup"
                className="font-semibold text-sm rounded-md px-4 py-2 bg-gray-900 text-white hover:bg-gray-700 transition cursor-pointer"
              >
                Sign up
              </a>
            </>
          )}
        </div>

      </div>
    </nav>
  );
};

export default Navbar;