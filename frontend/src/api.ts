import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const validateUrl = async (url: string) => {
  const response = await api.post('/api/validate-url', { url });
  return response.data;
};

export const transcribeVideo = async (url: string, includeTimestamps: boolean = false) => {
  const response = await api.post('/api/transcribe', { 
    url, 
    include_timestamps: includeTimestamps 
  });
  return response.data;
};

export const createFlashcards = async (transcript: string, style: string = 'flashcards') => {
  const response = await api.post('/api/create-flashcards', { 
    transcript, 
    style 
  });
  return response.data;
};

export const exportAnki = async (flashcards: any[], format: string = 'csv', deckName: string = 'FastScribe') => {
  const response = await api.post('/api/export-anki', { 
    flashcards, 
    format, 
    deck_name: deckName 
  });
  return response.data;
};

export const processComplete = async (url: string, style: string = 'flashcards') => {
  const response = await api.post('/api/process-complete', { 
    url, 
    style 
  });
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export default api;
