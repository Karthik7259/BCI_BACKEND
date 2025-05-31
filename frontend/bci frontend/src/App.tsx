import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ModesPage from './pages/ModesPage';
import ClassificationPage from './pages/ClassificationPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/classify" element={<ClassificationPage />} />
        <Route path="/modes/:mode" element={<ModesPage />} />
      </Routes>
    </Router>
  );
}

export default App;