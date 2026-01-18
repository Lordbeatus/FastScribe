"""
Updated transcriber.py that can use home Whisper server
Falls back to OpenAI API if home server not available
"""

import os
import tempfile
import yt_dlp
import requests
from urlScraper import YouTubeURLScraper


class YouTubeTranscriber:
    """Transcribe YouTube videos using home Whisper server or OpenAI API"""
    
    def __init__(self):
        self.transcript = None
        self.video_id = None
        # Check if home Whisper server is configured
        self.home_whisper_url = os.getenv('WHISPER_API_URL')
        
        if self.home_whisper_url:
            print(f"✅ Using home Whisper server: {self.home_whisper_url}")
        else:
            print("ℹ️  No WHISPER_API_URL found, will use OpenAI API")
    
    def get_transcript(self, video_id_or_url, language=None, cookies_from_browser=None, cookies_file=None):
        """Get transcript using home server or OpenAI API"""
        
        # Extract video ID if URL provided
        if 'youtube.com' in video_id_or_url or 'youtu.be' in video_id_or_url:
            scraper = YouTubeURLScraper()
            video_id = scraper.extract_video_id(video_id_or_url)
        else:
            video_id = video_id_or_url
        
        self.video_id = video_id
        
        # Download audio
        audio_path = self._download_audio(video_id, cookies_from_browser, cookies_file)
        
        try:
            # Try home Whisper server first
            if self.home_whisper_url:
                try:
                    transcript = self._transcribe_with_home_server(audio_path, language)
                    print("✅ Transcribed with home Whisper server")
                    return transcript
                except Exception as e:
                    print(f"⚠️  Home server failed: {e}")
                    print("Falling back to OpenAI API...")
            
            # Fallback to OpenAI API
            transcript = self._transcribe_with_openai(audio_path, language)
            print("✅ Transcribed with OpenAI API")
            return transcript
        
        finally:
            # Cleanup audio file
            try:
                os.remove(audio_path)
            except:
                pass
    
    def _download_audio(self, video_id, cookies_from_browser=None, cookies_file=None):
        """Download audio from YouTube"""
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, 'audio.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }
        
        # Use android client if no cookies (avoids JS runtime requirement)
        if not cookies_file and not cookies_from_browser:
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['android'],
                    'skip': ['hls', 'dash']
                }
            }
        
        # Add cookies if provided
        if cookies_file and os.path.exists(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
        elif cookies_from_browser:
            ydl_opts['cookiesfrombrowser'] = (cookies_from_browser,)
        
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find downloaded file
        for file in os.listdir(temp_dir):
            if file.startswith('audio.'):
                return os.path.join(temp_dir, file)
        
        raise Exception("Failed to download audio")
    
    def _transcribe_with_home_server(self, audio_path, language=None):
        """Transcribe using home Whisper server"""
        url = f"{self.home_whisper_url.rstrip('/')}/transcribe"
        
        with open(audio_path, 'rb') as f:
            files = {'file': f}
            data = {}
            if language:
                data['language'] = language
            
            response = requests.post(url, files=files, data=data, timeout=300)
        
        if response.status_code != 200:
            raise Exception(f"Home server error: {response.text}")
        
        result = response.json()
        return result['text']
    
    def _transcribe_with_openai(self, audio_path, language=None):
        """Transcribe using OpenAI Whisper API"""
        from openai import OpenAI
        from apiKeyCycler import get_next_api_key
        
        api_key = get_next_api_key()
        client = OpenAI(api_key=api_key)
        
        with open(audio_path, 'rb') as audio_file:
            params = {'file': audio_file, 'model': 'whisper-1'}
            if language:
                params['language'] = language
            
            transcript = client.audio.transcriptions.create(**params)
        
        return transcript.text


# For backwards compatibility
def get_transcript(video_id_or_url, language=None, cookies_from_browser=None, cookies_file=None):
    """Legacy function - creates transcriber and gets transcript"""
    transcriber = YouTubeTranscriber()
    return transcriber.get_transcript(video_id_or_url, language, cookies_from_browser, cookies_file)
