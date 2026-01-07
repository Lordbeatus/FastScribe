"""
YouTube Video Transcriber using yt-dlp and OpenAI Whisper
Downloads audio and transcribes using OpenAI's Whisper API
"""

import os
import tempfile
import yt_dlp
from openai import OpenAI
from urlScraper import YouTubeURLScraper


class YouTubeTranscriber:
    """Transcribe YouTube videos using Whisper API"""
    
    def __init__(self, api_key=None):
        self.transcript = None
        self.formatted_text = None
        self.video_id = None
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        self.client = OpenAI(api_key=self.api_key)
    
    def get_transcript(self, url_or_video_id):
        """
        Get transcript from YouTube video using yt-dlp and Whisper
        Args:
            url_or_video_id: YouTube URL or video ID
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
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(temp_dir, f"{self.video_id}.%(ext)s"),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"Audio downloaded. Transcribing with Whisper...")
            
            # Transcribe using OpenAI Whisper API
            with open(audio_file, 'rb') as audio:
                transcript_response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    response_format="text"
                )
            
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
