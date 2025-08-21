import React from 'react';

const Hero = () => {
  const scrollToSignup = () => {
    const signupSection = document.getElementById('signup');
    if (signupSection) {
      signupSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="section">
      <div className="container">
        <div className="hero-content">
          <h1>Quit Addictions Like It's an RPG Game</h1>
          <p className="hero-subtitle">
            Respawn: Level up your life, track progress, and defeat your final boss — your addiction.
          </p>
          <button className="btn" onClick={scrollToSignup}>
            Join the Waitlist
          </button>
        </div>
      </div>
    </section>
  );
};

export default Hero;
