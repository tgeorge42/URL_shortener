import React, { useState, useEffect } from 'react';
import { fetchAllShortUrls } from '../services/api.jsx';
import '../styles/History.css';

function HistoryPage() {
  const [shortUrls, setShortUrls] = useState([]);

  useEffect(() => {
    fetchAllShortUrls().then(setShortUrls);
  }, []);

  return (
    <div className="container">
      <h1>All Shortlinks</h1>
      <ul className='scrollable-history'>
        {shortUrls.map(({ original_url, short_code, title }) => (
          <li key={short_code}>
          <strong>{title || 'No Title'}</strong>
          <a href={`http://127.0.0.1:5173/go/${short_code}`}>{short_code}</a>
        </li>
        ))}
      </ul>

      <p>
        <a href="/">Back to Home</a>
      </p>
    </div>
  );
}

export default HistoryPage;
