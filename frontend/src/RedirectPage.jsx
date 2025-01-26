import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchOriginalUrl } from './services/api';

function RedirectPage() {
  const { shortCode } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const handleRedirect = async () => {
      try {
        const originalUrl = await fetchOriginalUrl(shortCode);
        if (originalUrl) {
          window.location.href = originalUrl;
        } else {
            navigate('/notfound');
        }
      } catch (error) {
          console.error('Failed to fetch the original URL:', error);
          navigate('/notfound');
      }
    };

    handleRedirect();
  }, [shortCode, navigate]);

  return <p>Redirecting...</p>;
}

export default RedirectPage;
