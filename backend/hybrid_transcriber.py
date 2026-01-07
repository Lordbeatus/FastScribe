"""
Hybrid Transcriber - supports both local Whisper and OpenAI API
Automatically uses local if no API key is available
"""

import os
import tempfile
import yt_dlp
from urlScraper import YouTubeURLScraper


class HybridTranscriber:
    """Transcribe YouTube videos using local Whisper or OpenAI API"""
    
    def __init__(self, use_local=None, model_size='base'):
        """
        Args:
            use_local: True=force local, False=force API, None=auto-detect
            model_size: For local Whisper: 'tiny', 'base', 'small', 'medium', 'large'
        """
        self.transcript = None
        self.video_id = None
        
        # Auto-detect if not specified
        if use_local is None:
            api_key = os.getenv('OPENAI_API_KEY')
            use_local = not api_key or api_key.startswith('sk-abcde')
        
        self.use_local = use_local
        
        if use_local:
            print(f"Using LOCAL Whisper ({model_size} model)")
            from local_whisper import LocalWhisperTranscriber
            self.whisper = LocalWhisperTranscriber(model_size=model_size)
        else:
            print("Using OpenAI Whisper API")
            from openai import OpenAI
            from apiKeyCycler import get_next_api_key
            api_key = get_next_api_key()
            self.client = OpenAI(api_key=api_key)
    
    def get_transcript(self, url_or_video_id, language=None, cookies_from_browser=None, cookies_file=None):
        """
        Get transcript from YouTube video
        Args:
            url_or_video_id: YouTube URL or video ID
            language: Optional ISO-639-1 language code
            cookies_from_browser: Browser to extract cookies from
            cookies_file: Path to cookies.txt file
        Returns:
            Transcript text
        """
        # Check if input is a URL or video ID
        if url_or_video_id.startswith('http'):
            scraper = YouTubeURLScraper()
            self.video_id = scraper.extract_video_id(url_or_video_id)
            url = scraper.get_standard_url()
        else:
            self.video_id = url_or_video_id
            url = f"https://www.youtube.com/watch?v={url_or_video_id}"
        
        # Create temporary directory for audio file
        temp_dir = tempfile.mkdtemp()
        audio_file = os.path.join(temp_dir, f"{self.video_id}.mp3")
        
        try:
            # Download audio using yt-dlp
            print(f"Downloading audio from video: {self.video_id}")
            
            # Determine if using cookies
            using_cookies = cookies_from_browser or (cookies_file and os.path.exists(cookies_file)) or os.path.exists('cookies.txt')
            
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(temp_dir, f"{self.video_id}.%(ext)s"),
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
            }
            
            # Use android client if not using cookies
            if not using_cookies:
                ydl_opts['extractor_args'] = {'youtube': {'player_client': ['android']}}
            
            # Add cookie options
            if cookies_from_browser:
                ydl_opts['cookiesfrombrowser'] = (cookies_from_browser,)
            elif cookies_file and os.path.exists(cookies_file):
                ydl_opts['cookiefile'] = cookies_file
            elif os.path.exists('cookies.txt'):
                ydl_opts['cookiefile'] = 'cookies.txt'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"Audio downloaded. Transcribing...")
            
            # Transcribe using local or API
            if self.use_local:
                # Use local Whisper
                transcript_text = self.whisper.transcribe(audio_file, language=language)
            else:
                # Use OpenAI API
                with open(audio_file, 'rb') as audio:
                    whisper_params = {
                        "model": "whisper-1",
                        "file": audio,
                        "response_format": "text"
                    }
                    if language:
                        whisper_params["language"] = language
                    
                    transcript_text = self.client.audio.transcriptions.create(**whisper_params)
            
            self.transcript = transcript_text
            
            # Cleanup
            if os.path.exists(audio_file):
                os.remove(audio_file)
            os.rmdir(temp_dir)
            
            return transcript_text
            
        except Exception as e:
            # Cleanup on error
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            raise Exception(f"Error transcribing video: {e}")


if __name__ == '__main__':
    # Test with a known video
    transcriber = HybridTranscriber(use_local=True, model_size='base')
    transcript = transcriber.get_transcript('dQw4w9WgXcQ')
    print(f"\nTranscript preview:\n{transcript[:500]}...")
