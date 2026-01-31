import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import RankingDashboard from './components/RankingDashboard';
import AboutUs from './components/AboutUs';

function App() {
  return (
    <div className="bg-background min-h-screen font-sans">
      <Navbar />
      <main>
        <Hero />
        <RankingDashboard />
        <AboutUs />
      </main>
    </div>
  );
}

export default App;
