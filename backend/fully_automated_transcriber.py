"""
Fully Automated Free Transcription Pipeline
Uses local Whisper + GitHub Copilot API for 100% automated, free processing
"""

import os
import sys
from local_whisper import LocalWhisperTranscriber
from copilot_flashcard_generator import CopilotFlashcardGenerator
from urlScraper import is_valid_youtube_url, download_audio


class FullyAutomatedTranscriber:
    """Fully automated pipeline: Video → Transcript → Flashcards"""
    
    def __init__(self, whisper_model="base", copilot_api_url="http://localhost:8080/api"):
        """
        Initialize the fully automated transcriber
        
        Args:
            whisper_model: Whisper model size (tiny/base/small/medium/large)
            copilot_api_url: URL of the copilot-api server
        """
        self.whisper = LocalWhisperTranscriber(model_size=whisper_model)
        self.copilot = CopilotFlashcardGenerator(copilot_api_url=copilot_api_url)
    
    def process_video(self, video_url, language="English", save_dir="output"):
        """
        Fully automated processing: Download → Transcribe → Generate Flashcards
        
        Args:
            video_url: YouTube video URL
            language: Language of the video content
            save_dir: Directory to save output files
            
        Returns:
            Dictionary with paths to all generated files
        """
        # Validate URL
        if not is_valid_youtube_url(video_url):
            raise ValueError(f"Invalid YouTube URL: {video_url}")
        
        print(f"🎬 Processing video: {video_url}")
        print(f"🗣️  Language: {language}")
        print(f"📁 Output directory: {save_dir}")
        print()
        
        # Create output directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Step 1: Download audio
        print("⬇️  Step 1/3: Downloading audio...")
        try:
            audio_path = download_audio(video_url, output_dir=save_dir)
            print(f"✅ Audio downloaded: {audio_path}")
        except Exception as e:
            raise Exception(f"Failed to download audio: {str(e)}")
        
        # Step 2: Transcribe with local Whisper
        print("\n🎙️  Step 2/3: Transcribing with local Whisper...")
        try:
            # Detect language code (Whisper uses 2-letter codes)
            lang_code = self._language_to_code(language)
            transcript = self.whisper.transcribe(audio_path, language=lang_code)
            
            # Save transcript
            transcript_path = os.path.join(save_dir, "transcript.txt")
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            
            print(f"✅ Transcription complete ({len(transcript)} characters)")
            print(f"💾 Saved to: {transcript_path}")
        except Exception as e:
            raise Exception(f"Failed to transcribe: {str(e)}")
        
        # Step 3: Generate flashcards with Copilot API
        print("\n🤖 Step 3/3: Generating flashcards with GitHub Copilot...")
        try:
            flashcards = self.copilot.generate_flashcards(transcript, language=language)
            
            # Save flashcards as Anki CSV
            anki_csv = self.copilot.format_for_anki(flashcards)
            flashcards_path = os.path.join(save_dir, "flashcards.csv")
            with open(flashcards_path, 'w', encoding='utf-8') as f:
                f.write(anki_csv)
            
            print(f"✅ Generated {len(flashcards)} flashcards")
            print(f"💾 Saved to: {flashcards_path}")
        except Exception as e:
            raise Exception(f"Failed to generate flashcards: {str(e)}")
        
        # Cleanup: Delete audio file to save space
        try:
            os.remove(audio_path)
            print(f"\n🗑️  Cleaned up audio file")
        except:
            pass
        
        # Return all file paths
        result = {
            'transcript_path': transcript_path,
            'flashcards_path': flashcards_path,
            'transcript': transcript,
            'flashcards': flashcards,
            'flashcard_count': len(flashcards)
        }
        
        print("\n" + "="*60)
        print("✨ Processing complete!")
        print("="*60)
        
        return result
    
    def _language_to_code(self, language):
        """Convert language name to Whisper language code"""
        language_map = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Chinese': 'zh',
            'Arabic': 'ar',
            'Hindi': 'hi',
            'Dutch': 'nl',
            'Polish': 'pl',
            'Turkish': 'tr',
            'Vietnamese': 'vi',
            'Indonesian': 'id',
            'Thai': 'th',
            'Swedish': 'sv',
            'Danish': 'da'
        }
        return language_map.get(language, 'en')


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("Fully Automated Free YouTube → Anki Flashcard Pipeline")
        print("=" * 60)
        print("\nUsage: python fully_automated_transcriber.py <video_url> [language]")
        print("\nExample:")
        print("  python fully_automated_transcriber.py https://youtube.com/watch?v=VIDEO_ID English")
        print("\nPrerequisites:")
        print("  1. Install dependencies:")
        print("     pip install openai-whisper torch yt-dlp")
        print()
        print("  2. Start copilot-api server:")
        print("     git clone https://github.com/B00TK1D/copilot-api.git")
        print("     cd copilot-api")
        print("     pip install -r requirements.txt")
        print("     python api.py 8080")
        print()
        print("  3. Authenticate with GitHub Copilot (first time only)")
        print("     - The copilot-api will prompt you to visit a URL")
        print("     - Enter the code to authenticate with your GitHub account")
        print("     - Your student Copilot subscription will be used (FREE!)")
        print()
        sys.exit(1)
    
    video_url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "English"
    
    # Initialize transcriber
    transcriber = FullyAutomatedTranscriber(whisper_model="base")
    
    try:
        # Process video
        result = transcriber.process_video(video_url, language=language)
        
        # Display results
        print(f"\n📊 Results:")
        print(f"   Transcript: {result['transcript_path']}")
        print(f"   Flashcards: {result['flashcards_path']}")
        print(f"   Total flashcards: {result['flashcard_count']}")
        
        print("\n📚 Next steps:")
        print("   1. Open Anki")
        print("   2. File → Import")
        print(f"   3. Select: {result['flashcards_path']}")
        print("   4. Set Field separator: Comma")
        print("   5. Click Import")
        print("\n✨ Done! Happy studying!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
