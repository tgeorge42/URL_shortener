import React, { useState, useEffect } from 'react';
import { createShortUrl, fetchAllShortUrls } from '../services/api.jsx';
import '../styles/App.css';

function HomePage() {
  const [url, setUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [shortUrls, setShortUrls] = useState([]);

  useEffect(() => {
    fetchAllShortUrls().then(setShortUrls);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await createShortUrl(url);
    setShortUrl(result.short_code);
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
            {shortUrl && (
                <span className="short-url">
                Short URL: <a href={`http://127.0.0.1:5173/go/${shortUrl}`}>{shortUrl}</a>
                 </span>
            )}
        </form>
        <div style={{ flex: 1, overflow: 'hidden' }}>
            <h2>Recent Shortlinks</h2>
            <ul className="scrollable-list">
            {shortUrls.slice(0, 5).map(({ original_url, short_code, title, id }) => (
                <li key={id}>
                <strong>{title || 'No Title'}</strong>
                <a href={`http://127.0.0.1:5173/go/${short_code}`}>{short_code}</a>
                </li>
            ))}
            </ul>
        </div>
        <p>
            <a href="/history">See all shortlinks</a>
        </p>
        </div>
  );
}

export default HomePage;
