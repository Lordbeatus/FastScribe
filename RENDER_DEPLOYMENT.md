# Render Deployment Guide

## Setting Up YouTube Cookies on Render

YouTube's bot detection requires cookie authentication for the production server. Here's how to set it up:

### Step 1: Export Cookies Locally

1. Install the **"Get cookies.txt LOCALLY"** browser extension:
   - [Chrome Web Store](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Go to [youtube.com](https://youtube.com) and log in to your account

3. Click the extension icon and export cookies for youtube.com

4. Save the exported file as `cookies.txt`

### Step 2: Upload Cookies to Render

You have two options:

#### Option A: Environment Variable (Recommended for Small Files)

1. Base64 encode your cookies file:
   ```bash
   # On Windows PowerShell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("cookies.txt")) | Out-File cookies_base64.txt
   
   # On Linux/Mac
   base64 cookies.txt > cookies_base64.txt
   ```

2. In Render Dashboard:
   - Go to your `fastscribe-api` service
   - Navigate to **Environment** tab
   - Add new environment variable:
     - Key: `YOUTUBE_COOKIES_BASE64`
     - Value: (paste the base64 encoded content)

3. Update `backend/app.py` to decode and use cookies (see code below)

#### Option B: Secret Files (Recommended for Larger Files)

1. In Render Dashboard:
   - Go to your `fastscribe-api` service
   - Navigate to **Environment** tab
   - Scroll to **Secret Files** section
   - Click **Add Secret File**
   - Filename: `cookies.txt`
   - Contents: (paste your cookies.txt content)

2. The file will be available at `/etc/secrets/cookies.txt` in production

3. Update your code to use this path (see code below)

### Step 3: Update Backend Code

Add this to the top of `backend/app.py`:

```python
import base64

# Setup cookies for production
COOKIES_PATH = None

if os.getenv('YOUTUBE_COOKIES_BASE64'):
    # Decode base64 cookies from environment variable
    cookies_b64 = os.getenv('YOUTUBE_COOKIES_BASE64')
    cookies_data = base64.b64decode(cookies_b64).decode('utf-8')
    
    # Write to temp file
    temp_cookies = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_cookies.write(cookies_data)
    temp_cookies.close()
    COOKIES_PATH = temp_cookies.name
    print(f"✓ Using cookies from environment variable")

elif os.path.exists('/etc/secrets/cookies.txt'):
    # Use Render secret file
    COOKIES_PATH = '/etc/secrets/cookies.txt'
    print(f"✓ Using cookies from secret file")

elif os.path.exists('cookies.txt'):
    # Use local cookies.txt for development
    COOKIES_PATH = 'cookies.txt'
    print(f"✓ Using local cookies.txt")

else:
    print("⚠ Warning: No cookies configured - YouTube downloads may fail")
```

Then update the transcribe endpoint to use cookies:

```python
@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    # ... existing code ...
    
    # Use production cookies if available
    cookies_from_browser = data.get('cookies_from_browser')
    cookies_file = COOKIES_PATH if COOKIES_PATH else data.get('cookies_file')
    
    transcript = transcriber.get_transcript(
        video_id,
        language=language,
        cookies_from_browser=cookies_from_browser,
        cookies_file=cookies_file  # Use the production cookies path
    )
```

### Step 4: Redeploy

```bash
git add -A
git commit -m "Add YouTube cookie support for Render"
git push origin main
```

Render will automatically redeploy with the new environment variables or secret files.

### Step 5: Verify

1. Check the Render logs for the cookie confirmation message:
   ```
   ✓ Using cookies from environment variable
   ```
   or
   ```
   ✓ Using cookies from secret file
   ```

2. Test a video transcription through the API

### Cookie Maintenance

YouTube cookies typically expire after several weeks or months. If downloads start failing:

1. Re-export cookies from your browser
2. Update the environment variable or secret file in Render
3. Redeploy (automatic for secret files, manual restart for env vars)

### Security Notes

- **Never commit cookies.txt to git** (already in .gitignore)
- Use a dedicated YouTube account for the API (not your personal account)
- Rotate cookies periodically for security
- Monitor Render logs for authentication failures

### Troubleshooting

**Error: "Sign in to confirm you're not a bot"**
- Your cookies have expired - re-export from browser
- Make sure you're logged into YouTube when exporting cookies

**Error: "Unable to extract video data"**
- Cookies may not be formatted correctly
- Ensure cookies.txt is in Netscape format
- Try exporting cookies again using the browser extension

**Cookies not being used**
- Check Render logs for cookie confirmation message
- Verify environment variable or secret file is set correctly
- Ensure the path `/etc/secrets/cookies.txt` is correct for secret files
