"""
YouTube URL Scraper
Extracts and validates YouTube video IDs from URLs for transcription
"""

import re
from urllib.parse import urlparse, parse_qs


class YouTubeURLScraper:
    """Handle YouTube URL processing and validation"""
    
    def __init__(self):
        self.video_id = None
        self.url = None
    
    def extract_video_id(self, url):
        """
        Extract video ID from various YouTube URL formats
        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        - https://m.youtube.com/watch?v=VIDEO_ID
        """
        if not url:
            raise ValueError("URL cannot be empty")
        
        self.url = url
        
        # Pattern 1: youtu.be short URLs
        if 'youtu.be/' in url:
            match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
            if match:
                self.video_id = match.group(1)
                return self.video_id
        
        # Pattern 2: youtube.com URLs
        if 'youtube.com' in url:
            parsed_url = urlparse(url)
            
            # Check if it's a watch URL
            if parsed_url.path == '/watch':
                query_params = parse_qs(parsed_url.query)
                if 'v' in query_params:
                    self.video_id = query_params['v'][0]
                    return self.video_id
            
            # Check if it's an embed URL
            if '/embed/' in parsed_url.path:
                match = re.search(r'/embed/([a-zA-Z0-9_-]{11})', url)
                if match:
                    self.video_id = match.group(1)
                    return self.video_id
        
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def get_standard_url(self):
        """Return standardized YouTube URL"""
        if not self.video_id:
            raise ValueError("No video ID available. Call extract_video_id first.")
        return f"https://www.youtube.com/watch?v={self.video_id}"
    
    def get_embed_url(self):
        """Return YouTube embed URL"""
        if not self.video_id:
            raise ValueError("No video ID available. Call extract_video_id first.")
        return f"https://www.youtube.com/embed/{self.video_id}"
    
    def validate_url(self, url):
        """Check if URL is a valid YouTube URL"""
        try:
            self.extract_video_id(url)
            return True
        except ValueError:
            return False


def main():
    """Example usage"""
    scraper = YouTubeURLScraper()
    
    # Example URLs
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ"
    ]
    
    for url in test_urls:
        try:
            video_id = scraper.extract_video_id(url)
            print(f"URL: {url}")
            print(f"Video ID: {video_id}")
            print(f"Standard URL: {scraper.get_standard_url()}")
            print("-" * 50)
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
