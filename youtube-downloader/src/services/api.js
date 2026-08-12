import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const downloadMedia = async (type, urlsArray) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/${type}`,
      { urls_vid: urlsArray },
      { responseType: 'blob' }
    );

    const blob = new Blob([response.data]);


    const contentDisposition =
  response.headers['content-disposition'] || '';

let filename;

if (urlsArray.length > 1) {
  filename = `${type}.zip`;
} else {
  const filenameStarMatch = contentDisposition.match(
    /filename\*=UTF-8''([^;]+)/i
  );

  const filenameMatch = contentDisposition.match(
    /filename="([^"]+)"/i
  );

  if (filenameStarMatch) {
    filename = decodeURIComponent(filenameStarMatch[1]);
  } else if (filenameMatch) {
    filename = filenameMatch[1];
  } else {
    filename = type === 'audios'
      ? 'audio.mp3'
      : 'video.mp4';
  }
}




    return { blob, filename };

  } catch (error) {
    if (error.response && error.response.data) {
      try {
        const text = await error.response.data.text();

        let message = text;
        try {
          const json = JSON.parse(text);
          if (json.detail) message = json.detail;
        } catch {
      
        }
        throw new Error(message);
      } catch {
        throw new Error('Erro desconhecido ao processar a resposta do servidor.');
      }
    }
    throw error;
  }
};
