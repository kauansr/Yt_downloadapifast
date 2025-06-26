import React, { useState } from 'react';
import styles from '../styles/Home.module.css';
import { downloadMedia } from '../services/api';

const Home = () => {
  const [urlsInput, setUrlsInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleDownload = async (type) => {
    setLoading(true);

  
    const urlsArray = urlsInput
      .split(/[\n,]+/)
      .map(url => url.trim())
      .filter(url => url.length > 0);

    if (urlsArray.length === 0) {
      alert('Digite pelo menos uma URL válida.');
      setLoading(false);
      return;
    }

    try {
      const { blob, filename } = await downloadMedia(type, urlsArray);
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.click();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      alert('Erro ao baixar. Verifique as URLs.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Youtube Downloader</h1>

      <textarea
        className={styles.textarea}
        placeholder="Paste one or more URLs (one per line or separated by commas)"
        rows={8}
        value={urlsInput}
        onChange={(e) => setUrlsInput(e.target.value)}
      />

      <div className={styles.buttonGroup}>
        <button onClick={() => handleDownload('videos')} disabled={loading}>
          {loading ? 'Downloading vídeos...' : 'Download Vídeo(s)'}
        </button>
        <button onClick={() => handleDownload('audios')} disabled={loading}>
          {loading ? 'Downloading áudios...' : 'Download Áudio(s)'}
        </button>
      </div>
    </div>
  );
};

export default Home;
