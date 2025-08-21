import React from 'react';
import heartIcon from '../assets/pixel-icons/heart.svg';
import swordIcon from '../assets/pixel-icons/sword.svg';
import shieldIcon from '../assets/pixel-icons/shield.svg';
import './HowItWorks.css';

const HowItWorks = () => {
  const steps = [
    {
      icon: heartIcon,
      title: "Daily Quests",
      description: "Build streaks with small wins"
    },
    {
      icon: swordIcon,
      title: "Gain XP",
      description: "Earn rewards as you stay clean"
    },
    {
      icon: shieldIcon,
      title: "Defeat Bosses",
      description: "Conquer challenges and overcome addiction"
    }
  ];

  return (
    <section className="section">
      <div className="container">
        <h2>How It Works</h2>
        <p>Transform your recovery journey into an epic adventure</p>
        
        <div className="steps-grid">
          {steps.map((step, index) => (
            <div key={index} className="step-card">
              <div className="howitworks-icon">
                <img 
                  src={step.icon} 
                  alt={step.title}
                />
              </div>
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
