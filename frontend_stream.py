#!/usr/bin/env python3
"""
SentraAGI Virtual Senses Frontend - FastAPI + OpenCV Stream

Streams live camera feed processed by VirtualSenses to a web browser.
Supports overlays: YOLO detections, SAM masks, CLIP captions (optional)

Author: SentraAGI Team
Version: Phase 21
"""

import os
import time
import logging
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np

# Import SentraAGI modules
from multi_modal.virtual_senses import VirtualSenses

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SentraAGI Virtual Senses Frontend",
    description="Live camera feed with AI perception overlays",
    version="Phase 21"
)

# Initialize Virtual Senses
vs = VirtualSenses()

# Global settings
OVERLAY_ENABLED = os.getenv('SENTRA_OVERLAY_ENABLED', 'true').lower() == 'true'
FRAME_RATE = int(os.getenv('SENTRA_FRAME_RATE', '30'))
QUALITY = int(os.getenv('SENTRA_JPEG_QUALITY', '85'))


@app.get("/", response_class=HTMLResponse)
async def index():
    """Main page with live video feed."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>👁️ SentraAGI - Synthetic Vision Online</title>
        <style>
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
                color: #00ff88;
                font-family: 'Courier New', monospace;
                margin: 0;
                padding: 20px;
                text-align: center;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 0 0 10px #00ff88;
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { text-shadow: 0 0 10px #00ff88; }
                to { text-shadow: 0 0 20px #00ff88, 0 0 30px #00ff88; }
            }
            
            .subtitle {
                font-size: 1.2em;
                color: #88ff88;
                margin-bottom: 30px;
            }
            
            .video-container {
                position: relative;
                display: inline-block;
                margin: 20px 0;
            }
            
            .video-feed {
                border: 3px solid #00ff88;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
                max-width: 100%;
                height: auto;
            }
            
            .controls {
                margin: 20px 0;
                padding: 20px;
                background: rgba(0, 255, 136, 0.1);
                border-radius: 10px;
                border: 1px solid #00ff88;
            }
            
            .control-group {
                margin: 10px 0;
            }
            
            label {
                display: inline-block;
                width: 150px;
                text-align: right;
                margin-right: 10px;
            }
            
            select, button {
                background: #1a1a2e;
                color: #00ff88;
                border: 1px solid #00ff88;
                padding: 8px 15px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Courier New', monospace;
            }
            
            select:hover, button:hover {
                background: #00ff88;
                color: #1a1a2e;
            }
            
            .status {
                margin: 20px 0;
                padding: 15px;
                background: rgba(0, 255, 136, 0.1);
                border-radius: 8px;
                border-left: 4px solid #00ff88;
            }
            
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #00ff88;
                margin-right: 10px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .info-panel {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            
            .info-card {
                background: rgba(0, 255, 136, 0.05);
                border: 1px solid #00ff88;
                border-radius: 8px;
                padding: 15px;
                text-align: left;
            }
            
            .info-card h3 {
                margin-top: 0;
                color: #88ff88;
            }
            
            .detection-list {
                max-height: 200px;
                overflow-y: auto;
                background: rgba(0, 0, 0, 0.3);
                padding: 10px;
                border-radius: 5px;
            }
            
            .detection-item {
                margin: 5px 0;
                padding: 5px;
                background: rgba(0, 255, 136, 0.1);
                border-radius: 3px;
            }
            
            .footer {
                margin-top: 40px;
                padding: 20px;
                border-top: 1px solid #00ff88;
                color: #88ff88;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👁️ SentraAGI - Synthetic Vision Online</h1>
            <div class="subtitle">Phase 21: The Final Sovereign Trials</div>
            
            <div class="status">
                <span class="status-indicator"></span>
                <strong>Status:</strong> Virtual Senses Active | AI Perception Engaged | Stream Live
            </div>
            
            <div class="video-container">
                <img src="/video_feed" alt="SentraAGI Vision Feed" class="video-feed" width="800" height="600">
            </div>
            
            <div class="controls">
                <div class="control-group">
                    <label for="overlay-mode">Overlay Mode:</label>
                    <select id="overlay-mode" onchange="updateOverlay()">
                        <option value="full">Full AI Overlays</option>
                        <option value="yolo">YOLO Detection Only</option>
                        <option value="sam">SAM Segmentation Only</option>
                        <option value="none">No Overlays</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label for="quality">Stream Quality:</label>
                    <select id="quality" onchange="updateQuality()">
                        <option value="high">High Quality</option>
                        <option value="medium" selected>Medium Quality</option>
                        <option value="low">Low Quality</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <button onclick="captureFrame()">📸 Capture Frame</button>
                    <button onclick="toggleRecording()">🎥 Toggle Recording</button>
                    <button onclick="refreshStats()">📊 Refresh Stats</button>
                </div>
            </div>
            
            <div class="info-panel">
                <div class="info-card">
                    <h3>🔍 Live Detections</h3>
                    <div id="detection-list" class="detection-list">
                        <div class="detection-item">Loading detections...</div>
                    </div>
                </div>
                
                <div class="info-card">
                    <h3>📈 System Stats</h3>
                    <div id="system-stats">
                        <p><strong>Frame Rate:</strong> <span id="fps">--</span> FPS</p>
                        <p><strong>Resolution:</strong> <span id="resolution">--</span></p>
                        <p><strong>Processing Time:</strong> <span id="processing-time">--</span> ms</p>
                        <p><strong>Memory Usage:</strong> <span id="memory-usage">--</span> MB</p>
                    </div>
                </div>
                
                <div class="info-card">
                    <h3>🧠 AI Models</h3>
                    <div id="model-status">
                        <p><strong>YOLO:</strong> <span id="yolo-status">Initializing...</span></p>
                        <p><strong>SAM:</strong> <span id="sam-status">Initializing...</span></p>
                        <p><strong>CLIP:</strong> <span id="clip-status">Initializing...</span></p>
                        <p><strong>OpenCV:</strong> <span id="opencv-status">Active</span></p>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>SentraAGI Virtual Senses Frontend</strong> | Phase 21 | Real-time AI Perception</p>
                <p>Powered by OpenCV, YOLO, SAM, and CLIP | Built with FastAPI</p>
            </div>
        </div>
        
        <script>
            // Update overlay mode
            function updateOverlay() {
                const mode = document.getElementById('overlay-mode').value;
                fetch('/api/overlay/' + mode);
            }
            
            // Update quality
            function updateQuality() {
                const quality = document.getElementById('quality').value;
                fetch('/api/quality/' + quality);
            }
            
            // Capture frame
            function captureFrame() {
                fetch('/api/capture')
                    .then(response => response.blob())
                    .then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'sentraagi_capture_' + Date.now() + '.jpg';
                        a.click();
                    });
            }
            
            // Toggle recording
            function toggleRecording() {
                fetch('/api/recording/toggle');
            }
            
            // Refresh stats
            function refreshStats() {
                fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('fps').textContent = data.fps || '--';
                        document.getElementById('resolution').textContent = data.resolution || '--';
                        document.getElementById('processing-time').textContent = data.processing_time || '--';
                        document.getElementById('memory-usage').textContent = data.memory_usage || '--';
                        
                        // Update model status
                        document.getElementById('yolo-status').textContent = data.models.yolo;
                        document.getElementById('sam-status').textContent = data.models.sam;
                        document.getElementById('clip-status').textContent = data.models.clip;
                        document.getElementById('opencv-status').textContent = data.models.opencv;
                        
                        // Update detections
                        const detectionList = document.getElementById('detection-list');
                        detectionList.innerHTML = '';
                        if (data.detections && data.detections.length > 0) {
                            data.detections.forEach(detection => {
                                const item = document.createElement('div');
                                item.className = 'detection-item';
                                item.textContent = `${detection.class_name} (${(detection.confidence * 100).toFixed(1)}%)`;
                                detectionList.appendChild(item);
                            });
                        } else {
                            detectionList.innerHTML = '<div class="detection-item">No objects detected</div>';
                        }
                    });
            }
            
            // Auto-refresh stats every 2 seconds
            setInterval(refreshStats, 2000);
            
            // Initial load
            refreshStats();
        </script>
    </body>
    </html>
    """


def generate_frames():
    """Generate video frames for streaming."""
    frame_count = 0
    start_time = time.time()
    
    while True:
        try:
            # Get frame with overlays
            frame = vs.get_frame(include_overlays=OVERLAY_ENABLED)
            
            if frame is None:
                logger.warning("Failed to capture frame")
                time.sleep(0.1)
                continue
            
            # Calculate FPS
            frame_count += 1
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                fps = frame_count / elapsed
                logger.info(f"Stream FPS: {fps:.1f}")
            
            # Encode frame to JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY]
            _, jpeg = cv2.imencode('.jpg', frame, encode_param)
            
            # Yield frame data
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            
            # Control frame rate
            time.sleep(1.0 / FRAME_RATE)
            
        except Exception as e:
            logger.error(f"Error generating frame: {e}")
            time.sleep(0.1)


@app.get("/video_feed")
async def video_feed():
    """Stream video feed with MJPEG format."""
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/api/overlay/{mode}")
async def set_overlay_mode(mode: str):
    """Set overlay mode for video feed."""
    global OVERLAY_ENABLED
    
    if mode == "none":
        OVERLAY_ENABLED = False
    else:
        OVERLAY_ENABLED = True
    
    logger.info(f"Overlay mode set to: {mode}")
    return {"status": "success", "mode": mode}


@app.get("/api/quality/{quality}")
async def set_quality(quality: str):
    """Set JPEG quality for video stream."""
    global QUALITY
    
    quality_map = {
        "high": 95,
        "medium": 85,
        "low": 70
    }
    
    QUALITY = quality_map.get(quality, 85)
    logger.info(f"Quality set to: {quality} ({QUALITY})")
    return {"status": "success", "quality": quality, "value": QUALITY}


@app.get("/api/capture")
async def capture_frame():
    """Capture a single frame and return as image."""
    frame = vs.get_frame(include_overlays=OVERLAY_ENABLED)
    
    if frame is None:
        return {"error": "Failed to capture frame"}
    
    # Encode to JPEG
    _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    
    return StreamingResponse(
        iter([jpeg.tobytes()]),
        media_type="image/jpeg",
        headers={"Content-Disposition": f"attachment; filename=sentraagi_capture_{int(time.time())}.jpg"}
    )


@app.get("/api/recording/toggle")
async def toggle_recording():
    """Toggle video recording (placeholder for future implementation)."""
    logger.info("Recording toggle requested")
    return {"status": "success", "message": "Recording toggle not yet implemented"}


@app.get("/api/stats")
async def get_stats():
    """Get system statistics and detection data."""
    try:
        # Get Virtual Senses status
        vs_status = vs.get_status()
        
        # Get current frame for detections
        frame = vs.capture_frame()
        detections = []
        if frame is not None:
            detections = vs.detect_objects(frame)
        
        # Calculate processing time (placeholder)
        processing_time = 15.5  # ms
        
        # Get system info
        stats = {
            "fps": 30.0,  # Placeholder
            "resolution": f"{frame.shape[1]}x{frame.shape[0]}" if frame is not None else "Unknown",
            "processing_time": processing_time,
            "memory_usage": 125.7,  # MB placeholder
            "models": {
                "yolo": "Active" if vs.yolo_model else "Not Loaded",
                "sam": "Active" if vs.sam_predictor else "Not Loaded",
                "clip": "Active" if vs.clip_model else "Not Loaded",
                "opencv": "Active" if vs.cap and vs.cap.isOpened() else "Error"
            },
            "detections": detections
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {"error": str(e)}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "SentraAGI Virtual Senses Frontend",
        "version": "Phase 21",
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting SentraAGI Virtual Senses Frontend...")
    logger.info(f"Overlay enabled: {OVERLAY_ENABLED}")
    logger.info(f"Frame rate: {FRAME_RATE} FPS")
    logger.info(f"JPEG quality: {QUALITY}")
    
    uvicorn.run(
        "frontend_stream:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 