#!/bin/bash

# SentraAGI Sovereign Chat Console Startup Script
# Phase 21: The Final Sovereign Trials

echo "🧠 Starting SentraAGI Sovereign Chat Console..."
echo "================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import fastapi, uvicorn, openai, python_multipart" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing required packages. Please install:"
    echo "   pip3 install fastapi uvicorn openai python-multipart"
    exit 1
fi

# Set environment variables
export OPENAI_API_KEY=${OPENAI_API_KEY:-""}
export SENTRA_CHAT_PORT=${SENTRA_CHAT_PORT:-"8001"}
export SENTRA_CHAT_HOST=${SENTRA_CHAT_HOST:-"0.0.0.0"}

echo "✅ Dependencies OK"
echo "🔧 Configuration:"
echo "   - Host: $SENTRA_CHAT_HOST"
echo "   - Port: $SENTRA_CHAT_PORT"
if [ -n "$OPENAI_API_KEY" ]; then
    echo "   - OpenAI API: Configured"
else
    echo "   - OpenAI API: Not configured (will use fallback responses)"
fi

# Start the chat console
echo ""
echo "🌐 Starting chat server..."
echo "💬 Open your browser: http://localhost:$SENTRA_CHAT_PORT"
echo "🛑 Press Ctrl+C to stop"
echo ""

python3 sovereign_chat.py 