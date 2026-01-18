#!/bin/bash
# Stop all FastScribe Mac servers

echo "🛑 Stopping FastScribe servers..."

# Kill processes on our ports
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "  Stopping Whisper server (port 8000)"
    lsof -ti:8000 | xargs kill -9
fi

if lsof -ti:8080 > /dev/null 2>&1; then
    echo "  Stopping Copilot API (port 8080)"
    lsof -ti:8080 | xargs kill -9
fi

# Kill ngrok if running
if pgrep ngrok > /dev/null 2>&1; then
    echo "  Stopping ngrok tunnel"
    pkill ngrok
fi

echo ""
echo "✅ All servers stopped!"
