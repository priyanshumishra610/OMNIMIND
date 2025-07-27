#!/bin/bash

# SentraAGI Virtual Senses Frontend Startup Script
# Phase 21: The Final Sovereign Trials

echo "🚀 Starting SentraAGI Virtual Senses Frontend..."
echo "================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import fastapi, uvicorn, cv2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing required packages. Please install:"
    echo "   pip install fastapi uvicorn opencv-python-headless"
    exit 1
fi

# Set environment variables
export SENTRA_OVERLAY_ENABLED=true
export SENTRA_FRAME_RATE=30
export SENTRA_JPEG_QUALITY=85
export SENTRA_OPENCV_DEVICE=0

echo "✅ Dependencies OK"
echo "🔧 Configuration:"
echo "   - Overlay: $SENTRA_OVERLAY_ENABLED"
echo "   - Frame Rate: $SENTRA_FRAME_RATE FPS"
echo "   - Quality: $SENTRA_JPEG_QUALITY"
echo "   - Camera: $SENTRA_OPENCV_DEVICE"

# Start the frontend
echo ""
echo "🌐 Starting web server..."
echo "📱 Open your browser: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop"
echo ""

python3 frontend_stream.py 