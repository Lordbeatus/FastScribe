"""
FastScribe Flask API Server
Provides REST API endpoints for YouTube transcription and flashcard generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import base64
from urlScraper import YouTubeURLScraper
from transcriber import YouTubeTranscriber
from createNotes import NotesCreator
from formatNotes import NotesFormatter
from apiKeyCycler import get_api_key_cycler, get_next_api_key

app = Flask(__name__)
CORS(app)

# Setup YouTube cookies for production
COOKIES_PATH = None

if os.getenv('YOUTUBE_COOKIES_BASE64'):
    # Decode base64 cookies from environment variable
    try:
        cookies_b64 = os.getenv('YOUTUBE_COOKIES_BASE64')
        cookies_data = base64.b64decode(cookies_b64).decode('utf-8')
        
        # Write to temp file
        temp_cookies = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_cookies.write(cookies_data)
        temp_cookies.close()
        COOKIES_PATH = temp_cookies.name
        print(f"✓ Using cookies from environment variable")
    except Exception as e:
        print(f"⚠ Failed to decode cookies from environment: {e}")

elif os.path.exists('/etc/secrets/cookies.txt'):
    # Use Render secret file
    COOKIES_PATH = '/etc/secrets/cookies.txt'
    print(f"✓ Using cookies from secret file")

elif os.path.exists('cookies.txt'):
    # Use local cookies.txt for development
    COOKIES_PATH = 'cookies.txt'
    print(f"✓ Using local cookies.txt")

else:
    print("⚠ Warning: No cookies configured - YouTube downloads may fail")

# Initialize API key cycler
try:
    cycler = get_api_key_cycler()
    print(f"Using {cycler.get_key_count()} API keys in rotation")
except Exception as e:
    print(f"Warning: API key cycler initialization: {e}")
    cycler = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'FastScribe API',
        'api_keys_available': cycler.get_key_count() if cycler else 0
    })


@app.route('/api/validate-url', methods=['POST'])
def validate_url():
    """Validate YouTube URL and extract video ID"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        scraper = YouTubeURLScraper()
        video_id = scraper.extract_video_id(url)
        
        return jsonify({
            'valid': True,
            'video_id': video_id,
            'standard_url': scraper.get_standard_url()
        })
    
    except ValueError as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/transcribe', methods=['POST'])
def transcribe_video():
    """Get transcript from YouTube video using Whisper"""
    try:
        data = request.get_json()
        url = data.get('url')
        language = data.get('language')  # Optional language code
        cookies_from_browser = data.get('cookies_from_browser')  # Optional: 'chrome', 'firefox', etc.
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Extract video ID
        scraper = YouTubeURLScraper()
        video_id = scraper.extract_video_id(url)
        
        # Get transcript using Whisper (cycler handles API key)
        transcriber = YouTubeTranscriber()
        
        # Use production cookies if available, otherwise use browser cookies from request
        cookies_file = COOKIES_PATH if COOKIES_PATH else data.get('cookies_file')
        
        transcript_text = transcriber.get_transcript(
            video_id, 
            language=language,
            cookies_from_browser=cookies_from_browser if not COOKIES_PATH else None,
            cookies_file=cookies_file
        )
        
        return jsonify({
            'video_id': video_id,
            'transcript': transcript_text,
            'language': language or 'auto'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/create-flashcards', methods=['POST'])
def create_flashcards():
    """Generate flashcards from transcript using GPT"""
    try:
        data = request.get_json()
        transcript = data.get('transcript')
        style = data.get('style', 'flashcards')
        
        if not transcript:
            return jsonify({'error': 'Transcript is required'}), 400
        
        if not API_KEY:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        # Create notes (cycler handles API key)
        creator = NotesCreator(
        formatter = NotesFormatter()
        flashcards = formatter.parse_flashcards(notes)
        
        return jsonify({
            'notes': notes,
            'flashcards': flashcards,
            'count': len(flashcards)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-anki', methods=['POST'])
def export_anki():
    """Generate Anki export file content"""
    try:
        data = request.get_json()
        flashcards = data.get('flashcards')
        format_type = data.get('format', 'csv')  # 'csv' or 'txt'
        deck_name = data.get('deck_name', 'FastScribe')
        
        if not flashcards:
            return jsonify({'error': 'Flashcards are required'}), 400
        
        formatter = NotesFormatter()
        formatter.flashcards = flashcards
        
        # Generate content based on format
        if format_type == 'csv':
            content = []
            for card in flashcards:
                content.append(f"{card['question']};{card['answer']};{deck_name}")
            file_content = '\n'.join(content)
            mime_type = 'text/csv'
        else:  # txt
            content = []
            for card in flashcards:
                content.append(f"{card['question']}\t{card['answer']}")
            file_content = '\n'.join(content)
            mime_type = 'text/plain'
        
        return jsonify({
            'content': file_content,
            'mime_type': mime_type,
            'filename': f'flashcards.{format_type}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-complete', methods=['POST'])
def process_complete():
    """Complete pipeline: URL to flashcards in one call"""
    try:
        data = request.get_json()
        url = data.get('url')
        style = data.get('style', 'flashcards')
        language = data.get('language')  # Optional language code
        cookies_from_browser = data.get('cookies_from_browser')  # Optional
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Step 1: Validate URL
        scraper = YouTubeURLScraper()
        video_id = scraper.extract_video_id(url)
        
        # Step 2: Get transcript using Whisper (cycler handles API key)
        transcriber = YouTubeTranscriber()
        
        # Use production cookies if available, otherwise use browser cookies from request
        cookies_file = COOKIES_PATH if COOKIES_PATH else data.get('cookies_file')
        
        formatted_text = transcriber.get_transcript(
            video_id, 
            language=language,
            cookies_from_browser=cookies_from_browser if not COOKIES_PATH else None,
            cookies_file=cookies_file
        )
        
        # Step 3: Create flashcards (cycler handles API key)
        creator = NotesCreator()
        notes = creator.create_notes(formatted_text, style=style)
        
        # Step 4: Parse flashcards
        formatter = NotesFormatter()
        flashcards = formatter.parse_flashcards(notes)
        
        return jsonify({
            'video_id': video_id,
            'transcript': formatted_text,
            'notes': notes,
            'flashcards': flashcards,
            'count': len(flashcards),
            'language': language or 'auto'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
