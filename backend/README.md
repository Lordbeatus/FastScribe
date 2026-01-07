# Backend - FastScribe API

Flask REST API for YouTube video transcription and flashcard generation.

## Setup

```bash
pip install -r requirements-server.txt
```

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."  # Optional if using cycler
export FLASK_ENV="development"  # or "production"
export PORT=5000
```

## Run

```bash
python app.py
```

Server runs on `http://localhost:5000`

## Modules

- **app.py** - Flask REST API server
- **apiKeyCycler.py** - Rotates through 50 OpenAI API keys
- **transcriber.py** - Downloads audio with yt-dlp, transcribes with Whisper
- **createNotes.py** - Generates flashcards with GPT-4
- **formatNotes.py** - Exports to Anki CSV/TXT formats
- **urlScraper.py** - Parses YouTube URLs
- **main.py** - Command-line interface

## API Documentation

### POST /api/process-complete

Complete pipeline from URL to flashcards.

**Request:**
```json
{
  "url": "https://youtube.com/watch?v=...",
  "language": "en",
  "cookies_from_browser": "chrome"
}
```

**Response:**
```json
{
  "video_id": "...",
  "transcript": "...",
  "notes": "...",
  "flashcards": [...],
  "count": 10,
  "language": "en"
}
```

### POST /api/transcribe

Transcribe video only.

### POST /api/create-flashcards

Generate flashcards from existing transcript.

### POST /api/export-anki

Format flashcards for Anki export.

## Dependencies

- Flask, flask-cors
- yt-dlp
- openai
- gunicorn (production)

## Deployment

See `../render.yaml` for Render deployment configuration.
