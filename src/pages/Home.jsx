import React from 'react';
import { Link } from 'react-router-dom';
import { FiZap, FiBell, FiCheckCircle } from 'react-icons/fi';

const features = [
  {
    icon: <FiBell className="text-blue-500 w-6 h-6" />,
    title: "Smart Reminders",
    desc: "Get notified before any subscription renews. Never pay for what you don't use.",
  },
  {
    icon: <FiCheckCircle className="text-green-500 w-6 h-6" />,
    title: "Simple Management",
    desc: "Add, update, or delete subscriptions in seconds with a clean dashboard.",
  },
  {
    icon: <FiZap className="text-yellow-500 w-6 h-6" />,
    title: "Fast & Secure",
    desc: "Built with speed and user privacy in mind. Your data stays yours.",
  },
];

const Home = () => {
  return (
    <div className="bg-[#FFFFFF] text-white min-h-screen flex items-center justify center py-12">
      {/* Hero */}
      <div className="text-center max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold leading-tight flex items-center">
          📬 Manage Subscriptions <br /> Like a Pro.
        </h1>
        <p className="text-gray-300 text-base sm:text-lg">
          Stay on top of all your recurring payments with one sleek tool.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link
            to="/login"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md font-semibold transition"
          >
            Get Started
          </Link>
          <Link
            to="/features"
            className="border border-gray-500 hover:border-white text-gray-300 px-6 py-3 rounded-md transition"
          >
            See Features
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="mt-20 max-w-5xl mx-auto grid gap-6 sm:grid-cols-2 md:grid-cols-3 px-4">
        {features.map((f, i) => (
          <div
            key={i}
            className="bg-gray-900 p-6 rounded-xl shadow hover:shadow-lg transition-all"
          >
            <div className="mb-4">{f.icon}</div>
            <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
            <p className="text-gray-400 text-sm">{f.desc}</p>
          </div>
        ))}
      </div>

      {/* Pricing Teaser */}
      <div className="mt-20 text-center space-y-4 px-4">
        <h2 className="text-xl sm:text-2xl md:text-3xl font-bold">Simple Pricing</h2>
        <p className="text-gray-400 text-sm sm:text-base">
          Start for free. Upgrade when you're ready.
        </p>
        <Link
          to="/pricing"
          className="inline-block bg-green-500 hover:bg-green-600 text-black px-5 py-2 rounded-md font-medium transition"
        >
          View Pricing Plans
        </Link>
      </div>
    </div>
  );
};

export default Home;
