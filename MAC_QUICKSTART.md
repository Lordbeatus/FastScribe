# Mac Setup - Quick Start

## 1. One-Time Setup

```bash
# Clone repo
cd ~
git clone https://github.com/Lordbeatus/FastScribe.git
cd FastScribe

# Install dependencies
brew install python@3.11 ffmpeg ngrok

# Install Python packages
cd home-server && pip3 install -r requirements.txt && cd ..
cd copilot-api && pip3 install -r requirements.txt && cd ..

# Make scripts executable
chmod +x start_mac_server.sh stop_mac_server.sh

# Setup ngrok
ngrok config add-authtoken YOUR_TOKEN_HERE
```

## 2. Start Servers

```bash
cd ~/FastScribe
./start_mac_server.sh
```

This starts:
- ✅ Whisper on port 8000
- ✅ Copilot on port 8080

## 3. Expose to Internet

```bash
ngrok http 8000
```

Copy the URL (e.g., `https://abc123.ngrok-free.app`)

## 4. Update Render

Render Dashboard → Environment → Add:
- `WHISPER_API_URL` = your ngrok URL

## Stop Servers

```bash
cd ~/FastScribe
./stop_mac_server.sh
```

## Logs

```bash
tail -f ~/FastScribe/logs/whisper.log
tail -f ~/FastScribe/logs/copilot.log
```

---

**Full guide:** [MACOS_SERVER_SETUP.md](MACOS_SERVER_SETUP.md)
