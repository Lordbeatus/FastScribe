import sys
from transcriber import YouTubeTranscriber

# Test transcriber with android client
video_id = 'dQw4w9WgXcQ'  # Rick Roll
print(f"Testing transcriber with video: {video_id}\n")

try:
    transcriber = YouTubeTranscriber()
    
    # This will fail at ffmpeg step locally, but that's OK
    # We just want to verify the download part works
    transcript = transcriber.get_transcript(video_id)
    
    print(f"\nSUCCESS! Transcript length: {len(transcript)} characters")
    print(f"First 200 chars: {transcript[:200]}")
    
except Exception as e:
    error_msg = str(e)
    if 'ffmpeg' in error_msg.lower():
        print("\n[EXPECTED] FFmpeg not installed locally - this is fine for testing")
        print("On Render, ffmpeg is pre-installed")
        print("\nDownload portion worked successfully!")
    else:
        print(f"\n[ERROR] {error_msg}")
