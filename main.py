"""
Main Pipeline: YouTube to Anki Flashcards
Complete workflow from YouTube URL to Anki cards and Google Docs
"""

import os
import sys
from urlScraper import YouTubeURLScraper
from transcriber import YouTubeTranscriber
from createNotes import NotesCreator
from formatNotes import NotesFormatter


def run_full_pipeline(youtube_url, export_to_google_docs=False):
    """
    Complete pipeline from YouTube to Anki
    Args:
        youtube_url: YouTube video URL
        export_to_google_docs: Whether to export to Google Docs
    """
    print("=" * 60)
    print("YouTube to Anki Flashcards Pipeline")
    print("=" * 60)
    
    # Step 1: Validate and extract video ID
    print("\n[1/5] Processing YouTube URL...")
    scraper = YouTubeURLScraper()
    try:
        video_id = scraper.extract_video_id(youtube_url)
        print(f"✓ Video ID: {video_id}")
        print(f"✓ Standard URL: {scraper.get_standard_url()}")
    except ValueError as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 2: Get transcript
    print("\n[2/5] Downloading and transcribing audio with Whisper...")
    transcriber = YouTubeTranscriber()
    try:
        formatted_transcript = transcriber.get_transcript(video_id)
        transcriber.save_transcript(f"transcript_{video_id}.txt")
        print(f"✓ Transcription complete")
        print(f"✓ Preview: {formatted_transcript[:150]}...")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 3: Create notes with GPT
    print("\n[3/5] Creating flashcards with GPT...")
    try:
        creator = NotesCreator()
        notes = creator.create_notes(formatted_transcript, style="flashcards")
        creator.save_notes(f"notes_{video_id}.txt")
        print(f"✓ Flashcards created")
        print(f"✓ Preview:\n{notes[:300]}...")
    except Exception as e:
        print(f"✗ Error: {e}")
        print("Make sure OPENAI_API_KEY environment variable is set")
        return
    
    # Step 4: Format for Anki
    print("\n[4/5] Formatting for Anki...")
    formatter = NotesFormatter()
    try:
        flashcards = formatter.parse_flashcards(notes)
        print(f"✓ Parsed {len(flashcards)} flashcards")
        
        # Export to both CSV and TXT
        csv_file = formatter.export_to_anki_csv(f"anki_{video_id}.csv")
        txt_file = formatter.export_to_anki_txt(f"anki_{video_id}.txt")
        print(f"✓ Exported to {csv_file} and {txt_file}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 5: Export to Google Docs (optional)
    if export_to_google_docs:
        print("\n[5/5] Exporting to Google Docs...")
        try:
            formatter.setup_google_docs_auth('credentials.json')
            doc_url = formatter.export_to_google_docs(notes, f"YouTube Notes - {video_id}")
            print(f"✓ Exported to Google Docs: {doc_url}")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print("\n[5/5] Skipping Google Docs export")
    
    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print("=" * 60)
    print(f"\nGenerated files:")
    print(f"  - transcript_{video_id}.txt")
    print(f"  - notes_{video_id}.txt")
    print(f"  - anki_{video_id}.csv (import to Anki)")
    print(f"  - anki_{video_id}.txt (alternative format)")


def main():
    """Main entry point"""
    print("YouTube to Anki Flashcards Generator")
    print("-" * 40)
    
    # Get YouTube URL from user or command line
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter YouTube URL: ").strip()
    
    if not url:
        print("Error: No URL provided")
        return
    
    # Ask about Google Docs export
    google_docs = input("Export to Google Docs? (y/n): ").strip().lower() == 'y'
    
    # Run pipeline
    run_full_pipeline(url, export_to_google_docs=google_docs)


if __name__ == "__main__":
    main()
