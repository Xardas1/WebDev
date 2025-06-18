import React, { useEffect, useState } from 'react';
import api from '../api'; // 👈 assumes you have axios instance here
import { useAuth } from '../context/AuthContext';
import { Hammer } from 'lucide-react';
import { X } from 'lucide-react';

const Product = () => {
  const { token, loading } = useAuth();
  const [subscriptions, setSubscriptions] = useState([]);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    subscription_name: '',
    deadline: ''
  });
  const [editingId, setEditingId] = useState(null);


  const handleSubmit = async (e) => {
    e.preventDefault();         // This prevents the page from reloading

    try {
      if (editingId) {
        // Update mode
        await api.put(`/subscriptions/${editingId}`, formData);
      } else {
        // Create mode
        await api.post(`/subscriptions/`, formData);
      }
    
    
    // Reset
    setFormData({ subscription_name: '', deadline: ''});
    setEditingId(null);

    const response = await api.get('/subscriptions');
    setSubscriptions(response.data);
    } catch (error) {
      console.error(editingId ? "Update failed" : "Add failed", error);
    }
  };



  const handleDelete = async (id) => {
    try {
      await api.delete(`/subscriptions/${id}`);
      setSubscriptions(prevSubs => prevSubs.filter(sub => sub.id !== id));
      //const updated = await api.get('/subscriptions');
      //setSubscriptions(updated.data);
    } catch (err) {
      console.error("Faild to delete subscription:", err);
      setError("Failed to delte subscription");
    }
  };

  // 🔁 Fetch subscriptions from the backend
  useEffect(() => {
    if (token) {
      api.get('/subscriptions/')
        .then((res) => {
          setSubscriptions(res.data);
        })
        .catch((err) => {
          setError('Failed to fetch subscriptions');
          console.error("Full error:", err.response?.data || err.messagee || err);
        });
    }
  }, [token]);

  if (loading) {
    return <p className="text-center text-white">Loading...</p>;
  }

  return (
    <div className="min-h-screen text-black p-10">
      <div className="max-w-4xl mx-auto">

        <form onSubmit={handleSubmit}>
            <div className="flex flex-col items-center space-y-6 mt-50">
              <div className="flex flex-col items-start w-96">
                <label className="block text-xl font-medium mb-2">Subscription Name</label>
                <input
                  name="subscription_name"
                  value={formData.subscription_name}
                  onChange={(e) => setFormData({ ...formData, [e.target.name]: e.target.value })}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-3 focus:ring-black"
                  placeholder="e.g Netflix"
                  required
                />
              </div>

              <div className="flex flex-col items-start w-96">
                <label htmlFor="deadline" className="block text-xl font-medium mb-2">
                  Deadline
                </label>
                <input
                  type="date"
                  name="deadline"
                  value={formData.deadline}
                  onChange={(e) => setFormData({ ...formData, [e.target.name]: e.target.value })}
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 shadow-sm focus:outline-none focus:ring-3 focus:ring-black"
                  required
                />
              </div>
            </div>
       


        <div className="flex justify-center mt-7">
          <button 
              type="submit"
              className='py-2 px-4 border border-transparent font-medium rounded-md text-white bg-black hover:bg-neutral-800 transition shadow-md focus:ring-2 focus:ring-offset-2  mt-5'
          >
            {editingId ? 'Update Subscription' : 'Add Subscription'}
          </button>
        </div>
        </form>


        <div className="mt-8">
          <h2 className="text-2xl font-semibold mb-8 text-center">Your Subscriptions</h2>
          <ul className="space-y-4">
            {subscriptions.map((sub) => (
              <li key={sub.id} className="bg-white text-black px-6 py-3 rounded-lg shadow-md flex justify-between items-center hover:bg-gray-50">
                <div>
                  <p className="font-bold">{sub.subscription_name}</p>
                  <p className="text-lg text-gray-600">Deadline: {sub.deadline}</p>
                </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => {
                    setEditingId(sub.id);
                    setFormData({
                      subscription_name: sub.subscription_name,
                      deadline: sub.deadline
                    });
                  }}
                >
                  <Hammer className="w-9 h-9 hover:text-yellow-500" />
                </button>

                  <button
                    onClick={() => handleDelete(sub.id)}
                  >
                    <X className="w-11 h-11 hover:text-red-600" />
                  </button>

                  {editingId && (
                    <div className="flex justify-center mt-2">
                      <button
                        type="button"
                        onClick={() => {
                          setEditingId(null);
                          setFormData({ subscription_name: '', deadline: ''});
                        }}
                        className="py-1 px-3 text-sm bg-gray-500 text-white rounded-md mb-2 hover:bg-neutral-800"
                      >
                        Cancel Edit
                      </button>
                    </div>
                  )}
                </div> 
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Product;
