# FastScribe

FastScribe is an automated system that converts YouTube video transcripts into Anki flashcards using GPT-4. The application provides both a command-line interface and a web-based frontend for processing educational content from YouTube videos into study materials.

## Architecture

FastScribe consists of four core processing modules and a Flask API server with React frontend:

### Core Modules

**urlScraper.py**  
Handles YouTube URL parsing and validation. Extracts video IDs from various YouTube URL formats including standard watch URLs, shortened youtu.be links, and embed URLs. Returns standardized video identifiers for downstream processing.

**transcriber.py**  
Downloads and formats video transcripts using the YouTube Transcript API. Retrieves available transcripts in multiple languages, with preference for English. Supports both plain text and timestamped transcript formats.

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
- `POST /api/transcribe` - Download video transcript
- `POST /api/create-flashcards` - Generate flashcards from transcript using GPT
- `POST /api/export-anki` - Format flashcards for Anki export
- `POST /api/process-complete` - Full pipeline from URL to flashcards
- `GET /api/health` - Server health check

## Deployment

The application is configured for deployment on Render using the included render.yaml configuration. The backend requires an OpenAI API key set as an environment variable. The frontend can be built and served statically or run on a development server.

## Command Line Usage

The main.py script provides a complete command-line pipeline that orchestrates all modules sequentially. It processes a YouTube URL through transcript download, GPT processing, and Anki export, generating multiple output files in the working directory.

## Output Formats

**Anki CSV Format**: Semicolon-delimited files with Question;Answer;Tags structure  
**Anki TXT Format**: Tab-delimited files with Question\tAnswer structure  
**Raw Transcript**: Plain text or timestamped transcript files  
**Formatted Notes**: GPT-generated study notes in specified style

## Dependencies

Python backend requires Flask, youtube-transcript-api, OpenAI Python client, and supporting libraries listed in requirements-server.txt. Frontend requires React, Axios for API communication, and Tailwind CSS for styling.
