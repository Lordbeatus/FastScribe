"""
Local Whisper API Server
Run this on your home computer to provide free transcription service
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import tempfile
import os

app = Flask(__name__)
CORS(app)

# Load Whisper model once at startup
print("Loading Whisper model (this takes a moment)...")
model = whisper.load_model("base")  # 74MB - good balance of speed/quality
print("✅ Whisper model loaded and ready!")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Local Whisper API',
        'model': 'base'
    })


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Transcribe audio file
    
    Expects:
    - file: audio file (mp3, m4a, wav, etc.)
    - language: optional language code (en, es, fr, etc.)
    - fast: optional bool to use faster settings (default: false)
    
    Returns:
    - text: transcribed text
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        language = request.form.get('language', None)
        use_fast = request.form.get('fast', 'false').lower() == 'true'
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            file.save(temp_audio.name)
            temp_path = temp_audio.name
        
        print(f"Transcribing audio file: {temp_path} (fast mode: {use_fast})")
        
        # Build transcription options
        transcribe_opts = {
            'language': language,
            'fp16': False,  # Use FP32 for CPU compatibility (change to True for GPU)
        }
        
        # Optimization: Fast mode for long videos
        if use_fast:
            transcribe_opts.update({
                'beam_size': 1,  # Greedy decoding (default is 5)
                'best_of': 1,    # No temperature fallback (default is 5)
                'condition_on_previous_text': False,  # Faster for long audio
            })
        
        # Transcribe
        result = model.transcribe(temp_path, **transcribe_opts)
        
        # Cleanup
        os.remove(temp_path)
        
        print(f"✅ Transcription complete: {len(result['text'])} characters")
        
        return jsonify({
            'text': result['text'],
            'language': result['language']
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run on all interfaces so it's accessible from network
    port = int(os.getenv('PORT', 8000))
    print(f"\n🚀 Starting Whisper API server on port {port}")
    print(f"📡 Accessible at: http://localhost:{port}")
    print(f"🔍 Health check: http://localhost:{port}/health")
    print(f"\nReady to transcribe! 🎙️\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
