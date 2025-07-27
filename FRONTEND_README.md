# 👁️ SentraAGI Virtual Senses Frontend

**Phase 21: The Final Sovereign Trials**

Real-time camera feed streaming with AI perception overlays powered by OpenCV, YOLO, SAM, and CLIP.

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)
```bash
./start_frontend.sh
```

### Option 2: Direct Python execution
```bash
python3 frontend_stream.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn frontend_stream:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Access the Frontend

Once running, open your browser and navigate to:
- **Main Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

## ✨ Features

### 🎥 Live Video Streaming
- Real-time camera feed with MJPEG streaming
- Configurable frame rate (default: 30 FPS)
- Adjustable JPEG quality (High/Medium/Low)
- Automatic camera device detection

### 🤖 AI Perception Overlays
- **YOLO Object Detection**: Real-time object detection with bounding boxes
- **SAM Segmentation**: Image segmentation with mask overlays
- **CLIP Grounding**: Concept grounding and captioning
- **Configurable Overlays**: Enable/disable individual AI components

### 🎛️ Interactive Controls
- **Overlay Mode Selection**: Full AI, YOLO only, SAM only, or no overlays
- **Quality Control**: Adjust stream quality for performance
- **Frame Capture**: Download individual frames as JPEG
- **Recording Toggle**: Start/stop video recording (future feature)

### 📊 Real-time Statistics
- **System Stats**: FPS, resolution, processing time, memory usage
- **Model Status**: YOLO, SAM, CLIP, and OpenCV status indicators
- **Live Detections**: Real-time list of detected objects with confidence scores
- **Auto-refresh**: Statistics update every 2 seconds

## 🛠️ Configuration

### Environment Variables
```bash
# Overlay settings
export SENTRA_OVERLAY_ENABLED=true          # Enable AI overlays
export SENTRA_FRAME_RATE=30                 # Frames per second
export SENTRA_JPEG_QUALITY=85               # JPEG quality (0-100)

# Camera settings
export SENTRA_OPENCV_DEVICE=0               # Camera device index

# Model paths (optional)
export SENTRA_YOLO_MODEL=yolov8n.pt        # YOLO model path
export SENTRA_SAM_MODEL=sam_vit_h_4b8939.pth # SAM model path
export SENTRA_CLIP_MODEL=ViT-B/32          # CLIP model name
```

### API Endpoints

#### Video Streaming
- `GET /video_feed` - MJPEG video stream
- `GET /api/capture` - Capture single frame

#### Configuration
- `GET /api/overlay/{mode}` - Set overlay mode
- `GET /api/quality/{quality}` - Set stream quality

#### System Information
- `GET /api/stats` - Get system statistics
- `GET /health` - Health check endpoint

## 🎨 User Interface

### Design Features
- **Cyberpunk Theme**: Dark gradient background with neon green accents
- **Responsive Layout**: Adapts to different screen sizes
- **Real-time Updates**: Live statistics and detection lists
- **Smooth Animations**: Glowing effects and pulsing indicators
- **Professional Styling**: Clean, modern interface with SentraAGI branding

### Interface Sections
1. **Header**: SentraAGI branding with Phase 21 designation
2. **Status Bar**: System status with animated indicator
3. **Video Feed**: Main camera stream with configurable overlays
4. **Control Panel**: Overlay modes, quality settings, and action buttons
5. **Information Panels**: Live detections, system stats, and AI model status
6. **Footer**: Technical information and credits

## 🔧 Technical Details

### Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │◄──►│   FastAPI App   │◄──►│  VirtualSenses  │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │    │ • MJPEG Stream  │    │ • OpenCV Capture│
│ • Real-time UI  │    │ • REST API      │    │ • YOLO Detection│
│ • Controls      │    │ • WebSocket     │    │ • SAM Segmentation│
└─────────────────┘    └─────────────────┘    │ • CLIP Grounding│
                                              └─────────────────┘
```

### Dependencies
- **FastAPI**: Web framework for API and streaming
- **OpenCV**: Computer vision and camera capture
- **Uvicorn**: ASGI server for FastAPI
- **NumPy**: Numerical computing for image processing

### Performance Considerations
- **Frame Rate Control**: Configurable FPS to balance quality and performance
- **Quality Settings**: Adjustable JPEG compression
- **Overlay Toggle**: Disable AI processing for better performance
- **Memory Management**: Efficient frame processing and cleanup

## 🚨 Troubleshooting

### Common Issues

#### Camera Not Working
```bash
# Check camera device
ls /dev/video*

# Test with OpenCV
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
```

#### Missing Dependencies
```bash
# Install required packages
pip install fastapi uvicorn opencv-python-headless

# For development
pip install fastapi[all] uvicorn[standard]
```

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Use different port
uvicorn frontend_stream:app --port 8001
```

#### AI Models Not Loading
- Ensure model files are in the correct paths
- Check environment variables for model paths
- Models are optional - frontend works without them

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python3 frontend_stream.py
```

## 🔮 Future Enhancements

### Planned Features
- **Video Recording**: Save video streams to disk
- **Multiple Cameras**: Support for multiple camera feeds
- **Advanced Overlays**: Custom overlay configurations
- **WebSocket Updates**: Real-time UI updates via WebSocket
- **Authentication**: Secure access control
- **Mobile Support**: Responsive design for mobile devices

### AI Model Integration
- **Real YOLO Models**: Load actual YOLO models for detection
- **SAM Integration**: Full SAM segmentation support
- **CLIP Grounding**: Real-time concept grounding
- **Custom Models**: Support for custom trained models

## 📝 Development

### Project Structure
```
SentraAGI/
├── frontend_stream.py      # Main FastAPI application
├── start_frontend.sh       # Startup script
├── multi_modal/
│   └── virtual_senses.py   # VirtualSenses class
└── FRONTEND_README.md      # This file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of SentraAGI Phase 21: The Final Sovereign Trials.

---

**SentraAGI now sees — and so do you.** 🜂 