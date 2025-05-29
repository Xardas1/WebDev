import React from 'react';
import { Link, useLocation } from 'react-router-dom';


const Navbar = () => {
    const location = useLocation();

    const navLinks = [
        { to: '/dashboard', label: 'Dashboard' },
        { to: '/features', label: 'Features'},
        { to: '/pricing', label: 'Priciing'},
        { to: '/faq', label: 'FAQ'},
    ];

    return (
        <nav className="bg-gray-900 text-white sticky top-0 z-50 shadow-md">
            <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
               <span className="font-bold text-xl">SubReminder</span>
               <div className="flex gap-6">
                 {navLinks.map((link) => (
                    <Link
                       key={link.to}
                       to={link.to}
                       className={`hover:text-blue-400 transition ${
                         location.pathname === link.to ? 'text-blue-400 font-semibold' : 'text-white'
                       }`}
                    >
                        {link.label}
                    </Link>
                 ))}
               </div>
            </div>
        </nav>
    );
};


export default Navbar;