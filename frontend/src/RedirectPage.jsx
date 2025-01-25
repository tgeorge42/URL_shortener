import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchOriginalUrl } from './services/api'; // Assure-toi que cette fonction existe et fonctionne correctement

function RedirectPage() {
  const { shortCode } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const handleRedirect = async () => {
      try {
        const originalUrl = await fetchOriginalUrl(shortCode);
        if (originalUrl) {
          window.location.href = originalUrl; // Redirige vers l'URL d'origine
        } else {
          // Si l'URL est introuvable, redirige vers la page NotFound
          navigate('/notfound');
        }
      } catch (error) {
        console.error('Failed to fetch the original URL:', error);
        navigate('/notfound'); // En cas d'erreur, redirige vers la page NotFound
      }
    };

    handleRedirect();
  }, [shortCode, navigate]); // Ajout de navigate comme dépendance

  return <p>Redirecting...</p>; // Vous pouvez personnaliser le message ou ajouter un spinner
}

export default RedirectPage;
