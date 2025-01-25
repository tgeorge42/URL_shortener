import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchOriginalUrl } from './services/api';

function RedirectPage() {
  const { shortCode } = useParams();

  useEffect(() => {
    const handleRedirect = async () => {
      try {
        const originalUrl = await fetchOriginalUrl(shortCode);
        if (originalUrl) {
          window.location.href = originalUrl; // Redirige vers l'URL d'origine
        } else {
          alert('URL not found.');
        }
      } catch (error) {
        console.error('Failed to fetch the original URL:', error);
      }
    };

    handleRedirect();
  }, [shortCode]);

  return <p>Redirecting...</p>; // Vous pouvez personnaliser le message ou ajouter un spinner
}

export default RedirectPage;
