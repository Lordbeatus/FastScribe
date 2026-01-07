"""
FastScribe Flask API Server
Provides REST API endpoints for YouTube transcription and flashcard generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from urlScraper import YouTubeURLScraper
from transcriber import YouTubeTranscriber
from createNotes import NotesCreator
from formatNotes import NotesFormatter

app = Flask(__name__)
CORS(app)

# Configuration
API_KEY = os.getenv('OPENAI_API_KEY')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'FastScribe API',
        'openai_configured': bool(API_KEY)
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
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not API_KEY:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        # Extract video ID
        scraper = YouTubeURLScraper()
        video_id = scraper.extract_video_id(url)
        
        # Get transcript using Whisper
        transcriber = YouTubeTranscriber(api_key=API_KEY)
        transcript_text = transcriber.get_transcript(video_id, language=language)
        
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
        
        # Create notes
        creator = NotesCreator(api_key=API_KEY)
        notes = creator.create_notes(transcript, style=style)
        
        # Parse into flashcards
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
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not API_KEY:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        # Step 1: Validate URL
        scraper = YouTubeURLScraper()
        video_id = scraper.extract_video_id(url)
        
        # Step 2: Get transcript using Whisper
        transcriber = YouTubeTranscriber(api_key=API_KEY)
        formatted_text = transcriber.get_transcript(video_id, language=language)
        
        # Step 3: Create flashcards
        creator = NotesCreator(api_key=API_KEY)
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
