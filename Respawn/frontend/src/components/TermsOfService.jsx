import React from 'react';

const TermsOfService = () => {
  return (
    <div style={{
      maxWidth: '800px',
      margin: '0 auto',
      padding: '2rem',
      lineHeight: '1.6',
      color: '#333'
    }}>
      <h1 style={{ 
        color: '#2c3e50', 
        marginBottom: '2rem',
        textAlign: 'center'
      }}>
        Terms of Service
      </h1>
      
      <div style={{
        background: 'white',
        padding: '2rem',
        borderRadius: '8px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ color: '#34495e', marginBottom: '1rem' }}>1. Acceptance of Terms</h2>
        <p>By accessing and using Respawn, you accept and agree to be bound by the terms and provision of this agreement.</p>
        
        <h2 style={{ color: '#34495e', marginBottom: '1rem', marginTop: '2rem' }}>2. Use License</h2>
        <p>Permission is granted to temporarily download one copy of Respawn for personal, non-commercial transitory viewing only.</p>
        
        <h2 style={{ color: '#34495e', marginBottom: '1rem', marginTop: '2rem' }}>3. Disclaimer</h2>
        <p>The materials on Respawn are provided on an 'as is' basis. Respawn makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.</p>
        
        <h2 style={{ color: '#34495e', marginBottom: '1rem', marginTop: '2rem' }}>4. Limitations</h2>
        <p>In no event shall Respawn or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Respawn.</p>
        
        <h2 style={{ color: '#34495e', marginBottom: '1rem', marginTop: '2rem' }}>5. Privacy Policy</h2>
        <p>Your privacy is important to us. Please review our Privacy Policy, which also governs your use of the Service, to understand our practices.</p>
        
        <h2 style={{ color: '#34495e', marginBottom: '1rem', marginTop: '2rem' }}>6. Contact Information</h2>
        <p>If you have any questions about these Terms of Service, please contact us.</p>
        
        <hr style={{ 
          margin: '3rem 0 2rem 0',
          border: 'none',
          borderTop: '1px solid #e9ecef'
        }} />
        
        {/* Attribution Section */}
        <div style={{
          marginTop: '2rem',
          padding: '1.5rem',
          background: '#f8f9fa',
          borderRadius: '6px',
          border: '1px solid #e9ecef',
          fontSize: '0.9rem',
          color: '#6c757d',
          textAlign: 'center'
        }}>
          <p style={{ margin: '0 0 0.5rem 0' }}>
            <strong>Attribution</strong>
          </p>
          <p style={{ margin: 0 }}>
            ❤️ The favicon/icon used in this application was created by Freepik from Flaticon (
            <a 
              href="https://www.flaticon.com/authors/freepik" 
              target="_blank" 
              rel="noopener noreferrer"
              style={{ color: '#007bff', textDecoration: 'none' }}
            >
              https://www.flaticon.com/authors/freepik
            </a>
            ). This icon is licensed under Flaticon Free License, free for personal and commercial use with attribution.
          </p>
        </div>
      </div>
    </div>
  );
};

export default TermsOfService;
