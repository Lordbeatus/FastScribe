"""
Free Transcriber - Uses local Whisper only (no API costs)
Generate notes manually with GitHub Copilot Chat
"""

import os
import tempfile
import yt_dlp
from local_whisper import LocalWhisperTranscriber
from urlScraper import YouTubeURLScraper


class FreeTranscriber:
    """Transcribe YouTube videos using local Whisper (100% free)"""
    
    def __init__(self, model_size='base'):
        """
        Args:
            model_size: 'tiny' (fastest), 'base' (recommended), 'small', 'medium', 'large'
        """
        print(f"Initializing FREE transcriber with Whisper {model_size} model")
        self.whisper = LocalWhisperTranscriber(model_size=model_size)
        self.video_id = None
    
    def transcribe_video(self, url_or_video_id, language=None, cookies_file=None):
        """
        Transcribe YouTube video for FREE
        Args:
            url_or_video_id: YouTube URL or video ID
            language: Optional language code
            cookies_file: Optional cookies.txt path
        Returns:
            dict with transcript and instructions for GitHub Copilot
        """
        # Parse video ID
        if url_or_video_id.startswith('http'):
            scraper = YouTubeURLScraper()
            self.video_id = scraper.extract_video_id(url_or_video_id)
            url = scraper.get_standard_url()
        else:
            self.video_id = url_or_video_id
            url = f"https://www.youtube.com/watch?v={url_or_video_id}"
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        audio_file = os.path.join(temp_dir, f"{self.video_id}.mp3")
        
        try:
            # Download audio
            print(f"Downloading audio from: {url}")
            
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
                'extractor_args': {'youtube': {'player_client': ['android']}},
            }
            
            # Add cookies if provided
            if cookies_file and os.path.exists(cookies_file):
                ydl_opts['cookiefile'] = cookies_file
            elif os.path.exists('cookies.txt'):
                ydl_opts['cookiefile'] = 'cookies.txt'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            print("Audio downloaded. Transcribing with local Whisper...")
            
            # Transcribe with local Whisper (FREE!)
            transcript = self.whisper.transcribe(audio_file, language=language)
            
            # Cleanup
            if os.path.exists(audio_file):
                os.remove(audio_file)
            os.rmdir(temp_dir)
            
            # Return transcript with Copilot instructions
            return {
                'video_id': self.video_id,
                'transcript': transcript,
                'length': len(transcript),
                'copilot_prompt': self._generate_copilot_prompt(transcript),
                'instructions': self._get_instructions()
            }
            
        except Exception as e:
            # Cleanup on error
            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            raise Exception(f"Error: {e}")
    
    def _generate_copilot_prompt(self, transcript):
        """Generate a prompt to paste into GitHub Copilot Chat"""
        prompt = f"""Create study flashcards from this transcript in Q&A format.

TRANSCRIPT:
{transcript}

Generate 10-15 flashcards in this exact format:
Q: [Question about a key concept]
A: [Clear, concise answer]

Focus on main concepts, definitions, and important details."""
        return prompt
    
    def _get_instructions(self):
        """Instructions for using GitHub Copilot"""
        return """
HOW TO GENERATE FLASHCARDS (100% FREE):

1. Copy the 'copilot_prompt' text above
2. Open GitHub Copilot Chat in VS Code (Ctrl+Shift+I or Cmd+Shift+I)
3. Paste the prompt into Copilot Chat
4. Copilot will generate flashcards using GPT-4 (free with your student account!)
5. Copy the flashcards and save them

ALTERNATIVE: Run the full pipeline locally
- Use local Whisper (free) for transcription
- Use local TinyLlama (free) for flashcard generation
- Requires 2GB+ RAM but 100% free and automated
"""


def save_transcript(transcript_data, output_file):
    """Save transcript and Copilot prompt to file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"VIDEO: {transcript_data['video_id']}\n")
        f.write(f"TRANSCRIPT LENGTH: {transcript_data['length']} characters\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("TRANSCRIPT:\n")
        f.write("-" * 80 + "\n")
        f.write(transcript_data['transcript'])
        f.write("\n" + "-" * 80 + "\n\n")
        
        f.write("GITHUB COPILOT PROMPT (Copy & Paste into Copilot Chat):\n")
        f.write("=" * 80 + "\n")
        f.write(transcript_data['copilot_prompt'])
        f.write("\n" + "=" * 80 + "\n\n")
        
        f.write(transcript_data['instructions'])
    
    print(f"\n✓ Saved to: {output_file}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python free_transcriber.py <youtube_url> [language]")
        print("\nExample:")
        print("  python free_transcriber.py https://youtube.com/watch?v=dQw4w9WgXcQ")
        print("  python free_transcriber.py dQw4w9WgXcQ en")
        sys.exit(1)
    
    url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Transcribe
    transcriber = FreeTranscriber(model_size='base')
    result = transcriber.transcribe_video(url, language=language)
    
    # Save to file
    output_file = f"transcript_{result['video_id']}.txt"
    save_transcript(result, output_file)
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print(f"1. Open {output_file}")
    print("2. Copy the 'GITHUB COPILOT PROMPT' section")
    print("3. Paste into GitHub Copilot Chat in VS Code")
    print("4. Copilot will generate flashcards using GPT-4 for FREE!")
    print("=" * 80)
