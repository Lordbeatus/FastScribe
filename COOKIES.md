# YouTube Cookie Authentication for FastScribe

If you're getting "Sign in to confirm you're not a bot" errors, you need to provide YouTube cookies.

## Quick Setup (Recommended)

### Option 1: Use Browser Cookies Directly

The easiest method - FastScribe can extract cookies directly from your browser:

1. Make sure you're logged into YouTube in your browser
2. Set environment variable:
   ```bash
   # Windows PowerShell
   $env:YOUTUBE_COOKIES_BROWSER="chrome"
   
   # Linux/Mac
   export YOUTUBE_COOKIES_BROWSER="chrome"
   ```
   
   Supported browsers: `chrome`, `firefox`, `edge`, `safari`, `opera`, `brave`

3. Restart the server - cookies will be extracted automatically

### Option 2: Export Cookies to File

For production/server environments:

1. **Export cookies from your browser:**
   
   Using yt-dlp (simplest):
   ```bash
   yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```
   
   Or use a browser extension:
   - Chrome: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Save as `cookies.txt` in the project root**

3. The server will automatically use `cookies.txt` if it exists

## Format Requirements

The cookies file MUST be in Netscape format:
- First line: `# Netscape HTTP Cookie File` or `# HTTP Cookie File`
- Use correct line endings:
  - Windows: CRLF (`\r\n`)
  - Linux/Mac: LF (`\n`)

## Troubleshooting

**Error: HTTP 400 Bad Request**
- Wrong line endings in cookies file
- Convert line endings:
  ```bash
  # Linux/Mac
  dos2unix cookies.txt
  
  # Windows (PowerShell)
  (Get-Content cookies.txt) | Set-Content -NoNewline cookies.txt
  ```

**Error: Still getting bot detection**
- Cookies expired - re-export from browser
- Make sure you're logged into YouTube
- Try a different browser

## Security Notes

- Cookies file contains authentication for ALL sites you visit
- Keep `cookies.txt` private - add to `.gitignore`
- Never commit cookies to version control
- Rotate cookies periodically for security

## Programmatic Usage

```python
from transcriber import YouTubeTranscriber

# Use browser cookies
transcriber = YouTubeTranscriber()
transcript = transcriber.get_transcript(
    "https://youtube.com/watch?v=...",
    cookies_from_browser="chrome"
)

# Use cookies file
transcript = transcriber.get_transcript(
    "https://youtube.com/watch?v=...",
    cookies_file="path/to/cookies.txt"
)
```

## API Usage

```bash
# With browser cookies
curl -X POST http://localhost:5000/api/process-complete \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=...",
    "cookies_from_browser": "chrome"
  }'
```
