const apiUrl = 'http://127.0.0.1:8000/api/';

// API call to shorten an URL
export async function createShortUrl(originalUrl) {
  const response = await fetch(`${apiUrl}shorten/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      original_url: originalUrl,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to create short URL');
  }

  return await response.json();
}

// API call to get all data
export const fetchAllShortUrls = async () => {
  const response = await fetch(`${apiUrl}list/`);
  const data = await response.json();
  return data;
};

// API call to get the original URL based on a short URL
export const fetchOriginalUrl = async (shortCode) => {
  const response = await fetch(`${apiUrl}urls/${shortCode}/`);

  if (!response.ok) {
    throw new Error(`Failed to fetch original URL for shortCode: ${shortCode}`);
  }

  const data = await response.json();
  return data.original_url;
};
