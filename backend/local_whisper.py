"""
Local Whisper Transcriber using OpenAI's open-source Whisper
No API keys required - runs entirely locally
"""

import whisper
import os


class LocalWhisperTranscriber:
    """Transcribe audio using local Whisper model"""
    
    def __init__(self, model_size='base'):
        """
        Initialize local Whisper model
        Args:
            model_size: 'tiny', 'base', 'small', 'medium', 'large'
                       tiny: fastest, least accurate (39 MB)
                       base: good balance (74 MB) - recommended for Render
                       small: better quality (244 MB)
                       medium: high quality (769 MB)
                       large: best quality (1550 MB) - may be too large for Render
        """
        self.model_size = model_size
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        print(f"✓ Whisper model loaded")
    
    def transcribe(self, audio_file, language=None):
        """
        Transcribe audio file
        Args:
            audio_file: Path to audio file (mp3, mp4, wav, etc.)
            language: Optional language code (e.g., 'en', 'es', 'fr')
                     If None, auto-detects language
        Returns:
            Transcript text
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        print(f"Transcribing {audio_file}...")
        
        # Transcribe options
        options = {
            'task': 'transcribe',  # or 'translate' to translate to English
            'verbose': False,
        }
        
        if language:
            options['language'] = language
        
        # Transcribe
        result = self.model.transcribe(audio_file, **options)
        
        transcript = result['text']
        detected_language = result.get('language', 'unknown')
        
        print(f"✓ Transcription complete ({detected_language})")
        
        return transcript


# Test if run directly
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python local_whisper.py <audio_file> [language]")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None
    
    transcriber = LocalWhisperTranscriber(model_size='base')
    transcript = transcriber.transcribe(audio_file, language)
    
    print(f"\nTranscript:\n{transcript}")
