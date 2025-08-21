import React from 'react';

const Footer = ({ onTermsClick }) => {
  return (
    <footer className="footer">
      <div className="container">
        <p>Built with ❤️ by the Respawn Team</p>
        <div className="footer-links">
          <a href="#" className="footer-link">Privacy Policy</a>
          <a 
            href="#" 
            className="footer-link" 
            onClick={onTermsClick}
            style={{ cursor: 'pointer' }}
          >
            Terms of Service
          </a>
          <a href="#" className="footer-link">Contact</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
