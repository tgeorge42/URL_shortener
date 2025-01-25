import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './HomePage';
import HistoryPage from './HistoryPage';
import RedirectPage from './RedirectPage';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/go/:shortCode" element={<RedirectPage />} />
      </Routes>
    </Router>
  );
}

export default App;
