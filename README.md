# FastScribe

FastScribe is an automated system that converts YouTube videos into Anki flashcards using OpenAI's Whisper and GPT-4. The application downloads audio from YouTube videos, transcribes them using Whisper API, and generates study materials formatted for Anki's spaced repetition system. Both command-line and web interfaces are provided.

## Architecture

FastScribe consists of four core processing modules and a Flask API server with React frontend:

### Core Modules

**urlScraper.py**  
Handles YouTube URL parsing and validation. Extracts video IDs from various YouTube URL formats including standard watch URLs, shortened youtu.be links, and embed URLs. Returns standardized video identifiers for downstream processing.

**transcriber.py**  
Downloads audio from YouTube videos using yt-dlp and transcribes them using OpenAI's Whisper API. This approach works for any video regardless of whether captions are available, providing high-quality transcriptions in multiple languages. Automatically handles audio extraction, format conversion, and cleanup of temporary files. Supports cookie-based authentication to bypass YouTube bot detection.

**createNotes.py**  
Generates structured study materials from transcripts using OpenAI's GPT-4. Processes raw transcript text into formatted notes with configurable output styles including flashcards (Q&A format), detailed notes, summaries, and bullet points. Integrates with the API key rotation system for load balancing.

**formatNotes.py**  
Exports flashcards to Anki-compatible formats (CSV and TXT). Parses Q&A formatted notes into structured flashcard data and generates properly delimited files for import into Anki's spaced repetition system. Also includes optional Google Docs export functionality with lazy imports to avoid deployment issues.

**apiKeyCycler.py**  
Thread-safe API key rotation manager that distributes OpenAI API requests across 50 hardcoded keys. Uses round-robin scheduling to prevent rate limiting on individual keys. Provides a global singleton instance for consistent key cycling across the application.

### Web Application

**app.py**  
Flask REST API server providing HTTP endpoints for the core processing pipeline. Exposes individual module functions as API routes and includes a complete end-to-end processing endpoint. Handles CORS for frontend integration and includes health check monitoring. Initializes the API key cycler on startup.

**frontend/**  
React application with Tailwind CSS styling. Single-page application that interfaces with the Flask API to provide a user-friendly web interface for generating flashcards. Features language selection dropdown, real-time processing feedback, and downloadable Anki exports. Users input YouTube URLs and receive flashcards without data persistence on the server.

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

The system supports multiple OpenAI API keys for load balancing. Keys are hardcoded in `backend/apiKeyCycler.py` or can be set via environment:

```bash
export OPENAI_API_KEY="sk-..."
```

### YouTube Cookies for Production

For production deployment on Render, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for complete cookie setup instructions.

**Quick summary:**
1. Export cookies from your browser using "Get cookies.txt LOCALLY" extension
2. Upload to Render as environment variable (base64) or secret file
3. The app automatically detects and uses production cookies

### Development Setup

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

## Deployment

Configured for Render deployment. See `render.yaml` for configuration details.

```bash
git push origin main
# Render auto-deploys both frontend and backend
```

Full deployment guide: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

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

