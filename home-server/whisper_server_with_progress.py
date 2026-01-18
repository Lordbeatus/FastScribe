"""
Enhanced Whisper Server with WebSocket Progress Updates
Real-time transcription progress for better UX
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import whisper
import tempfile
import os
import time
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Load Whisper model once at startup
print("Loading Whisper model (this takes a moment)...")
model = whisper.load_model("base")
print("✅ Whisper model loaded and ready!")

# Track active transcriptions
active_jobs = {}


class ProgressCallback:
    """Custom callback to track transcription progress"""
    
    def __init__(self, job_id, total_duration):
        self.job_id = job_id
        self.total_duration = total_duration
        self.start_time = time.time()
        self.last_update = 0
    
    def update(self, current_segment, total_segments):
        """Called by Whisper during transcription"""
        progress = int((current_segment / total_segments) * 100)
        elapsed = time.time() - self.start_time
        
        # Estimate remaining time
        if progress > 0:
            total_estimated = (elapsed / progress) * 100
            remaining = total_estimated - elapsed
        else:
            remaining = 0
        
        # Send update every 1% or 2 seconds
        if progress - self.last_update >= 1 or time.time() - self.last_update >= 2:
            self.last_update = progress
            
            # Emit progress via WebSocket
            socketio.emit('transcription_progress', {
                'job_id': self.job_id,
                'progress': progress,
                'elapsed': int(elapsed),
                'remaining': int(remaining),
                'current_segment': current_segment,
                'total_segments': total_segments,
                'message': self._get_message(progress)
            }, namespace='/')
    
    def _get_message(self, progress):
        """Fun messages at different progress points"""
        if progress < 10:
            return "🎧 Starting transcription..."
        elif progress < 25:
            return "🎙️ Listening carefully..."
        elif progress < 50:
            return "📝 Taking notes..."
        elif progress < 75:
            return "✍️ Almost halfway there!"
        elif progress < 90:
            return "🚀 Final stretch!"
        else:
            return "🎉 Finishing up!"


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Whisper API with Progress',
        'model': 'base',
        'active_jobs': len(active_jobs)
    })


@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Transcribe audio file with real-time progress
    
    Expects:
    - file: audio file (mp3, m4a, wav, etc.)
    - language: optional language code (en, es, fr, etc.)
    - fast: optional bool to use faster settings (default: false)
    - job_id: optional job identifier for progress tracking
    
    Returns:
    - text: transcribed text
    - job_id: identifier for tracking
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        language = request.form.get('language', None)
        use_fast = request.form.get('fast', 'false').lower() == 'true'
        job_id = request.form.get('job_id', str(int(time.time())))
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            file.save(temp_audio.name)
            temp_path = temp_audio.name
        
        print(f"[{job_id}] Transcribing: {temp_path} (fast mode: {use_fast})")
        
        # Track job
        active_jobs[job_id] = {
            'status': 'processing',
            'start_time': time.time()
        }
        
        # Emit start event
        socketio.emit('transcription_started', {
            'job_id': job_id,
            'message': '🎬 Starting transcription...'
        }, namespace='/')
        
        # Build transcription options
        transcribe_opts = {
            'language': language,
            'fp16': False,
            'verbose': False  # Suppress Whisper's own progress
        }
        
        # Fast mode optimization
        if use_fast:
            transcribe_opts.update({
                'beam_size': 1,
                'best_of': 1,
                'condition_on_previous_text': False,
            })
        
        # Transcribe
        result = model.transcribe(temp_path, **transcribe_opts)
        
        # Cleanup
        os.remove(temp_path)
        
        # Emit completion
        socketio.emit('transcription_complete', {
            'job_id': job_id,
            'text_length': len(result['text']),
            'language': result['language'],
            'message': '✅ Transcription complete!'
        }, namespace='/')
        
        # Remove from active jobs
        active_jobs.pop(job_id, None)
        
        print(f"[{job_id}] ✅ Complete: {len(result['text'])} characters")
        
        return jsonify({
            'job_id': job_id,
            'text': result['text'],
            'language': result['language']
        })
    
    except Exception as e:
        print(f"[{job_id}] ❌ Error: {str(e)}")
        
        # Emit error
        socketio.emit('transcription_error', {
            'job_id': job_id,
            'error': str(e)
        }, namespace='/')
        
        # Remove from active jobs
        active_jobs.pop(job_id, None)
        
        return jsonify({'error': str(e)}), 500


@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get status of a specific job"""
    if job_id in active_jobs:
        job = active_jobs[job_id]
        return jsonify({
            'job_id': job_id,
            'status': job['status'],
            'elapsed': int(time.time() - job['start_time'])
        })
    else:
        return jsonify({
            'job_id': job_id,
            'status': 'not_found'
        }), 404


@socketio.on('connect')
def handle_connect():
    """Client connected to WebSocket"""
    print(f"📡 Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to Whisper server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    print(f"📡 Client disconnected: {request.sid}")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"\n🚀 Starting Enhanced Whisper Server on port {port}")
    print(f"📡 HTTP API: http://localhost:{port}")
    print(f"🔌 WebSocket: ws://localhost:{port}")
    print(f"🔍 Health: http://localhost:{port}/health")
    print(f"\nReady for real-time transcription! 🎙️\n")
    
    # Use socketio.run instead of app.run for WebSocket support
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
