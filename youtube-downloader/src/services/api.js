import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const downloadMedia = async (type, urlsArray) => {
  const response = await axios.post(
    `${BASE_URL}/${type}`,
    { urls_vid: urlsArray },
    { responseType: 'blob' }
  );

  const blob = new Blob([response.data]);


  const contentDisposition = response.headers['content-disposition'] || '';

  const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
  
  const filename = filenameMatch ? filenameMatch[1] : (urlsArray.length > 1 ? `${type}.zip` : `${type}.mp4`);

  return { blob, filename };
};
