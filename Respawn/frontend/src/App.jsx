import React from 'react';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import FakeUIPreview from './components/FakeUIPreview';
import SignupForm from './components/SignupForm';
import Footer from './components/Footer';
import './App.css';

function App() {
  return (
    <div className="App">
      <Hero />
      <HowItWorks />
      <FakeUIPreview />
      <SignupForm />
      <Footer />
    </div>
  );
}

export default App;
