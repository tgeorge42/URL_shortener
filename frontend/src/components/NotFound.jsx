import React from 'react';
import '../styles/NotFound.css';

const NotFound = () => {
  return (
    <div className="not-found-container">
      <h1 className="not-found-title">404</h1>
      <p className="not-found-text">Oops! The page you're looking for doesn't exist.</p>
      <a href="/" className="not-found-link">Go back to Home</a>
    </div>
  );
};

export default NotFound;
