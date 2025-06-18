import React, { useState } from 'react';
import api from '../api'; // your axios instance

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/forgot-password', { email });
      setMessage('✅ Reset link sent! Check your inbox.');
    } catch (err) {
      console.error(err);
      setMessage('❌ Could not send reset link.');
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center px-4">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6 text-center">Forgot Password</h2>
        
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email address
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-4 py-2 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black"
        />

        <button
          type="submit"
          className="w-full bg-black text-white py-2 rounded-md hover:bg-neutral-800 transition"
        >
          Send Reset Link
        </button>

        {message && <p className="mt-4 text-center text-sm text-black">{message}</p>}
      </form>
    </div>
  );
};

export default ForgotPassword;
