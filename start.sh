#!/bin/bash
# Render Startup Script - Runs both copilot-api and Flask

set -e

echo "🚀 Starting FastScribe with Copilot API integration..."

# Check if copilot-api exists, if not clone it
if [ ! -d "copilot-api" ]; then
    echo "📥 Cloning copilot-api..."
    git clone https://github.com/B00TK1D/copilot-api.git
    cd copilot-api
    pip install -r requirements.txt
    cd ..
fi

# Check for Copilot token
if [ ! -f "copilot-api/.copilot_token" ]; then
    echo "⚠️  WARNING: No Copilot token found!"
    echo "You need to authenticate locally and upload the .copilot_token file"
    echo "See RENDER_COPILOT_SETUP.md for instructions"
    
    # Check if token is in environment variable
    if [ -n "$COPILOT_TOKEN" ]; then
        echo "✅ Found COPILOT_TOKEN in environment, creating token file..."
        echo "$COPILOT_TOKEN" > copilot-api/.copilot_token
    else
        echo "❌ No COPILOT_TOKEN environment variable found"
        echo "Deployment will fail without authentication!"
        exit 1
    fi
fi

echo "✅ Copilot token found"

# Start copilot-api in the background
echo "🔧 Starting Copilot API server on port 8080..."
cd copilot-api
python api.py 8080 &
COPILOT_PID=$!
cd ..

# Wait for copilot-api to be ready
echo "⏳ Waiting for Copilot API to be ready..."
sleep 5

# Check if copilot-api is running
if ! kill -0 $COPILOT_PID 2>/dev/null; then
    echo "❌ Copilot API failed to start"
    exit 1
fi

echo "✅ Copilot API is running (PID: $COPILOT_PID)"

# Start Flask app with Gunicorn
echo "🌐 Starting Flask app with Gunicorn..."
cd backend
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app

# If Flask crashes, kill copilot-api
kill $COPILOT_PID 2>/dev/null || true
