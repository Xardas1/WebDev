import React, { useState } from 'react';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import FakeUIPreview from './components/FakeUIPreview';
import SignupForm from './components/SignupForm';
import Footer from './components/Footer';
import TermsOfService from './components/TermsOfService';
import './App.css';

function App() {
  const [showTerms, setShowTerms] = useState(false);

  return (
    <div className="App">
      <Hero />
      <HowItWorks />
      <FakeUIPreview />
      <SignupForm />
      <Footer onTermsClick={() => setShowTerms(true)} />
      
      {/* Terms of Service Modal */}
      {showTerms && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          zIndex: 1000,
          overflowY: 'auto',
          padding: '20px'
        }}>
          <div style={{
            position: 'relative',
            maxWidth: '900px',
            margin: '0 auto',
            background: 'white',
            borderRadius: '8px',
            padding: '20px'
          }}>
            <button
              onClick={() => setShowTerms(false)}
              style={{
                position: 'absolute',
                top: '10px',
                right: '15px',
                background: 'none',
                border: 'none',
                fontSize: '24px',
                cursor: 'pointer',
                color: '#666',
                padding: '5px'
              }}
            >
              ×
            </button>
            <TermsOfService />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
