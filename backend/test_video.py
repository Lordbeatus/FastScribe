import yt_dlp
import sys

# Test with a known working video
test_videos = [
    ('zZ6vybT1HQs', 'User provided video'),
    ('dQw4w9WgXcQ', 'Rick Roll (known working)'),
]

for video_id, description in test_videos:
    url = f'https://youtube.com/watch?v={video_id}'
    
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print('='*60)
    
    # Try to extract info without downloading
    ydl_opts = {
        'quiet': True,
        'no_warnings': False,
        'extractor_args': {'youtube': {'player_client': ['android']}},  # Android doesn't need JS
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print("[OK] Video accessible")
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Duration: {info.get('duration', 'N/A')} seconds")
            print(f"Live: {info.get('is_live', False)}")
            print(f"Upcoming: {info.get('live_status') == 'is_upcoming'}")
            
            formats = info.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none']
            video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('vcodec') != 'images']
            
            print(f"\nFormats - Total: {len(formats)}, Audio: {len(audio_formats)}, Video: {len(video_formats)}")
            
            if audio_formats:
                print("\nSample audio formats:")
                for f in audio_formats[:3]:
                    print(f"  {f.get('format_id'):5s} - {f.get('ext'):4s} - {f.get('acodec'):10s} @ {f.get('abr', 0)}kbps")
            else:
                print("\n[WARNING] No audio formats found!")
                print("Available format types:")
                format_types = set([f.get('vcodec', 'unknown') for f in formats])
                for ft in format_types:
                    count = len([f for f in formats if f.get('vcodec') == ft])
                    print(f"  {ft}: {count} formats")
            
    except yt_dlp.utils.DownloadError as e:
        print(f"[ERROR] Download Error: {e}")
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

print(f"\n{'='*60}")
print("Test complete")
print('='*60)
