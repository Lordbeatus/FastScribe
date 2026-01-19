# Ubuntu Server Setup - Quick Start

## 1. One-Time Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Check Python version (Ubuntu comes with Python 3)
python3 --version

# Install pip, ffmpeg, and Python dev tools
sudo apt install -y python3-pip python3-dev python3-venv ffmpeg build-essential

# If you want Python 3.11 specifically (optional - system Python works fine):
# sudo apt install -y software-properties-common
# sudo add-apt-repository ppa:deadsnakes/ppa -y
# sudo apt update
# sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Clone repo
cd ~
git clone https://github.com/Lordbeatus/FastScribe.git
cd FastScribe

# Create virtual environment (fixes "externally managed" error)
python3 -m venv venv
source venv/bin/activate

# Install Python packages for Whisper
cd home-server
pip install -r requirements.txt
cd ..

# Install Python packages for Copilot API
cd copilot-api
pip install -r requirements.txt
cd ..

# Install ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Setup ngrok auth (get token from https://dashboard.ngrok.com/get-started/your-authtoken)
ngrok config add-authtoken YOUR_TOKEN_HERE

# Make scripts executable
chmod +x start_mac_server.sh stop_mac_server.sh
```

## 2. Start Servers (Quick Test)

```bash
cd ~/FastScribe
source venv/bin/activate  # Activate virtual environment

# Terminal 1: Whisper server
cd home-server
python whisper_server.py
```

Wait for: `✅ Whisper model loaded and ready!`

Open a NEW terminal:
```bash
cd ~/FastScribe
source venv/bin/activate  # Activate in new terminal too

# Terminal 2: Copilot API
cd copilot-api
python api.py 8080
```

**First time**: It will show a URL and code
- Open browser → https://github.com/login/device
- Enter the code shown
- Authorize GitHub Copilot

```bash
# Terminal 3: Ngrok tunnel
ngrok http 8000
```

Copy the URL like `https://abc123.ngrok-free.app`

## 3. Test It Works

```bash
# Test Whisper
curl http://localhost:8000/health

# Test Copilot
curl -X POST http://localhost:8080/api \
  -H "Content-Type: application/json" \
  -d '{"prompt":"# hello world\ndef ","language":"python"}'
```

## 4. Run as Background Services (24/7)

### Using screen (Simple)

```bash
# Whisper
screen -S whisper
cd ~/FastScribe
source venv/bin/activate
cd home-server
python whisper_server.py
# Press Ctrl+A then D to detach

# Copilot
screen -S copilot
cd ~/FastScribe
source venv/bin/activate
cd copilot-api
python api.py 8080
# Press Ctrl+A then D to detach

# Ngrok
screen -S ngrok
ngrok http 8000
# Press Ctrl+A then D to detach

# List sessions: screen -ls
# Reattach: screen -r whisper
```

### Using systemd (Production - Auto-start on boot)

```bash
# Create Whisper service
sudo nano /etc/systemd/system/fastscribe-whisper.service
```

Paste this:
```ini
[Unit]
Description=FastScribe Whisper Server
After=network.target

[Service]home/YOUR_USERNAME/FastScribe/venv/bin/python
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/FastScribe/home-server
ExecStart=/usr/bin/python3 whisper_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Replace `YOUR_USERNAME` with your actual username!

```bash
# Create Copilot service
sudo nano /etc/systemd/system/fastscribe-copilot.service
```

Paste this:
```ini
[Unit]
Description=FastScribe Copilot API
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/FastScribe/copilot-api
ExecStart=/home/YOUR_USERNAME/FastScribe/venv/bin/python api.py 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable fastscribe-whisper
sudo systemctl enable fastscribe-copilot
sudo systemctl start fastscribe-whisper
sudo systemctl start fastscribe-copilot

# Check status
sudo systemctl status fastscribe-whisper
sudo systemctl status fastscribe-copilot

# View logs
sudo journalctl -u fastscribe-whisper -f
sudo journalctl -u fastscribe-copilot -f
```

## 5. Update Render

Render Dashboard → Environment → Add:
- **Key**: `WHISPER_API_URL`
- **Value**: `https://abc123.ngrok-free.app` (your ngrok URL)

## Troubleshooting

**Port in use:**
```bash
sudo lsof -ti:8000 | xargs kill -9  # Kill process on port 8000
sudo lsof -ti:8080 | xargs kill -9  # Kill process on port 8080
```

**Check logs:**
```bash
# If using screen
screen -r whisper
screen -r copilot

# If using systemd
sudo journalctl -u fastscribe-whisper -n 50
sudo journalctl -u fastscribe-copilot -n 50
```

**Restart services:**
```bash
sudo systemctl restart fastscribe-whisper
sudo systemctl restart fastscribe-copilot
```

**Ngrok disconnects:**
- Free tier: 2-hour sessions, need to restart
- Get new URL from `ngrok http 8000`
- Update `WHISPER_API_URL` in Render

---

## Performance

- **10-min video**: 1-2 minutes
- **1-hour video**: 6-10 minutes  
- **2-hour video**: 6-9 minutes (fast mode) or 8-12 minutes (base)

Cost: ~$2-3/month electricity vs $8-15/month APIs 💰
