import React, { useState, useEffect } from 'react';
import api from '../api';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';

const Dashboard = () => {
  const { user, token, logout, loading } = useAuth();
  const [items, setItems] = useState([]);
  const [formData, setFormData] = useState({ subscription_name: '', deadline: '' });
  const [editId, setEditId] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchItems = async () => {
    try {
      const response = await api.get('/subscriptions/');
      setItems(response.data);
    } catch (err) {
      console.error('Fetch error', err);
    }
  };

  useEffect(() => {
    if (token) {
      fetchItems();
    }
  }, [token]);

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setFormData({ ...formData, [event.target.name]: value });
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      if (editId) {
        await api.put(`/subscriptions/${editId}`, formData);
      } else {
        await api.post('/subscriptions', formData);
      }
      fetchItems();
      setFormData({ subscription_name: '', deadline: '' });
      setEditId(null);
    } catch (err) {
      console.error('Submit error', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id) => {
    await api.delete(`/subscriptions/${id}`);
    fetchItems();
  };

  if (!user || !token) return <Navigate to="/login" />;

  return (
  <div className="min-h-screen bg-[#FFFFFF] text-white flex items-center justify-center pt-24 px-4">
    <div className="w-full max-w-4xl space-y-10">
      {/* Header */}
      <div className="bg-white dark:bg-gray-900 text-black dark:text-white rounded-xl shadow-xl p-6 space-y-4 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-white text-center">
          📬 Welcome back, {user?.username || "User"}!
        </h1>
        <p className="text-gray-400 text-sm md:text-base">
          Manage your subscriptions and never miss a renewal.
        </p>
        <button
          onClick={logout}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-md text-white font-semibold"
        >
          Logout
        </button>
      </div>

      {/* Form */}
      <form onSubmit={handleFormSubmit} className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-xl w-full max-w-xl mx-auto space-y-4">
        <div>
          <label className="text-sm font-medium text-gray-300 mb-1">Subscription Name:</label>
          <input
            type="text"
            name="subscription_name"
            value={formData.subscription_name}
            onChange={handleInputChange}
            required
            className="w-full px-4 py-2 rounded-md bg-gray-800 text-white border border-gray-700 placeholder-gray-500"
            placeholder="e.g. Netflix"
          />
        </div>
        <div>
          <label className="text-sm font-medium text-gray-300 mb-1">Deadline:</label>
          <input
            type="date"
            name="deadline"
            value={formData.deadline}
            onChange={handleInputChange}
            required
            className="w-full px-4 py-2 rounded-md bg-gray-800 text-white border border-gray-700"
          />
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
          className={`w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-md ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isSubmitting ? 'Saving...' : editId ? 'Update' : 'Add'} Subscription
        </button>
      </form>

      {/* Subscription List */}
      <div className="w-full max-w-2xl mx-auto">
        <h2 className="text-2xl font-semibold text-white mt-8">📄 Your Subscriptions</h2>
        <ul className="space-y-2 mt-4">
          {items.length === 0 ? (
            <p className="text-gray-400 text-sm">No subscriptions yet.</p>
          ) : (
            items.map((item) => (
              <li key={item.id} className="flex justify-between items-center bg-gray-800 p-4 rounded-md">
                <span className="text-gray-200">
                  <strong>{item.subscription_name}</strong> — {item.deadline}
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded-md text-white"
                  >
                    ❌ Delete
                  </button>
                  <button
                    onClick={() => {
                      setFormData({ subscription_name: item.subscription_name, deadline: item.deadline });
                      setEditId(item.id);
                    }}
                    className="bg-yellow-400 hover:bg-yellow-500 px-3 py-1 rounded-md text-black"
                  >
                    🛠️ Update
                  </button>
                </div>
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  </div>
);
}

export default Dashboard;
