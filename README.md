# FastScribe

FastScribe converts YouTube videos into Anki flashcards using OpenAI's Whisper and GPT-4.

## Project Structure

```
FastScribe/
├── backend/              # Flask API server
│   ├── app.py           # Main Flask application
│   ├── apiKeyCycler.py  # API key rotation manager
│   ├── transcriber.py   # YouTube audio download & Whisper transcription
│   ├── createNotes.py   # GPT-4 flashcard generation
│   ├── formatNotes.py   # Anki export formatting
│   ├── urlScraper.py    # YouTube URL parsing
│   ├── main.py          # CLI interface
│   ├── requirements-server.txt  # Production dependencies
│   └── requirements.txt         # Full dependencies
├── frontend/            # React web interface
│   ├── src/
│   ├── public/
│   └── package.json
├── COOKIES.md          # YouTube cookie authentication guide
├── README.md           # This file
└── render.yaml         # Deployment configuration
```

## Quick Start

### Web Interface

Visit the deployed site or run locally:

```bash
# Backend
cd backend
pip install -r requirements-server.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

### Command Line

```bash
cd backend
python main.py
# Enter YouTube URL when prompted
```

## Features

- **Multi-language transcription** - 50+ languages via Whisper API
- **Smart API key rotation** - Load balancing across multiple OpenAI keys
- **Cookie authentication** - Bypass YouTube bot detection
- **Anki export** - CSV and TXT formats ready for import
- **Web interface** - Clean React UI with Tailwind CSS

## How It Works

1. **URL Parsing** - Extracts video ID from any YouTube URL format
2. **Audio Download** - Uses yt-dlp to download audio from video
3. **Transcription** - OpenAI Whisper API converts speech to text
4. **Flashcard Generation** - GPT-4 creates Q&A pairs from transcript
5. **Export** - Formats flashcards for Anki import

## API Endpoints

- `POST /api/validate-url` - Validate YouTube URL
- `POST /api/transcribe` - Transcribe video with Whisper
- `POST /api/create-flashcards` - Generate flashcards with GPT-4
- `POST /api/export-anki` - Format for Anki export
- `POST /api/process-complete` - Full pipeline (URL → flashcards)
- `GET /api/health` - Server health check

## Deployment

Configured for Render deployment. See `render.yaml` for details.

```bash
git push origin main
# Render auto-deploys both frontend and backend
```

## Configuration

### API Keys

The system supports multiple OpenAI API keys for load balancing. Keys are hardcoded in `apiKeyCycler.py` or can be set via environment:

```bash
export OPENAI_API_KEY="sk-..."
```

### YouTube Cookies

If you encounter "bot detection" errors, see [COOKIES.md](COOKIES.md) for authentication setup.

## Technology Stack

**Backend:**
- Flask - REST API
- yt-dlp - YouTube audio download
- OpenAI Whisper - Speech-to-text transcription
- OpenAI GPT-4 - Flashcard generation

**Frontend:**
- React - UI framework
- Tailwind CSS - Styling
- Axios - API communication

## License

MIT

