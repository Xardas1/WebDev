import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  const navLinks = [
    { href: 'https://www.re-mind.xyz/home', label: 'Home' },
    { href: 'https://app.re-mind.xyz/product', label: 'Demo'},
  ];

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    axios.get("https://webdev-production-4c80.up.railway.app/users/me/", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then ((res) => {
      setUser(res.data);
    })
    .catch(() => {
      localStorage.removeItem("token");
      setUser(null);
    });
  }, []);

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
          <a
            href="https://app.re-mind.xyz/login"
            className="font-semibold text-sm border border-gray-300 rounded-md px-4 py-2 text-gray-800 hover:bg-gray-200 transition cursor-pointer"
          >
            Login
          </a>

          <a
            href="https://app.re-mind.xyz/signup"
            className="font-semibold text-sm rounded-md px-4 py-2 bg-gray-900 text-white hover:bg-gray-700 transition cursor-pointer"
          >
            Sign up
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;