# Mac Server Setup - Complete Guide

Turn your 2019 MacBook Pro into a FREE Whisper + Copilot server.

**Performance**: 2-hour video in 6-9 minutes | **Cost**: ~$2-3/month electricity

---

## Quick Setup (Copy-Paste Commands)

```bash
# 1. Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install dependencies
brew install python@3.11 ffmpeg ngrok

# 3. Clone FastScribe
cd ~
git clone https://github.com/Lordbeatus/FastScribe.git
cd FastScribe

# 4. Install Python packages
cd home-server
pip3 install -r requirements.txt

# 5. Install Copilot API
cd ~/FastScribe/copilot-api
pip3 install -r requirements.txt

# Done! Now start the servers ↓
```

---

## Running the Servers

### Terminal 1: Whisper Server
```bash
cd ~/FastScribe/home-server
python3 whisper_server.py
```
Should see: `✅ Whisper model loaded and ready!`

### Terminal 2: Copilot API Server
```bash
cd ~/FastScribe/copilot-api
python3 api.py 8080
```
**First time**: Opens browser → Login to GitHub → Enter code → Authorize

### Terminal 3: Ngrok Tunnel (Expose to Internet)
```bash
# Get free account at https://ngrok.com/signup
# Get auth token from https://dashboard.ngrok.com/get-started/your-authtoken

ngrok config add-authtoken YOUR_TOKEN_HERE
ngrok http 8000
```
**Copy the URL** like `https://abc123.ngrok-free.app`

---

## Test It Works

```bash
# Test Whisper
curl http://localhost:8000/health

# Test Copilot
curl -X POST http://localhost:8080/api \
  -H "Content-Type: application/json" \
  -d '{"prompt":"# hello world\ndef ","language":"python"}'
```

---

## Connect to Render

1. Go to Render dashboard → Your FastScribe service
2. **Environment** tab → Add:
   - `WHISPER_API_URL` = `https://your-ngrok-url.ngrok-free.app`
   - `COPILOT_API_URL` = Keep `http://localhost:8080/api` (or your deployed URL)
3. Save → Render redeploys

---

## Keep Running 24/7

### Simple Way: Use `screen`

```bash
# Whisper server
screen -S whisper
cd ~/FastScribe/home-server
python3 whisper_server.py
# Press Ctrl+A then D to detach

# Copilot server
screen -S copilot
cd ~/FastScribe/copilot-api
python3 api.py 8080
# Press Ctrl+A then D to detach

# Ngrok tunnel
screen -S ngrok
ngrok http 8000
# Press Ctrl+A then D to detach

# Reattach anytime with: screen -r whisper (or copilot/ngrok)
```

---

## Troubleshooting

**Port already in use:**
```bash
lsof -i :8000  # Find process
kill -9 PID    # Kill it
```

**Ngrok disconnects:**
- Free tier = 2-hour sessions
- Just restart: `ngrok http 8000`
- Update new URL in Render environment variables

**Mac sleeps:**
System Preferences → Energy Saver → Prevent sleep when display off

**Model loading slow:**
- First time downloads 74MB (30-60 seconds)
- After that: loads in 5-10 seconds

---

## What This Does

1. **Whisper Server** (port 8000) = Free transcription
2. **Copilot API** (port 8080) = Free GPT-4 flashcard generation
3. **Ngrok** = Exposes Mac to internet for Render to access

**Total cost**: ~$2-3/month electricity vs $8-15/month APIs 💰

---

## Performance

- **10-min video**: 1-2 minutes
- **1-hour video**: 6-10 minutes  
- **2-hour video**: 6-9 minutes (fast mode) or 8-12 minutes (base)

Add WebSocket progress bars so users don't just stare at loading screen!
