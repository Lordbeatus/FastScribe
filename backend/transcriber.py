"""
YouTube Video Transcriber using yt-dlp and OpenAI Whisper
Downloads audio and transcribes using OpenAI's Whisper API
"""

import os
import tempfile
import yt_dlp
from openai import OpenAI
from urlScraper import YouTubeURLScraper
from apiKeyCycler import get_next_api_key


class YouTubeTranscriber:
    """Transcribe YouTube videos using Whisper API"""
    
    def __init__(self, api_key=None):
        self.transcript = None
        self.formatted_text = None
        self.video_id = None
        # Use provided key or get next from cycler
        self.api_key = api_key or get_next_api_key()
        self.client = OpenAI(api_key=self.api_key)
    
    def get_transcript(self, url_or_video_id, language=None, cookies_from_browser=None, cookies_file=None):
        """
        Get transcript from YouTube video using yt-dlp and Whisper
        Args:
            url_or_video_id: YouTube URL or video ID
            language: Optional ISO-639-1 language code (e.g., 'en', 'es', 'fr', 'de', 'ja', 'zh')
                     If None, Whisper will auto-detect the language
            cookies_from_browser: Browser to extract cookies from (e.g., 'chrome', 'firefox', 'edge')
            cookies_file: Path to cookies.txt file in Netscape format
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
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
                'nocheckcertificate': True,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
            }
            
            # Android client works best without JavaScript runtime
            # BUT android doesn't support cookies, so only use it when we DON'T have cookies
            if not using_cookies:
                # No cookies: android is best choice (fast, no JS needed)
                ydl_opts['extractor_args'] = {'youtube': {'player_client': ['android']}}
                print("Using android client (no cookies)")
            else:
                # With cookies: we MUST skip android and accept that web client needs JS runtime
                # This will only work in environments with Node.js or where videos don't trigger JS challenges
                print("WARNING: Using web client with cookies - requires JavaScript runtime")
                print("If this fails, remove cookies to use android client instead")
                # Don't set player_client at all - let yt-dlp use default with cookies
                # ydl_opts['extractor_args'] = {'youtube': {'player_client': ['web']}}
            
            # Add cookie options if provided
            if cookies_from_browser:
                ydl_opts['cookiesfrombrowser'] = (cookies_from_browser,)
                print(f"Using cookies from browser: {cookies_from_browser}")
            elif cookies_file and os.path.exists(cookies_file):
                ydl_opts['cookiefile'] = cookies_file
                print(f"Using cookies from file: {cookies_file}")
            elif os.path.exists('cookies.txt'):
                # Check for default cookies.txt in current directory
                ydl_opts['cookiefile'] = 'cookies.txt'
                print("Using cookies from cookies.txt")
            
            # First, try to get video info to check if it's accessible
            print("Checking video availability...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    
                    # Check if video has any audio/video formats
                    formats = info.get('formats', [])
                    audio_formats = [f for f in formats if f.get('acodec') != 'none']
                    
                    if not audio_formats:
                        # Check if it's a live stream, premiere, or unavailable
                        if info.get('is_live'):
                            raise Exception("Cannot transcribe live streams. Please wait until the stream is finished.")
                        elif info.get('live_status') == 'is_upcoming':
                            raise Exception("This video is a scheduled premiere that hasn't started yet. Please try again after it airs.")
                        elif info.get('availability') in ['private', 'premium_only', 'subscriber_only']:
                            raise Exception(f"This video is {info.get('availability')} and cannot be downloaded.")
                        else:
                            raise Exception("No audio formats available for this video. It may be restricted, deleted, or region-locked.")
                    
                    print(f"Video is accessible. Found {len(audio_formats)} audio formats.")
                    
                except yt_dlp.utils.DownloadError as e:
                    error_msg = str(e)
                    if "Private video" in error_msg:
                        raise Exception("This is a private video and cannot be accessed.")
                    elif "Video unavailable" in error_msg:
                        raise Exception("This video is unavailable. It may have been deleted or restricted.")
                    elif "Sign in" in error_msg or "not a bot" in error_msg:
                        raise Exception("YouTube is blocking this request. Please configure cookies authentication. See COOKIES.md for setup instructions.")
                    else:
                        raise Exception(f"Cannot access video: {error_msg}")
            
            # Now download the audio
            print("Downloading audio...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            lang_msg = f" ({language})" if language else " (auto-detect)"
            print(f"Audio downloaded. Transcribing with Whisper{lang_msg}...")
            
            # Transcribe using OpenAI Whisper API
            whisper_params = {
                "model": "whisper-1",
                "file": open(audio_file, 'rb'),
                "response_format": "text"
            }
            
            # Add language parameter if specified
            if language:
                whisper_params["language"] = language
            
            transcript_response = self.client.audio.transcriptions.create(**whisper_params)
            
            self.formatted_text = transcript_response
            print(f"Transcription complete!")
            
            return self.formatted_text
        
        except Exception as e:
            raise Exception(f"Error transcribing video: {str(e)}")
        
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                os.rmdir(temp_dir)
            except:
                pass
    
    def format_transcript(self, include_timestamps=False):
        """
        Format transcript into readable text
        Note: Whisper API doesn't provide timestamps in basic mode
        Args:
            include_timestamps: Not supported in this version
        Returns:
            Formatted transcript string
        """
        if not self.formatted_text:
            raise ValueError("No transcript available. Call get_transcript first.")
        
        return self.formatted_text
    
    def save_transcript(self, filename):
        """Save transcript to file"""
        if not self.formatted_text:
            raise ValueError("No transcript available. Call get_transcript first.")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.formatted_text)
        
        print(f"Transcript saved to: {filename}")


def main():
    """Example usage"""
    transcriber = YouTubeTranscriber()
    
    # Example: Get transcript from URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        transcript_text = transcriber.get_transcript(url)
        
        print("Transcript preview:")
        print(transcript_text[:500] + "...")
        
        # Save to file
        transcriber.save_transcript("transcript.txt")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
