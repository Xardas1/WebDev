import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api';

const ResetPassword = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    // Get the token from URL
    const token = new URLSearchParams(location.search).get('token');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/reset-password', {
                token,
                new_password: password,
            });
            setMessage('✅ Password reset successfully!');
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            console.error(err);
            setMessage('❌ Failed to reset password.')
        }
    };

    return (
        <div className="min-h-screen flex justify-center items-center">
            <form onSubmit={handleSubmit} className="space-y-6 bg-whitee p-8 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold text-black">Reset Password</h2>
                <input
                    type="password"
                    placeholder="New Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="w-full px-4 py-2 border rounded-md text-black"
                />
                <button type="submit" className="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800">
                    Reset Password
                </button>
                    {message && <p className="text-center mt-4 text-black">{message}</p>}
            </form>
        </div>
    );
};

export default ResetPassword;