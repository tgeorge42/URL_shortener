import React, { useState, useEffect } from 'react';
import { createShortUrl, fetchAllShortUrls } from './services/api';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [shortUrls, setShortUrls] = useState([]);

  useEffect(() => {
    fetchAllShortUrls().then(setShortUrls);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await createShortUrl(url);
    setShortUrl(result.short_url);
    fetchAllShortUrls().then(setShortUrls);
  };

  return (
    <div className="container">
      <h1>URL Shortener</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="url"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button type="submit">Shorten</button>
      </form>
      {shortUrl && (
        <p>
          Short URL: <a href={`http://127.0.0.1:8000/go/${shortUrl}`}>{shortUrl}</a>
        </p>
      )}
      <h2>All Shortlinks</h2>
      <ul>
        {shortUrls.map(({ original_url, short_code, title }) => (
          <li key={short_code}>
            <strong>{title || 'No Title'}</strong> -{' '}
            <a href={`http://127.0.0.1:8000/go/${short_code}`}>{short_code}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
