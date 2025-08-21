import React, { useState } from 'react';

const SignupForm = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('submitting');
    
    try {
      const response = await fetch('https://formspree.io/f/meozbnpe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
      
      if (response.ok) {
        setStatus('success');
        setEmail('');
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('error');
    }
  };

  return (
    <section className="section" id="signup">
      <div className="container">
        <h2>Ready to Level Up?</h2>
        <p>Be among the first 100 players to try Respawn</p>
        
        <div className="signup-form">
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              name="email"
              className="form-input"
              placeholder="Enter your email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <button type="submit" className="btn">
              Join Respawn Early Access
            </button>
          </form>
          
          {status === 'success' && (
            <p style={{ color: '#00ff88', marginTop: '1rem' }}>
              ✅ You're on the Respawn waitlist!
            </p>
          )}
          
          {status === 'error' && (
            <p style={{ color: '#ff4757', marginTop: '1rem' }}>
              ⚠️ Something went wrong, please try again.
            </p>
          )}
          
          <p className="form-subtext">
            Be among the first 100 players to try Respawn.
          </p>
        </div>
      </div>
    </section>
  );
};

export default SignupForm;
