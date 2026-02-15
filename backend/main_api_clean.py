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

# STABLE PIPELINE: OpenVINO + ByteTrack + Context Reasoning (filters static objects!)
from core.stable_production_pipeline import stable_pipeline
from core.camera_lifecycle_manager import camera_manager

# EVENT STORE: Production-grade event reasoning pipeline
from backend.event_store import (
    publish_event, get_events, EventType, EventSeverity,
    generate_reasoning_text, get_severity_level
)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application lifecycle events:
    - Startup: Initialize resources
    - Shutdown: Cleanup camera, AI pipeline, GStreamer
    """
    # Startup
    print("≡ƒÜÇ FastAPI server starting...")
    
    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print(f"\nΓÜá∩╕Å  Received signal {sig}, shutting down gracefully...")
        cleanup_on_shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination
    
    yield  # Server runs here
    
    # Shutdown
    print("≡ƒ¢æ FastAPI server shutting down...")
    cleanup_on_shutdown()

app = FastAPI(lifespan=lifespan)

# CORS middleware ΓÇö allow ALL origins so any port / domain works without fail
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# API Router with /api prefix
api_router = APIRouter(prefix="/api")

# Global state
streaming = False
# Use stable_pipeline singleton (filters static objects like fans/ACs)

def cleanup_on_shutdown():
    """
    Graceful cleanup on server shutdown.
    Ensures camera and GStreamer pipeline are properly released.
    """
    global streaming
    
    print("≡ƒº╣ Starting cleanup...")
    
    # Stop streaming
    streaming = False
    
    # Shutdown camera manager (releases camera + GStreamer pipeline)
    camera_manager.shutdown()
    
    # Reset stable pipeline if needed
    try:
        stable_pipeline.reset()
    except Exception as e:
        print(f"ΓÜá∩╕Å  Error resetting pipeline: {e}")
    
    print("Γ£à Cleanup complete")

# Register atexit handler as backup
atexit.register(cleanup_on_shutdown)



def _ensure_camera():
    """Make sure camera is open. Auto-start if needed. Never fail."""
    state = camera_manager.get_state()
    if not state.get("camera_opened", False):
        for source in [0, 1, 2]:
            try:
                ok, msg = camera_manager.start_stream(camera_source=source, use_gstreamer=False)
                if ok:
                    print(f"≡ƒô╣ Camera auto-started on source {source}")
                    return True
            except Exception:
                continue
        return False
    return True


def gen_frames():
    """
    Low-Latency Frame Generator
    
    Key optimization: AI runs on every Nth frame, but the LATEST camera
    frame is ALWAYS sent to the browser immediately. No buffering delay.
    """
    global streaming
    import time
    
    print("≡ƒô╣ Frame generator started")
    fail_count = 0
    max_fails = 30
    frame_num = 0
    AI_INTERVAL = 1  # Run AI every frame for max detection coverage
    
    while streaming:
        _ensure_camera()
        
        # Read the LATEST frame (buffer is drained in camera manager)
        success, frame = camera_manager.read_frame()
        
        if not success or frame is None:
            fail_count += 1
            if fail_count >= max_fails:
                print("ΓÜá∩╕Å  Camera unresponsive, attempting re-open...")
                try:
                    camera_manager.stop_stream()
                except Exception:
                    pass
                time.sleep(0.5)
                _ensure_camera()
                fail_count = 0
            else:
                time.sleep(0.01)
            continue
        
        fail_count = 0
        frame_num += 1
        
        # Run AI silently on every Nth frame (non-blocking to stream)
        if frame_num % AI_INTERVAL == 0:
            try:
                stable_pipeline.process_frame(frame)
                
                # Publish events from pipeline alerts (every 30 frames ~ 1 second)
                if frame_num % 30 == 0:
                    try:
                        alerts = stable_pipeline.get_recent_alerts(limit=5)
                        for alert in alerts:
                            # Basic deduplication
                            alert_key = f"{alert.get('track_id', 0)}_{alert.get('event_type', 'unknown')}"
                            if not hasattr(gen_frames, 'processed_alerts'):
                                gen_frames.processed_alerts = set()
                            
                            if alert_key not in gen_frames.processed_alerts:
                                # Map alert types to event types
                                event_mapping = {
                                    'loitering': EventType.LOITERING,
                                    'loitering_detected': EventType.LOITERING,
                                    'zone_violation': EventType.ZONE_VIOLATION,
                                    'restricted_area': EventType.INTRUSION,
                                    'intrusion': EventType.INTRUSION,
                                    'theft_suspected': EventType.THEFT,
                                    'fighting': EventType.FIGHT,
                                    'crowd_forming': EventType.CROWD_FORMING,
                                    'abandoned_object': EventType.ABANDONED_OBJECT
                                }
                                
                                alert_type = alert.get('event_type', 'unknown').lower()
                                event_type = event_mapping.get(alert_type, EventType.NORMAL)
                                
                                # Only publish non-normal events
                                if event_type != EventType.NORMAL:
                                    track_id = alert.get('track_id', 0)
                                    severity_score = alert.get('severity', 0.5)
                                    duration = alert.get('duration', 0)
                                    
                                    severity = get_severity_level(severity_score)
                                    reasoning_text = generate_reasoning_text(
                                        event_type, track_id, duration, {}
                                    )
                                    
                                    publish_event(
                                        event_type=event_type,
                                        severity=severity,
                                        track_id=track_id,
                                        severity_score=severity_score,
                                        duration=duration,
                                        reasoning_text=reasoning_text
                                    )
                                    
                                    gen_frames.processed_alerts.add(alert_key)
                                    
                                    # Keep set from growing too large
                                    if len(gen_frames.processed_alerts) > 100:
                                        gen_frames.processed_alerts.clear()
                    except Exception:
                        pass  # Silently skip event publishing errors
                        
            except Exception as e:
                if frame_num < 20:  # log first few failures
                    print(f"ΓÜá∩╕Å AI pipeline error: {e}")
        
        # ALWAYS send the raw latest frame immediately ΓÇö never wait for AI
        try:
            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes() +
                b"\r\n"
            )
        except Exception:
            time.sleep(0.01)
            continue
    
    print("≡ƒô╣ Frame generator stopped")

@api_router.post("/start")
def start_camera():
    """
    Initialize camera ΓÇö tries multiple sources, never gives up.
    """
    global streaming
    
    # Try camera sources 0, 1, 2
    success = False
    message = "No camera found"
    for source in [0, 1, 2]:
        try:
            success, message = camera_manager.start_stream(camera_source=source, use_gstreamer=False)
            if success:
                break
        except Exception as e:
            message = str(e)
            continue
    
    streaming = True  # Always set so /live works
    
    return {
        "status": "ready" if success else "degraded",
        "message": message,
        "pipeline_active": True,
        "camera_state": camera_manager.get_state()
    }

@api_router.get("/live")
def live_feed():
    """MJPEG stream ΓÇö auto-starts camera if not already running."""
    global streaming
    streaming = True
    _ensure_camera()
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Access-Control-Allow-Origin": "*"
        }
    )

@api_router.get("/live/simple")
def live_feed_simple():
    """Simple MJPEG stream without AI processing - for testing"""
    global streaming
    streaming = True
    
    def gen_simple():
        import time
        while streaming:
            success, frame = camera_manager.read_frame()
            if success and frame is not None:
                _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" +
                       buffer.tobytes() + b"\r\n")
            else:
                time.sleep(0.033)
    
    return StreamingResponse(
        gen_simple(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Access-Control-Allow-Origin": "*"
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
    
    # Reset stable pipeline
    try:
        stable_pipeline.reset()
        print("≡ƒñû Stable Pipeline reset")
    except Exception as e:
        print(f"ΓÜá∩╕Å  Pipeline reset error: {e}")
    
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
        "ai_pipeline_active": True,  # stable_pipeline is always active (singleton)
        "camera_state": camera_manager.get_state()
    }


@api_router.get("/intelligence")
def get_intelligence_status():
    """Get detailed Intelligence Layer status and metrics"""
    # Stable pipeline uses context reasoning instead of intelligence layer
    return {
        "status": "ACTIVE",
        "pipeline": "stable_production_pipeline",
        "features": ["OpenVINO ONNX Inference", "ByteTrack", "Context Reasoning"],
        "static_filtering": "enabled"
    }


@api_router.get("/status")
def get_status():
    """Get current system status with Stable Pipeline data"""
    camera_state = camera_manager.get_state()
    pipeline_stats = stable_pipeline.get_pipeline_stats()
    
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
    
    Returns alerts generated by Reasoning Agent from context analysis
    """
    alerts = stable_pipeline.get_recent_alerts(limit)
    
    return {
        "total": len(alerts),
        "alerts": alerts
    }


@api_router.get("/detections")
def get_detections(since: float = 0):
    """
    Live detection feed ΓÇö returns recent object sightings.
    Frontend polls this to show Instagram/YouTube-style live messages.
    
    Query params:
        since: Unix timestamp ΓÇö only return detections after this time
    """
    detections = stable_pipeline.get_recent_detections(since=since, limit=60)
    return {
        "detections": detections,
        "server_time": __import__("time").time()
    }


@api_router.get("/evidence/list")
def get_evidence_list(limit: int = 50, severity: Optional[str] = None):
    """
    Get list of recorded evidence clips
    Note: Evidence recording not yet implemented in stable pipeline
    """
    # TODO: Add evidence_recorder to stable_pipeline
    return {
        "total": 0,
        "evidence": [],
        "message": "Evidence recording coming soon in stable pipeline"
    }


@api_router.get("/evidence/{event_id}")
def get_evidence_by_id(event_id: str):
    """Get specific evidence clip metadata"""
    # TODO: Add evidence_recorder to stable_pipeline
    return {"error": "Evidence recording coming soon", "event_id": event_id}


@api_router.get("/evidence/{event_id}/video")
def stream_evidence_video(event_id: str):
    """Stream recorded evidence video"""
    # TODO: Add evidence_recorder to stable_pipeline
    return {"error": "Evidence recording coming soon", "event_id": event_id}


@api_router.delete("/evidence/{event_id}")
def delete_evidence(event_id: str):
    """Delete evidence clip"""
    # TODO: Add evidence_recorder to stable_pipeline
    return {"error": "Evidence recording coming soon", "event_id": event_id}


@api_router.get("/intelligence/events")
def get_intelligence_events(limit: int = 50):
    """
    Get reasoning events from the production-grade event pipeline.
    
    This endpoint serves AI-generated behavioral events (loitering, theft,
    intrusion, zone violations) with human-readable reasoning text.
    
    Query params:
        limit: Maximum number of events to return (default: 50)
    
    Returns:
        {
            "status": "active",
            "total": 12,
            "events": [
                {
                    "event_id": 1,
                    "event_type": "LOITERING",
                    "severity": "MEDIUM",
                    "track_id": 42,
                    "reasoning_text": "Subject ID 42 remained stationary...",
                    "timestamp": "2024-01-15T10:30:45",
                    "severity_score": 0.68,
                    "duration": 18.5,
                    "context": {"zone": "entrance"}
                },
                ...
            ]
        }
    """
    events = get_events(limit)
    return {
        "status": "active",
        "total": len(events),
        "events": events
    }


@api_router.post("/intelligence/events/test")
def publish_test_events():
    """
    Publish sample test events (for development/testing only).
    
    This endpoint creates 5 sample events to test the pipeline without
    needing to run the camera. Remove in production.
    """
    test_events = [
        (EventType.LOITERING, EventSeverity.MEDIUM, 42, 0.68, 18.5),
        (EventType.ZONE_VIOLATION, EventSeverity.HIGH, 15, 0.82, 5.2),
        (EventType.INTRUSION, EventSeverity.CRITICAL, 7, 0.95, 12.0),
        (EventType.FIGHT, EventSeverity.CRITICAL, 23, 0.91, 8.7),
        (EventType.THEFT, EventSeverity.HIGH, 33, 0.79, 25.3)
    ]
    
    published_count = 0
    for event_type, severity, track_id, score, duration in test_events:
        reasoning = generate_reasoning_text(event_type, track_id, duration, {})
        publish_event(event_type, severity, track_id, score, duration, reasoning)
        published_count += 1
    
    return {
        "status": "success",
        "message": f"Published {published_count} test events",
        "total_events_in_store": len(get_events(50))
    }



# Include API router in the app
app.include_router(api_router)

# Keep root endpoint without /api prefix for health checks
# Root endpoint already defined above at line 249-259
# This duplicate definition has been removed

