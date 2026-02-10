# Minimal Backend for Testing Camera Feed
# Quick start without heavy AI dependencies

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import time
from datetime import datetime

app = FastAPI(title="Smart CCTV - Minimal Mode")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
streaming = False
camera = None

@app.get("/api/")
def root():
    return {"service": "Smart CCTV (Minimal)", "status": "online"}

@app.get("/api/status")
def get_status():
    return {
        "streaming": streaming,
        "camera_active": camera is not None,
        "pipeline_stats": {
            "tracker": {
                "avg_fps": 30,
                "active_tracks": np.random.randint(0, 5)
            }
        }
    }

@app.post("/api/start")
def start_stream():
    global streaming, camera
    streaming = True
    if camera is None:
        # Try to open default camera (0)
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("⚠️  No physical camera found, will use test pattern")
            camera = None
    return {"status": "started", "streaming": streaming}

@app.post("/api/stop")
def stop_stream():
    global streaming, camera
    streaming = False
    if camera is not None:
        camera.release()
        camera = None
    return {"status": "stopped", "streaming": streaming}

def generate_test_frame():
    """Generate a test pattern frame when no camera is available"""
    # Create a 640x480 test pattern
    height, width = 480, 640
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Dark gradient background
    for i in range(height):
        intensity = int(20 + (i / height) * 30)
        frame[i, :] = [intensity, intensity * 0.8, intensity * 0.6]
    
    # Add grid lines
    for i in range(0, width, 80):
        cv2.line(frame, (i, 0), (i, height), (0, 255, 255), 1)
    for i in range(0, height, 60):
        cv2.line(frame, (0, i), (width, i), (0, 255, 255), 1)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, f"TEST FEED - {timestamp}", (150, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    # Add system info
    cv2.putText(frame, "CAM-01 SECTOR 4 [NORTH]", (170, 280),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 1)
    
    # Add some animated elements
    t = int(time.time() * 2) % 360
    center_x, center_y = 320, 240
    radius = 100 + int(np.sin(np.radians(t)) * 20)
    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 255), 2)
    
    # Add corner markers
    corners = [(50, 50), (width - 50, 50), (50, height - 50), (width - 50, height - 50)]
    for (x, y) in corners:
        cv2.line(frame, (x - 15, y), (x + 15, y), (0, 255, 255), 2)
        cv2.line(frame, (x, y - 15), (x, y + 15), (0, 255, 255), 2)
    
    return frame

def gen_frames():
    """Generate video frames - from camera or test pattern"""
    global camera, streaming
    
    while True:
        if not streaming:
            time.sleep(0.1)
            continue
        
        # Try to get frame from camera
        if camera is not None and camera.isOpened():
            success, frame = camera.read()
            if not success:
                print("⚠️  Camera read failed, switching to test pattern")
                camera = None
                frame = generate_test_frame()
        else:
            # Generate test pattern
            frame = generate_test_frame()
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ret:
            continue
        
        # Yield frame in multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        time.sleep(0.033)  # ~30 FPS

@app.get("/api/live")
def live_stream():
    """Stream video feed"""
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
