# 🎓 FastScribe - YouTube to Anki Flashcards

> Transform YouTube videos into Anki flashcards automatically. **FREE mode** for students with GitHub Copilot!

## 🌟 Features

- 🎬 **YouTube Integration** - Works with any YouTube video
- 🎙️ **Accurate Transcription** - Whisper API or local Whisper
- 🤖 **AI-Powered Flashcards** - GPT-4 via OpenAI API or GitHub Copilot (FREE!)
- 📚 **Anki Export** - Ready-to-import CSV format
- 🌐 **Web Interface** - User-friendly React frontend
- 🔒 **Secure** - API keys in environment variables only
- 💰 **Cost Options** - FREE mode ($0/month) or API mode (~$8-15/month)

## 💸 Two Modes

### FREE Mode (Recommended for Students)
- ✅ Local Whisper transcription ($0)
- ✅ GitHub Copilot API for flashcards ($0)
- ✅ Unlimited usage
- ✅ **Total: $0/month**
- ⚡ Requires GitHub Copilot Pro (free for students)

### API Mode (Faster)
- ✅ OpenAI Whisper API (~$0.006/min)
- ✅ OpenAI GPT-4 API (~$0.01-0.03/request)
- ✅ Faster processing
- ⚡ Requires OpenAI API key
- 💰 **Total: ~$8-15/month**

## 🚀 Quick Start

### Option 1: FREE Mode (Students)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lordbeatus/FastScribe.git
   cd FastScribe
   ```

2. **Get your Copilot token** (see [COPILOT_API_SETUP.md](COPILOT_API_SETUP.md))

3. **Deploy to Render** (see [QUICK_DEPLOY.md](QUICK_DEPLOY.md))
   - Add `COPILOT_TOKEN` environment variable
   - Push to GitHub
   - Auto-deploys!

### Option 2: API Mode

1. **Set up OpenAI API key**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

2. **Deploy to Render**
   - Add `OPENAI_API_KEY` environment variable
   - Push to GitHub

## 📁 Repository Structure

```
FastScribe/
├── backend/                    # Flask API server
│   ├── app.py                 # Main server (both modes)
│   ├── apiKeyCycler.py        # API key management
│   ├── copilot_flashcard_generator.py  # FREE mode
│   ├── local_whisper.py       # FREE mode transcription
│   ├── transcriber.py         # API mode transcription
│   ├── createNotes.py         # API mode flashcards
│   ├── formatNotes.py         # Anki formatting
│   └── urlScraper.py          # YouTube URL handling
├── frontend/                   # React web app
├── ARCHITECTURE.md            # System design & security
├── QUICK_DEPLOY.md            # Deployment guide
└── RENDER_COPILOT_SETUP.md    # Copilot setup guide
```

## 🔌 API Endpoints

### FREE Mode
- `POST /api/process-free` - Full pipeline using Copilot API ($0)

### API Mode
- `POST /api/process-complete` - Full pipeline using OpenAI APIs
- `POST /api/transcribe` - Transcribe only
- `POST /api/create-flashcards` - Generate flashcards only
- `POST /api/export-anki` - Format for Anki

### Utilities
- `POST /api/validate-url` - Validate YouTube URL
- `GET /` - Health check

## 🔐 Security

✅ **Your API key is safe!**

- All keys in **environment variables only**
- No hardcoded keys in code
- `.gitignore` prevents committing secrets
- Render encrypts environment variables

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete security review.

## 📖 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system design, security review, and how it works
- **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** - Deploy in 3 steps
- **[RENDER_COPILOT_SETUP.md](RENDER_COPILOT_SETUP.md)** - Detailed Copilot setup
- **[COPILOT_API_SETUP.md](COPILOT_API_SETUP.md)** - Local testing guide

## 🧪 Testing

### Test FREE Mode Locally
```bash
# Start copilot-api
cd copilot-api && python api.py 8080

# In new terminal, start Flask
cd backend && python app.py

# Test
curl -X POST http://localhost:5000/api/process-free \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=VIDEO_ID", "language": "English"}'
```

### Test on Render
```bash
curl -X POST https://fastscribe-4nzr.onrender.com/api/process-free \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=VIDEO_ID", "language": "English"}'
```

## 💰 Cost Breakdown

| Feature | FREE Mode | API Mode |
|---------|-----------|----------|
| Transcription | Local Whisper | OpenAI Whisper API |
| Flashcards | Copilot API | OpenAI GPT-4 |
| Per Video | $0.00 | ~$0.08 |
| 100 videos/month | **$0.00** | ~$8.00 |
| Hosting | Render Free | Render Free |
| **Total** | **$0.00/month** | **~$8-15/month** |

## 🎓 Perfect for Students

- ✅ 100% free with GitHub Copilot Pro (free for students)
- ✅ Unlimited flashcard generation
- ✅ No credit card required
- ✅ Cloud-hosted (accessible anywhere)
- ✅ Professional-grade GPT-4 quality

## 🤝 Contributing

Pull requests welcome! Please ensure:
- No hardcoded API keys
- Update documentation
- Test both FREE and API modes

## 📝 License

MIT License - Free to use for students and educators

---

**Made with ❤️ for students who want free, automated study tools!**

### Development Setup

```bash
# Backend
cd backend
pip install -r requirements-server.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## Deployment

Configured for Render deployment. See `render.yaml` for configuration details.

```bash
git push origin main
# Render auto-deploys both frontend and backend
```

Full deployment guide: [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

## Technology Stack

**Backend:**
- Flask - REST API
- yt-dlp - YouTube audio download
- OpenAI Whisper - Speech-to-text transcription
- OpenAI GPT-4 - Flashcard generation

**Frontend:**
- React - UI framework
- Tailwind CSS - Styling
- Axios - API communication

## License

MIT

