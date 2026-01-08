# 🏗️ FastScribe System Architecture

## Overview

FastScribe is a YouTube-to-Anki flashcard generator with **two processing modes**:

### 1. **FREE Mode** (Recommended for Students)
- Uses **local Whisper** for transcription ($0)
- Uses **GitHub Copilot API** for flashcard generation ($0)
- Total cost: **$0/month**

### 2. **API Mode** (Faster but costs money)
- Uses **OpenAI Whisper API** for transcription (~$0.006/minute)
- Uses **OpenAI GPT-4 API** for flashcard generation (~$0.01/request)
- Total cost: **~$8-15/month** depending on usage

---

## 🔐 Security Review

### ✅ SAFE for Cloud Hosting

Your API keys are properly handled:

1. **Environment Variables Only**: API keys are read from `OPENAI_API_KEY` or `COPILOT_TOKEN` environment variables
2. **Never Hardcoded**: No keys in source code (we removed the hardcoded keys)
3. **Not in Git**: `.gitignore` prevents committing sensitive files
4. **Render Secrets**: Keys stored securely in Render's environment variable system

### How It Works on Render

```
Render Environment Variables (Secure)
    ↓
Flask app reads from os.getenv()
    ↓
Uses keys for API calls
    ↓
Never exposes keys to users
```

**Your API key is safe** as long as you:
- ✅ Add it as an environment variable on Render (not in code)
- ✅ Never commit `.env` files to Git
- ✅ Don't expose API keys in logs or responses

---

## 📁 Clean Repository Structure

```
FastScribe/
├── backend/
│   ├── app.py                          # Main Flask server
│   ├── apiKeyCycler.py                 # Manages API key rotation (secure)
│   ├── copilot_flashcard_generator.py  # Copilot API integration
│   ├── createNotes.py                  # GPT-4 flashcard generation
│   ├── formatNotes.py                  # Flashcard formatting/parsing
│   ├── local_whisper.py                # Local Whisper transcription
│   ├── transcriber.py                  # YouTube audio download + Whisper API
│   ├── urlScraper.py                   # YouTube URL validation
│   ├── requirements-server.txt         # Production dependencies
│   └── cookies.txt                     # YouTube cookies (optional, gitignored)
│
├── frontend/                           # React web app
├── copilot-api/                        # GitHub Copilot API server (gitignored)
│
├── .env                                # Local environment variables (gitignored)
├── .gitignore                          # Prevents committing secrets
├── render.yaml                         # Render deployment config
├── start.sh                            # Startup script for Render
│
└── Documentation/
    ├── README.md                       # Main project overview
    ├── QUICK_DEPLOY.md                 # Quick deployment guide
    ├── RENDER_COPILOT_SETUP.md         # Detailed Copilot setup
    └── COPILOT_API_SETUP.md            # Local Copilot testing
```

---

## 🔄 How the System Works

### FREE Mode Flow (`/api/process-free`)

```
1. User submits YouTube URL
   ↓
2. urlScraper validates URL and extracts video ID
   ↓
3. yt-dlp downloads audio (mp3/m4a)
   ↓
4. local_whisper transcribes audio using Whisper base model
   ↓
5. copilot_flashcard_generator creates formatted prompt
   ↓
6. Sends prompt to localhost:8080/api (copilot-api)
   ↓
7. Copilot API uses your GitHub Copilot subscription (GPT-4)
   ↓
8. Returns flashcards in Q&A format
   ↓
9. formatNotes parses and formats for Anki
   ↓
10. Returns CSV file to user
```

**Cost: $0** (uses your free student Copilot account)

### API Mode Flow (`/api/process-complete`)

```
1. User submits YouTube URL
   ↓
2. urlScraper validates URL and extracts video ID
   ↓
3. transcriber.py downloads audio via yt-dlp
   ↓
4. Sends audio to OpenAI Whisper API for transcription
   ↓
5. createNotes.py sends transcript to GPT-4 API
   ↓
6. GPT-4 generates flashcards
   ↓
7. formatNotes parses and formats for Anki
   ↓
8. Returns CSV file to user
```

**Cost: ~$0.02-0.10 per video** (depending on length)

---

## 🧩 Component Breakdown

### Backend Components

#### `app.py` - Main Flask Server
- **Routes**:
  - `GET /` - Health check
  - `POST /api/validate-url` - Validate YouTube URL
  - `POST /api/transcribe` - Get transcript only
  - `POST /api/create-flashcards` - Generate flashcards from transcript
  - `POST /api/export-anki` - Format flashcards for Anki
  - `POST /api/process-complete` - Full pipeline (API mode)
  - `POST /api/process-free` - Full pipeline (FREE mode)
- **Security**: Reads API keys from environment variables only

#### `apiKeyCycler.py` - API Key Management
- **Purpose**: Rotates through multiple API keys if provided
- **Security**: 
  - Reads from `OPENAI_API_KEY` or `OPENAI_API_KEYS` env vars
  - Thread-safe key rotation
  - Never stores keys in code
- **Usage**: `get_next_api_key()` returns next key in rotation

#### `transcriber.py` - OpenAI Whisper API
- Downloads YouTube audio via `yt-dlp`
- Sends to OpenAI Whisper API for transcription
- Supports YouTube cookies for bot detection bypass
- Uses `apiKeyCycler` for API key

#### `local_whisper.py` - Local Whisper
- Runs Whisper model locally (no API)
- Model sizes: tiny, base, small, medium, large
- Uses PyTorch (CPU or GPU)
- Free but slower than API

#### `createNotes.py` - GPT-4 Flashcard Generation
- Sends transcript to GPT-4 API
- Generates flashcards in Q&A format
- Uses `apiKeyCycler` for API key

#### `copilot_flashcard_generator.py` - Copilot Integration
- Sends prompts to local copilot-api server
- Uses your GitHub Copilot subscription (free for students)
- Same quality as GPT-4
- Parses flashcards from response

#### `formatNotes.py` - Flashcard Formatting
- Parses flashcards from GPT output
- Formats for Anki CSV import
- Supports custom deck names

#### `urlScraper.py` - YouTube URL Validation
- Validates YouTube URLs
- Extracts video IDs
- Supports youtu.be, youtube.com/watch, embed URLs

---

## 🚀 Deployment on Render

### How `start.sh` Works

```bash
1. Check if copilot-api exists
   ↓
2. If not, clone from GitHub
   ↓
3. Check for COPILOT_TOKEN env var
   ↓
4. Create .copilot_token file from env var
   ↓
5. Start copilot-api on port 8080 (background)
   ↓
6. Wait 5 seconds for it to be ready
   ↓
7. Start Flask app with Gunicorn (foreground)
```

### Environment Variables Needed

**For FREE Mode:**
- `COPILOT_TOKEN` - Your GitHub Copilot access token
- `PORT` - Port for Flask app (set by Render)

**For API Mode (optional):**
- `OPENAI_API_KEY` - Your OpenAI API key
- Can use both modes simultaneously

**Optional:**
- `YOUTUBE_COOKIES_BASE64` - Base64-encoded YouTube cookies
- `FLASK_ENV` - Set to `production`

---

## 💰 Cost Comparison

| Component | FREE Mode | API Mode |
|-----------|-----------|----------|
| **Transcription** | Local Whisper (free) | Whisper API ($0.006/min) |
| **Flashcards** | Copilot API (free) | GPT-4 API ($0.01-0.03/request) |
| **Hosting** | Render Free Tier | Render Free Tier |
| **Total/month** | **$0** | **$8-15** |

### Example Costs (API Mode)

- 10-min video: ~$0.06 transcription + ~$0.02 flashcards = **$0.08**
- 100 videos/month: **~$8.00**

### FREE Mode

- Unlimited videos
- **$0.00 forever**
- Requires GitHub Copilot Pro (free for students)

---

## 🔒 Security Best Practices

### ✅ What We Do Right

1. **Environment Variables**: All secrets in env vars, never in code
2. **Git Ignore**: `.env`, `cookies.txt`, `.copilot_token` are gitignored
3. **No Hardcoding**: Removed all hardcoded API keys
4. **Secure Storage**: Render encrypts environment variables
5. **Thread Safety**: API key cycler is thread-safe

### ⚠️ Important Reminders

1. **Never commit API keys** to Git
2. **Rotate keys** if accidentally exposed
3. **Monitor usage** on OpenAI dashboard
4. **Set spending limits** on OpenAI account
5. **Use .env locally**, environment variables on Render

### How to Check Security

```bash
# Never commit these files
git status
# Should NOT show:
# - .env
# - cookies.txt
# - .copilot_token

# Check for hardcoded keys
grep -r "sk-proj-" backend/
grep -r "sk-" backend/
# Should return nothing!
```

---

## 🧪 Testing

### Local Testing (FREE Mode)

```bash
# 1. Start copilot-api
cd copilot-api
python api.py 8080

# 2. In new terminal, start Flask
cd backend
python app.py

# 3. Test the endpoint
curl -X POST http://localhost:5000/api/process-free \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=VIDEO_ID", "language": "English"}'
```

### Production Testing (Render)

```bash
curl -X POST https://fastscribe-4nzr.onrender.com/api/process-free \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=VIDEO_ID", "language": "English"}'
```

---

## 🐛 Common Issues

### "No API keys provided"
- **Cause**: Missing `OPENAI_API_KEY` environment variable
- **Fix**: Add key to Render environment variables or use FREE mode

### "Could not connect to Copilot API"
- **Cause**: copilot-api server not running
- **Fix**: Check `start.sh` logs, ensure `COPILOT_TOKEN` is set

### "Only images available for download"
- **Cause**: YouTube bot detection
- **Fix**: Add YouTube cookies (see `RENDER_COPILOT_SETUP.md`)

### "Read-only file system"
- **Cause**: Render secret files are immutable
- **Fix**: `start.sh` already copies to temp location

---

## 📊 Monitoring

### Check System Health

```bash
# Health check
curl https://fastscribe-4nzr.onrender.com/

# Should return:
# {"status": "healthy", "service": "FastScribe API"}
```

### Monitor Costs (API Mode)

1. Go to https://platform.openai.com/usage
2. Check daily usage
3. Set spending limits in Account Settings

### Monitor Render

1. Dashboard: https://dashboard.render.com
2. View logs in real-time
3. Check deployment status

---

## 🎓 For Students

This system is designed to be:
- ✅ **Free** - No monthly costs with FREE mode
- ✅ **Secure** - No exposed API keys
- ✅ **Scalable** - Can handle many requests
- ✅ **Educational** - Learn Flask, APIs, deployment

Perfect for creating study materials without spending money!

---

## 📚 Next Steps

1. ✅ Clean repository (done!)
2. ✅ Review security (done!)
3. ⬜ Add your `COPILOT_TOKEN` to Render
4. ⬜ Test the `/api/process-free` endpoint
5. ⬜ Create some flashcards!

**Your system is now clean, secure, and ready for production!** 🚀
