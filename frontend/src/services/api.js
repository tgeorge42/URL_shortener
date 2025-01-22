const apiUrl = 'http://127.0.0.1:8000/api/';

export const createShortUrl = async (url) => {
  const response = await fetch(`${apiUrl}shorten/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  const data = await response.json();
  return data;
};

export const fetchAllShortUrls = async () => {
  const response = await fetch(`${apiUrl}list/`);
  const data = await response.json();
  return data;
};
