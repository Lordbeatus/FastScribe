# FastScribe

FastScribe is an automated system that converts YouTube videos into Anki flashcards using OpenAI's Whisper and GPT-4. The application downloads audio from YouTube videos, transcribes them using Whisper API, and generates study materials formatted for Anki's spaced repetition system. Both command-line and web interfaces are provided.

## Architecture

FastScribe consists of four core processing modules and a Flask API server with React frontend:

### Core Modules

**urlScraper.py**  
Handles YouTube URL parsing and validation. Extracts video IDs from various YouTube URL formats including standard watch URLs, shortened youtu.be links, and embed URLs. Returns standardized video identifiers for downstream processing.

**transcriber.py**  
Downloads audio from YouTube videos using yt-dlp and transcribes them using OpenAI's Whisper API. This approach works for any video regardless of whether captions are available, providing high-quality transcriptions in multiple languages. Automatically handles audio extraction, format conversion, and cleanup of temporary files.

**createNotes.py**  
Generates structured study materials from transcripts using OpenAI's GPT-4. Processes raw transcript text into formatted notes with configurable output styles including flashcards (Q&A format), detailed notes, summaries, and bullet points.

**formatNotes.py**  
Exports flashcards to Anki-compatible formats (CSV and TXT). Parses Q&A formatted notes into structured flashcard data and generates properly delimited files for import into Anki's spaced repetition system. Also includes optional Google Docs export functionality.

### Web Application

**app.py**  
Flask REST API server providing HTTP endpoints for the core processing pipeline. Exposes individual module functions as API routes and includes a complete end-to-end processing endpoint. Handles CORS for frontend integration and includes health check monitoring.

**frontend/**  
React application with Tailwind CSS styling. Single-page application that interfaces with the Flask API to provide a user-friendly web interface for generating flashcards. Users input YouTube URLs and receive downloadable Anki files without data persistence on the server.

## API Endpoints

- `POST /api/validate-url` - Validate YouTube URL and extract video ID
- `POST /api/transcribe` - Download audio and transcribe using Whisper
- `POST /api/create-flashcards` - Generate flashcards from transcript using GPT
- `POST /api/export-anki` - Format flashcards for Anki export
- `POST /api/process-complete` - Full pipeline from URL to flashcards
- `GET /api/health` - Server health check

## Deployment

The application is configured for deployment on Render using the included render.yaml configuration. The backend requires an OpenAI API key set as an environment variable for both Whisper transcription and GPT-4 flashcard generation. The frontend can be deployed as a static site and automatically connects to the backend API.

## Command Line Usage

The main.py script provides a complete command-line pipeline that orchestrates all modules sequentially. It processes a YouTube URL through audio download, Whisper transcription, GPT processing, and Anki export, generating multiple output files in the working directory.

## Output Formats

**Anki CSV Format**: Semicolon-delimited files with Question;Answer;Tags structure  
**Anki TXT Format**: Tab-delimited files with Question\tAnswer structure  
**Raw Transcript**: Whisper-generated transcription text  
**Formatted Notes**: GPT-generated study notes in specified style

## Dependencies

Python backend requires Flask, yt-dlp for audio downloading, OpenAI Python client for Whisper and GPT-4, and supporting libraries listed in requirements-server.txt. Frontend requires React, Axios for API communication, and Tailwind CSS for styling. FFmpeg is required by yt-dlp for audio extraction.
