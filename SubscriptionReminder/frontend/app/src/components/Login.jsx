import React, { useState } from 'react';
import { loginFields } from '../constants/formFields';
import Input from '../components/Input';
import FormExtra from './FormExtra';
import api from '../api';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const fields = loginFields;
let fieldsState = {};
fields.forEach(field => fieldsState[field.name] = '');

export default function Login() {
  const [loginState, setLoginState] = useState(fieldsState);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    setLoginState({ ...loginState, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Clear previous errors

    try {
      const params = new URLSearchParams();
      params.append('username', loginState.email);
      params.append('password', loginState.password);

      // ✅ This sets the HTTP-only cookie
      await api.post('/token', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        withCredentials: true,
      });

      // ✅ Now fetches user using the cookie
      await login(); // ✅ Make sure to await this
      
      // ✅ Navigate to product page after successful login
      navigate('/product');
    } catch (error) {
      console.error('Login failed:', error);
      if (error.response?.status === 401) {
        setError('Invalid credentials. Please check your email and password.');
      } else {
        setError('Login failed. Please try again.');
      }
    }
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      {fields.map(field => (
        <Input
          key={field.id}
          handleChange={handleChange}
          value={loginState[field.name]}
          name={field.name}
          type={field.type}
          id={field.id}
          labelText={field.labelText}
          labelFor={field.labelFor}
          isRequired={field.isRequired}
          placeholder={field.placeholder}
          customClass="mb-4 text-black border-neutral-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />
      ))}

      <FormExtra />

      {error && <p className="text-red-500 text-sm">{error}</p>}

      <button
        type="submit"
        className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 cursor-pointer"
      >
        Sign in
      </button>
    </form>
  );
}
