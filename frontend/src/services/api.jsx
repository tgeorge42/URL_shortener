const apiUrl = 'http://127.0.0.1:8000/api/';

export async function createShortUrl(originalUrl) {
  const response = await fetch(`${apiUrl}shorten/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      original_url: originalUrl,  // Assurez-vous que c'est bien "original_url"
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to create short URL');
  }

  return await response.json();
}

export const fetchAllShortUrls = async () => {
  const response = await fetch(`${apiUrl}list/`);
  const data = await response.json();
  return data;
};

export const fetchOriginalUrl = async (shortCode) => {
  const response = await fetch(`${apiUrl}urls/${shortCode}/`);  // Assurez-vous que l'URL est correcte

  if (!response.ok) {
    throw new Error(`Failed to fetch original URL for shortCode: ${shortCode}`);
  }

  const data = await response.json();
  return data.original_url; // Assurez-vous que le backend renvoie { "original_url": "<URL d'origine>" }
};
