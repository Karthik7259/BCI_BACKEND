import React from 'react';
import Hero from '../components/Hero';
import Features from '../components/Features';
import Footer from '../components/Footer';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <Hero />
      <Features />
      <Footer />
    </div>
  );
};

export default HomePage;