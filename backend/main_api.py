# main_api.py
from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import signal
import sys
import atexit
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

# NEW: Production pipeline (replaces old ai_pipeline)
from core.production_pipeline import production_pipeline
from core.camera_lifecycle_manager import camera_manager

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application lifecycle events:
    - Startup: Initialize resources
    - Shutdown: Cleanup camera, AI pipeline, GStreamer
    """
    # Startup
    print("🚀 FastAPI server starting...")
    
    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print(f"\n⚠️  Received signal {sig}, shutting down gracefully...")
        cleanup_on_shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination
    
    yield  # Server runs here
    
    # Shutdown
    print("🛑 FastAPI server shutting down...")
    cleanup_on_shutdown()

app = FastAPI(lifespan=lifespan)

# CORS middleware MUST be added immediately after app creation and BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.ngrok-free.app",  # ngrok frontend
        "https://*.ngrok.io",        # legacy ngrok domain
    ],
    allow_origin_regex=r"https://.*\.ngrok-free\.app",  # Dynamic ngrok URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# API Router with /api prefix
api_router = APIRouter(prefix="/api")

# Global state
streaming = False
# Use production_pipeline singleton (replaces ai_pipeline)

def cleanup_on_shutdown():
    """
    Graceful cleanup on server shutdown.
    Ensures camera and GStreamer pipeline are properly released.
    """
    global ai_pipeline, streaming
    
    print("🧹 Starting cleanup...")
    
    # Stop streaming
    streaming = False
    
    # Shutdown camera manager (releases camera + GStreamer pipeline)
    camera_manager.shutdown()
    
    # Reset AI pipeline
    if ai_pipeline is not None:
        try:
            ai_pipeline.reset()
        except Exception as e:
            print(f"⚠️  Error resetting AI pipeline: {e}")
        ai_pipeline = None
    
    print("✅ Cleanup complete")

# Register atexit handler as backup
atexit.register(cleanup_on_shutdown)



def gen_frames():
    """
    Production Frame Generator - Complete AI Pipeline
    
    Pipeline: camera → YOLOv8+ByteTrack → event_detector → security_agent → evidence_recorder → stream
    
    NO DUMMY DATA - All processing is real
    """
    global streaming
    
    print(f"📹 Production frame generator started (streaming={streaming})")
    
    while streaming:
        # Read frame from camera
        success, frame = camera_manager.read_frame()
        
        if not success or frame is None:
            print("⚠️  Camera read failed, waiting for recovery...")
            import time
            time.sleep(0.1)
            continue
        
        try:
            # ⚡ PRODUCTION AI PIPELINE ⚡
            # Returns: annotated_frame + {alerts, events, recordings, stats}
            processed_frame, pipeline_data = production_pipeline.process_frame(frame)
            
            # Log alerts in real-time
            if pipeline_data.get("alerts_raised", 0) > 0:
                for alert in pipeline_data.get("alerts", []):
                    print(f"🚨 ALERT: {alert['event']['event_type']} | {alert['decision']['severity']}")
            
            # Encode frame
            _, buffer = cv2.imencode(".jpg", processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            frame_bytes = buffer.tobytes()
            
            # Log every 100 frames
            if pipeline_data["frame_number"] % 100 == 0:
                print(f"✅ Frame {pipeline_data['frame_number']} | FPS: {pipeline_data['fps']:.1f} | "
                      f"Tracks: {pipeline_data['active_tracks']} | Alerts: {pipeline_data['metrics']['total_alerts']}")
            
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes +
                b"\r\n"
            )
        except Exception as e:
            print(f"⚠️  Frame processing error: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("📹 Production frame generator stopped")

@api_router.post("/start")
def start_camera():
    """
    Initialize camera and prepare for streaming with Production Pipeline
    """
    # Start camera through lifecycle manager
    success, message = camera_manager.start_stream(camera_source=0, use_gstreamer=False)
    
    if not success:
        return {
            "status": "error",
            "message": message,
            "camera_state": camera_manager.get_state()
        }, 500
    
    # Production pipeline is always active (singleton)
    print("🚀 Production Pipeline ready")
    
    return {
        "status": "ready",
        "message": message,
        "pipeline_active": True,
        "camera_state": camera_manager.get_state()
    }

@api_router.get("/live")
def live_feed():
    """MJPEG stream endpoint with AI processing"""
    global streaming
    streaming = True
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@api_router.post("/stop")
def stop_camera():
    """
    Stop camera stream and release all resources.
    """
    global streaming
    
    # Stop streaming flag
    streaming = False
    
    # Stop camera through lifecycle manager
    success, message = camera_manager.stop_stream()
    
    # Reset production pipeline
    try:
        production_pipeline.reset()
        print("🤖 Production Pipeline reset")
    except Exception as e:
        print(f"⚠️  Pipeline reset error: {e}")
    
    return {
        "status": "stopped" if success else "error",
        "message": message,
        "pipeline": "reset",
        "camera_state": camera_manager.get_state()
    }


@app.get("/")
def root():
    """Health check endpoint with camera state"""
    return {
        "service": "Smart Edge-AI CCTV System",
        "version": "1.0.0",
        "ai_enabled": True,
        "streaming": streaming,
        "ai_pipeline_active": ai_pipeline is not None,
        "camera_state": camera_manager.get_state()
    }


@api_router.get("/intelligence")
def get_intelligence_status():
    """Get detailed Intelligence Layer status and metrics"""
    if not ai_pipeline or not hasattr(ai_pipeline, 'intelligence'):
        return {
            "error": "Intelligence Layer not initialized",
            "status": "OFFLINE"
        }
    
    return ai_pipeline.intelligence.get_system_status()


@api_router.get("/status")
def get_status():
    """Get current system status with Production Pipeline data"""
    camera_state = camera_manager.get_state()
    pipeline_stats = production_pipeline.get_pipeline_stats()
    
    status_data = {
        "streaming": streaming,
        "camera_active": camera_state["camera_opened"],
        "camera_state": camera_state["state"],
        "frame_count": camera_state["frame_count"],
        "pipeline_active": True,
        "pipeline_stats": pipeline_stats
    }
    
    return status_data


@api_router.get("/alerts/live")
def get_live_alerts(limit: int = 50):
    """
    Get recent security alerts (REAL DATA)
    
    Returns alerts generated by SecurityAgent from actual events
    """
    alerts = production_pipeline.get_recent_alerts(limit)
    
    return {
        "total": len(alerts),
        "alerts": alerts
    }


@api_router.get("/evidence/list")
def get_evidence_list(limit: int = 50, severity: Optional[str] = None):
    """
    Get list of recorded evidence clips (REAL VIDEO FILES)
    
    Query params:
        limit: Max results (default 50)
        severity: Filter by CRITICAL, HIGH, MEDIUM, LOW
    """
    evidence = production_pipeline.get_evidence_list(limit, severity)
    
    return {
        "total": len(evidence),
        "evidence": evidence
    }


@api_router.get("/evidence/{event_id}")
def get_evidence_by_id(event_id: str):
    """Get specific evidence clip metadata"""
    evidence = production_pipeline.recorder.get_evidence_by_id(event_id)
    
    if not evidence:
        return {"error": "Evidence not found"}, 404
    
    return evidence


@api_router.get("/evidence/{event_id}/video")
def stream_evidence_video(event_id: str):
    """Stream recorded evidence video"""
    evidence = production_pipeline.recorder.get_evidence_by_id(event_id)
    
    if not evidence:
        return {"error": "Evidence not found"}, 404
    
    filepath = Path(evidence["filepath"])
    
    if not filepath.exists():
        return {"error": "Video file not found"}, 404
    
    return FileResponse(
        path=str(filepath),
        media_type="video/mp4",
        filename=evidence["filename"]
    )


@api_router.delete("/evidence/{event_id}")
def delete_evidence(event_id: str):
    """Delete evidence clip"""
    success = production_pipeline.recorder.delete_evidence(event_id)
    
    if not success:
        return {"error": "Failed to delete evidence"}, 400
    
    return {"message": "Evidence deleted successfully"}


# Include API router in the app
app.include_router(api_router)

# Keep root endpoint without /api prefix for health checks
@app.get("/")
def root():
    """Health check endpoint with camera state"""
    return {
        "service": "Smart Edge-AI CCTV System",
        "version": "1.0.0",
        "ai_enabled": True,
        "streaming": streaming,
        "ai_pipeline_active": ai_pipeline is not None,
        "camera_state": camera_manager.get_state()
    }

