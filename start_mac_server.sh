#!/bin/bash
# FastScribe Mac Server - Start All Services
# Run this on your MacBook Pro to start Whisper + Copilot servers

echo "=================================="
echo "FastScribe Mac Server Startup"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "home-server/whisper_server.py" ]; then
    echo "❌ Error: Run this from FastScribe root directory"
    echo "cd ~/FastScribe && ./start_mac_server.sh"
    exit 1
fi

# Function to check if port is in use
check_port() {
    lsof -ti:$1 > /dev/null 2>&1
}

# Kill existing processes on our ports
echo "🧹 Cleaning up old processes..."
if check_port 8000; then
    echo "  Killing process on port 8000"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi
if check_port 8080; then
    echo "  Killing process on port 8080"
    lsof -ti:8080 | xargs kill -9 2>/dev/null
fi

echo ""
echo "🚀 Starting servers in background..."
echo ""

# Start Whisper server
echo "1️⃣  Starting Whisper transcription server..."
cd home-server
python3 whisper_server.py > ../logs/whisper.log 2>&1 &
WHISPER_PID=$!
cd ..
sleep 3

# Check if Whisper started
if check_port 8000; then
    echo "   ✅ Whisper server running on http://localhost:8000"
else
    echo "   ❌ Failed to start Whisper server"
    echo "   Check logs: cat logs/whisper.log"
    exit 1
fi

# Start Copilot API server
echo ""
echo "2️⃣  Starting GitHub Copilot API server..."
cd copilot-api
python3 api.py 8080 > ../logs/copilot.log 2>&1 &
COPILOT_PID=$!
cd ..
sleep 3

# Check if Copilot started
if check_port 8080; then
    echo "   ✅ Copilot API running on http://localhost:8080"
else
    echo "   ❌ Failed to start Copilot API"
    echo "   Check logs: cat logs/copilot.log"
    exit 1
fi

echo ""
echo "=================================="
echo "✅ All servers running!"
echo "=================================="
echo ""
echo "📊 Status:"
echo "  Whisper:  http://localhost:8000 (PID: $WHISPER_PID)"
echo "  Copilot:  http://localhost:8080 (PID: $COPILOT_PID)"
echo ""
echo "📝 Logs:"
echo "  Whisper:  tail -f logs/whisper.log"
echo "  Copilot:  tail -f logs/copilot.log"
echo ""
echo "🌐 Next step: Start ngrok tunnel"
echo "  ngrok http 8000"
echo ""
echo "🛑 To stop servers:"
echo "  kill $WHISPER_PID $COPILOT_PID"
echo ""
