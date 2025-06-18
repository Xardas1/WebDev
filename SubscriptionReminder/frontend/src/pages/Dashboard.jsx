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


  return (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-400 to-dark-300 px-8">
    <div className="mr-260 max-w-7xl grid-gird-cols-1 md:grid-cols-2 gap-12 py-20">
      <div className="text-white flex flex-col justify-center">
        <h1 className="text-5xl font-bold leading-tight">
          Subscription Reminder <br /> 
          <spanc className="text-blue-400">
          never forget</spanc> & waste your <br />
          money again
        </h1>
        <p className="mt-4 text-lg text-gray-200 max-w-md">
          Safe money with our very simple system
        </p>
        <div className="mt-7 flex space-x-4">
          <button className='bg-white text-black font-semibold px-6 py-3 rounded'>Try it free</button>
          <button className="bg-black text-white font-semibold px-6 py-3 rounded">See demo</button>
        </div>
      </div>
    </div>
  </div>
);
}

export default Dashboard;
