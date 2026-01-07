import React, { useState } from 'react';
import './index.css';
import { processComplete, exportAnki } from './api';

interface Flashcard {
  question: string;
  answer: string;
}

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [transcript, setTranscript] = useState('');
  const [videoId, setVideoId] = useState('');
  const [language, setLanguage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setFlashcards([]);
    setTranscript('');

    try {
      const result = await processComplete(url, 'flashcards', language || undefined);
      setFlashcards(result.flashcards);
      setTranscript(result.transcript);
      setVideoId(result.video_id);
    } catch (err: any) {
      setError(err.response?.data?.error || 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (format: 'csv' | 'txt') => {
    try {
      const result = await exportAnki(flashcards, format, 'FastScribe');
      const blob = new Blob([result.content], { type: result.mime_type });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `fastscribe_${videoId}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download file');
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            FastScribe
          </h1>
          <p className="text-xl text-gray-600">
            Convert YouTube videos to Anki flashcards instantly
          </p>
        </header>

        {/* Main Form */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                  YouTube URL
                </label>
                <input
                  type="text"
                  id="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  required
                />
              </div>

              <div className="mb-6">
                <label htmlFor="language" className="block text-sm font-medium text-gray-700 mb-2">
                  Transcription Language
                </label>
                <select
                  id="language"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
                >
                  <option value="">Auto-detect</option>
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="it">Italian</option>
                  <option value="pt">Portuguese</option>
                  <option value="ru">Russian</option>
                  <option value="ja">Japanese</option>
                  <option value="ko">Korean</option>
                  <option value="zh">Chinese</option>
                  <option value="ar">Arabic</option>
                  <option value="hi">Hindi</option>
                  <option value="nl">Dutch</option>
                  <option value="pl">Polish</option>
                  <option value="tr">Turkish</option>
                  <option value="vi">Vietnamese</option>
                  <option value="sv">Swedish</option>
                  <option value="da">Danish</option>
                  <option value="no">Norwegian</option>
                  <option value="fi">Finnish</option>
                </select>
                <p className="mt-2 text-sm text-gray-500">
                  Select the video's language for better accuracy, or leave as auto-detect
                </p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Processing...' : 'Generate Flashcards'}
              </button>
            </form>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}
          </div>

          {/* Results */}
          {flashcards.length > 0 && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  Flashcards ({flashcards.length})
                </h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleDownload('csv')}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Download CSV
                  </button>
                  <button
                    onClick={() => handleDownload('txt')}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Download TXT
                  </button>
                </div>
              </div>

              {/* Flashcards Display */}
              <div className="space-y-4 mb-8">
                {flashcards.map((card, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="mb-2">
                      <span className="text-xs font-semibold text-gray-500 uppercase">Question</span>
                      <p className="text-gray-900 mt-1">{card.question}</p>
                    </div>
                    <div>
                      <span className="text-xs font-semibold text-gray-500 uppercase">Answer</span>
                      <p className="text-gray-700 mt-1">{card.answer}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Transcript Section */}
              <div className="border-t pt-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-bold text-gray-900">Transcript</h3>
                  <button
                    onClick={() => copyToClipboard(transcript)}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm"
                  >
                    Copy to Clipboard
                  </button>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <p className="text-gray-700 whitespace-pre-wrap">{transcript}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-600">
          <p className="mb-2">How to import to Anki:</p>
          <ol className="text-sm space-y-1 max-w-2xl mx-auto">
            <li>1. Download the CSV file</li>
            <li>2. Open Anki → File → Import</li>
            <li>3. Select the downloaded file</li>
            <li>4. Set delimiter to Semicolon (;)</li>
            <li>5. Map fields: Field 1 → Front, Field 2 → Back, Field 3 → Tags</li>
          </ol>
        </footer>
      </div>
    </div>
  );
}

export default App;
