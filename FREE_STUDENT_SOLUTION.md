# 100% FREE FastScribe Setup (Student Edition)

## Your Advantage: GitHub Copilot Pro (Free GPT-4!)

As a student with GitHub Copilot Pro, you have:
- ✅ Unlimited GPT-4 access through Copilot Chat
- ✅ Free local Whisper transcription
- ✅ Zero API costs!

## The Free Solution

### What Costs Money:
- ❌ OpenAI Whisper API: ~$0.006/minute
- ❌ OpenAI GPT-4 API: ~$0.02 per generation

### What's FREE:
- ✅ Local Whisper (open-source): $0
- ✅ GitHub Copilot GPT-4 (student): $0
- ✅ Render Free Tier: $0

## Setup (100% Free)

### Option 1: Semi-Automated (Recommended)

**How it works:**
1. Local Whisper transcribes video → FREE
2. Copy transcript to GitHub Copilot Chat → FREE GPT-4
3. Copilot generates flashcards → FREE
4. Copy flashcards to Anki → FREE

**Steps:**
```bash
cd backend

# Transcribe video (FREE)
python free_transcriber.py https://youtube.com/watch?v=VIDEO_ID

# Open the generated transcript_VIDEO_ID.txt
# Copy the "GITHUB COPILOT PROMPT" section
# Paste into VS Code Copilot Chat (Ctrl+Shift+I)
# Copilot will generate flashcards using GPT-4 for free!
```

**Pros:**
- 100% free
- Uses GPT-4 (better quality than local LLMs)
- Works on any computer

**Cons:**
- Manual copy-paste step
- Need VS Code open

### Option 2: Fully Automated Local

**How it works:**
1. Local Whisper transcribes → FREE
2. Local TinyLlama generates flashcards → FREE
3. Fully automated → FREE

**Requirements:**
- 2GB+ RAM
- 4-5GB disk space
- Render Standard plan ($25/mo) OR run on your computer

**Steps:**
```bash
cd backend
python hybrid_transcriber.py  # Auto-uses local models
```

**Pros:**
- Fully automated
- No manual steps

**Cons:**
- Lower quality flashcards (TinyLlama < GPT-4)
- Needs more resources
- Slow on CPU

### Option 3: GitHub Copilot Integration (Future)

We could potentially integrate with GitHub Copilot's API if available, making it fully automated while still free!

## My Recommendation for You

**Use Option 1 (Semi-Automated with Copilot Chat):**

1. Run local Whisper to transcribe (free)
2. Paste transcript into GitHub Copilot Chat
3. Get GPT-4 quality flashcards for free!

This gives you:
- Best of both worlds (free + GPT-4 quality)
- Runs on Render free tier
- One simple copy-paste step
- Better than local LLMs

## Cost Comparison

### Your Free Solution:
- Whisper transcription: $0 (local)
- Flashcard generation: $0 (Copilot)
- Hosting: $0 (Render free tier)
- **Total: $0 per month**

### If You Paid for APIs:
- Whisper: $6/mo (100 videos)
- GPT-4: $2/mo (100 videos)
- **Total: $8/mo**

### Local Everything:
- Render Standard: $25/mo
- Processing: $0
- **Total: $25/mo**

**You save $8-25/month with the free solution!**

## Installation

### For Local Whisper:
```bash
pip install openai-whisper

# For Windows, might need:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Dependencies:
- FFmpeg (already installed ✓)
- Python 3.8+ (have it ✓)
- ~2GB RAM for Whisper base model
- ~500MB disk for Whisper model

## Usage Example

```bash
# 1. Transcribe a video
python free_transcriber.py https://youtube.com/watch?v=dQw4w9WgXcQ

# 2. This creates: transcript_dQw4w9WgXcQ.txt
# 3. Open the file and copy the "COPILOT PROMPT" section
# 4. Open VS Code Copilot Chat (Ctrl+Shift+I)
# 5. Paste and hit enter
# 6. Copy the flashcards Copilot generates!
```

## Deploying to Render (Free Tier)

Since you're using local Whisper + manual Copilot Chat, you can run on the FREE tier:

```yaml
# render.yaml
services:
  - type: web
    name: fastscribe-free
    env: python
    buildCommand: cd backend && pip install openai-whisper yt-dlp flask flask-cors
    startCommand: cd backend && gunicorn app:app
```

Just update the app to use `FreeTranscriber` instead of the API-based one.

## Next Steps

1. Test locally: `python backend/free_transcriber.py VIDEO_URL`
2. Try pasting output into Copilot Chat
3. If it works well, we can update the web app to use this approach
4. Deploy to Render free tier

**Want me to help you test this now?**
