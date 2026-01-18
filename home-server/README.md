# 🏠 Home Whisper Server Setup

Run Whisper on your old computer at home for **100% free transcription**!

## 💰 Cost: $0/month (just electricity)

## 📋 Prerequisites

### Old Computer Specs
- **RAM:** 4GB minimum (8GB better)
- **Storage:** 5GB free
- **CPU:** Any modern CPU (2010+)
- **OS:** Windows, Mac, or Linux
- **Internet:** Stable connection

## 🚀 Setup (15 minutes)

### Step 1: Install Python

**Windows:**
```bash
# Download from python.org or use winget
winget install Python.Python.3.11
```

**Mac:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt install python3.11 python3-pip
```

### Step 2: Install Dependencies

```bash
cd home-server
pip install -r requirements.txt
```

**This will install:**
- Flask (web server)
- OpenAI Whisper (transcription)
- PyTorch (~2GB download, be patient!)

### Step 3: Test Locally

```bash
python whisper_server.py
```

You should see:
```
Loading Whisper model (this takes a moment)...
✅ Whisper model loaded and ready!
🚀 Starting Whisper API server on port 8000
```

Test it:
```bash
curl http://localhost:8000/health
```

### Step 4: Expose to Internet

You need to make your home server accessible from Render. **3 options:**

---

## Option A: Ngrok (Easiest, Free)

### Install Ngrok
1. Go to https://ngrok.com/download
2. Sign up (free)
3. Download ngrok
4. Get your auth token from dashboard

### Setup
```bash
# Authenticate (one time)
ngrok config add-authtoken YOUR_TOKEN

# Start tunnel
ngrok http 8000
```

You'll get a URL like:
```
https://abc123.ngrok-free.app → http://localhost:8000
```

**Pros:**
- ✅ Super easy (2 commands)
- ✅ Works behind any firewall/router
- ✅ HTTPS automatically

**Cons:**
- ⚠️ URL changes every restart (free tier)
- ⚠️ 40 requests/minute limit (free tier)

**For FastScribe:** Use the ngrok URL as `WHISPER_API_URL` on Render

---

## Option B: Cloudflare Tunnel (Best for 24/7)

### Install Cloudflared
```bash
# Windows
winget install Cloudflare.cloudflared

# Mac
brew install cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### Setup
```bash
# Login (opens browser)
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create whisper-api

# Note the tunnel ID from output

# Create config file
cat > ~/.cloudflared/config.yml << EOF
tunnel: YOUR_TUNNEL_ID
credentials-file: ~/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: whisper.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
EOF

# Run tunnel
cloudflared tunnel run whisper-api
```

**Pros:**
- ✅ Permanent URL
- ✅ No rate limits
- ✅ Very reliable
- ✅ HTTPS automatically

**Cons:**
- ⚠️ Slightly more setup
- ⚠️ Need a domain (free via Cloudflare)

---

## Option C: Port Forwarding (Advanced)

**Only if you:**
- Can access your router settings
- Have a static IP or dynamic DNS
- Understand networking

**Steps:**
1. Find your computer's local IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Log into router (usually 192.168.1.1)
3. Forward external port 8000 → your computer's IP:8000
4. Get your public IP: https://whatismyip.com
5. Use http://YOUR_PUBLIC_IP:8000

**⚠️ Security:** This exposes your computer to internet. Add authentication!

---

## 🔧 Running 24/7

### Windows - Run as Service

Create `start_whisper.bat`:
```batch
@echo off
cd /d C:\path\to\home-server
python whisper_server.py
pause
```

Use Task Scheduler to run on startup.

### Linux - Systemd Service

Create `/etc/systemd/system/whisper.service`:
```ini
[Unit]
Description=Whisper API Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/home-server
ExecStart=/usr/bin/python3 whisper_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable whisper
sudo systemctl start whisper
```

### Mac - LaunchAgent

Create `~/Library/LaunchAgents/com.whisper.api.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.whisper.api</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/whisper_server.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.whisper.api.plist
```

---

## 🔗 Integrate with Render

### Update Render Environment

Add environment variable on Render:
```
WHISPER_API_URL=https://your-ngrok-or-cloudflare-url.com
```

### Update Flask App (on Render)

The app will check for `WHISPER_API_URL` and use your home server instead of OpenAI API!

---

## 💡 Cost Analysis

### Home Server (This Approach)
- **Hardware:** Old computer (already have)
- **Electricity:** ~$2-5/month (50W computer)
- **Internet:** $0 (existing connection)
- **Ngrok/Cloudflare:** $0 (free tier)
- **Total:** **~$2-5/month**

### Alternative Costs
- OpenAI Whisper API: $8-15/month
- Render Standard + Local Whisper: $25/month
- **Home server wins!** 🏆

---

## 🧪 Testing

### Test Health
```bash
curl https://your-url.com/health
```

### Test Transcription
```bash
curl -X POST https://your-url.com/transcribe \
  -F "file=@test.mp3" \
  -F "language=en"
```

---

## 🐛 Troubleshooting

### "Model loading failed"
- Need more RAM (close other programs)
- Use smaller model: `whisper.load_model("tiny")` (39MB)

### "Connection refused"
- Check firewall (allow port 8000)
- Ngrok/Cloudflare running?
- Whisper server running?

### "Out of memory"
- Use tiny model instead of base
- Close other programs
- Add swap space (Linux)

### Slow transcription
- Normal on CPU (1-2 min for 10 min video)
- Consider base model (balanced)
- Or tiny model (faster, less accurate)

---

## 📊 Performance

**On typical old computer:**
- **Tiny model:** 30-60 seconds for 10-min video
- **Base model:** 1-2 minutes for 10-min video
- **Small model:** 3-5 minutes for 10-min video

**Recommendation:** Start with **base** - good balance!

---

## 🎯 Recommended Setup

1. **Home Server:** Whisper on old computer with **Ngrok**
2. **Render:** Flask app + Copilot API (free tier)
3. **Total Cost:** **~$2/month** (just electricity!)

This gives you:
- ✅ Free transcription (home Whisper)
- ✅ Free flashcards (Copilot API)
- ✅ Free hosting (Render)
- ✅ **100% functional system for $2/month!**

---

## 🔐 Security Notes

- Ngrok/Cloudflare provide HTTPS automatically
- Consider adding API key authentication to whisper_server.py
- Don't expose your home computer's ports directly (use tunnels)
- Keep Whisper server updated

---

## 🚀 Next Steps

1. Set up Whisper server on old computer
2. Choose tunnel option (Ngrok recommended for start)
3. Update Render with `WHISPER_API_URL`
4. Test end-to-end!

**Your old computer just became a free AI transcription service!** 🎉
