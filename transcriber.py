"""
YouTube Video Transcriber
Downloads and formats transcripts from YouTube videos
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from urlScraper import YouTubeURLScraper


class YouTubeTranscriber:
    """Transcribe YouTube videos"""
    
    def __init__(self):
        self.transcript = None
        self.formatted_text = None
        self.video_id = None
    
    def get_transcript(self, url_or_video_id):
        """
        Get transcript from YouTube video
        Args:
            url_or_video_id: YouTube URL or video ID
        Returns:
            List of transcript segments
        """
        # Check if input is a URL or video ID
        if url_or_video_id.startswith('http'):
            scraper = YouTubeURLScraper()
            self.video_id = scraper.extract_video_id(url_or_video_id)
        else:
            self.video_id = url_or_video_id
        
        try:
            # Get transcript list for the video
            api = YouTubeTranscriptApi()
            transcript_list = api.list(self.video_id)
            
            # Try to get English transcript first
            try:
                transcript_obj = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
                self.transcript = transcript_obj.fetch()
                return self.transcript
            except:
                # If no English, get the first available transcript
                transcript_obj = transcript_list.find_generated_transcript(['en'])
                self.transcript = transcript_obj.fetch()
                return self.transcript
        
        except TranscriptsDisabled:
            raise Exception(f"Transcripts are disabled for video: {self.video_id}")
        
        except NoTranscriptFound:
            raise Exception(f"No transcript found for video: {self.video_id}")
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")
    
    def format_transcript(self, include_timestamps=False):
        """
        Format transcript into readable text
        Args:
            include_timestamps: Include timestamps in output
        Returns:
            Formatted transcript string
        """
        if not self.transcript:
            raise ValueError("No transcript available. Call get_transcript first.")
        
        if include_timestamps:
            formatted = []
            for entry in self.transcript:
                timestamp = self._format_timestamp(entry['start'])
                text = entry['text']
                formatted.append(f"[{timestamp}] {text}")
            self.formatted_text = '\n'.join(formatted)
        else:
            # Join all text segments
            self.formatted_text = ' '.join([entry['text'] for entry in self.transcript])
        
        return self.formatted_text
    
    def _format_timestamp(self, seconds):
        """Convert seconds to MM:SS format"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def save_transcript(self, filename, include_timestamps=False):
        """Save transcript to file"""
        if not self.formatted_text:
            self.format_transcript(include_timestamps)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.formatted_text)
        
        print(f"Transcript saved to: {filename}")


def main():
    """Example usage"""
    transcriber = YouTubeTranscriber()
    
    # Example: Get transcript from URL
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        transcript = transcriber.get_transcript(url)
        formatted_text = transcriber.format_transcript(include_timestamps=False)
        
        print("Transcript preview:")
        print(formatted_text[:500] + "...")
        
        # Save to file
        transcriber.save_transcript("transcript.txt")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
