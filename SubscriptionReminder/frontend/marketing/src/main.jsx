import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../app/src/context/AuthContext.jsx';
import './index.css';
import '@fontsource/inter';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider.Provider value={{ user, login, logout, loading, fetchUser }} >
        <App />
      </AuthProvider.Provider>
    </BrowserRouter>
  </React.StrictMode>
);
