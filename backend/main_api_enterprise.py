"""
🏢 ENTERPRISE BACKEND API
========================

FastAPI backend for billion-dollar-grade Edge AI CCTV system

Features:
- Multi-stage detection pipeline (YOLOv8 + Grounding DINO)
- Open vocabulary detection (10,000+ classes)
- Temporal reasoning (no flicker)
- Real-time metrics
- Enterprise logging
- Evidence recording

Performance: 30 FPS target on Intel i5 CPU
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from typing import Dict, List, Optional
import logging
import time
from pathlib import Path

# Enterprise pipeline
from core.enterprise_pipeline import get_pipeline, Detection
from core.camera_lifecycle_manager import camera_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/enterprise.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory
Path('logs').mkdir(exist_ok=True)

# FastAPI app
app = FastAPI(
    title="Enterprise Edge AI CCTV System",
    description="Billion-dollar-grade object detection with open vocabulary (10,000+ classes)",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
pipeline = None
is_processing = False


@app.on_event("startup")
async def startup_event():
    """Initialize enterprise pipeline on startup"""
    global pipeline
    try:
        logger.info("🚀 Starting Enterprise Edge AI CCTV System v2.0")
        logger.info("=" * 60)
        
        # Initialize pipeline
        pipeline = get_pipeline()
        
        logger.info("=" * 60)
        logger.info("✅ Enterprise system ready")
        logger.info("🌐 API: http://localhost:8000")
        logger.info("📖 Docs: http://localhost:8000/docs")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise


@app.get("/")
async def root():
    """System info"""
    return {
        "service": "Enterprise Edge AI CCTV System",
        "version": "2.0.0",
        "description": "Multi-stage detection with open vocabulary (10,000+ classes)",
        "architecture": {
            "stage1": "YOLOv8 ONNX + OpenVINO (Dynamic agents)",
            "stage2": "Grounding DINO (Open vocabulary)",
            "stage3": "Temporal reasoning + Embedding memory"
        },
        "status": "operational",
        "docs": "/docs"
    }


@app.post("/api/start")
async def start_camera():
    """Start camera stream"""
    try:
        success = camera_manager.start_camera(camera_index=0)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to start camera")
        
        return {
            "status": "started",
            "camera_index": 0,
            "message": "Camera stream started successfully"
        }
        
    except Exception as e:
        logger.error(f"Camera start failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/stop")
async def stop_camera():
    """Stop camera stream"""
    global is_processing
    is_processing = False
    camera_manager.stop_camera()
    
    return {
        "status": "stopped",
        "message": "Camera stream stopped"
    }


@app.get("/api/status")
async def get_status():
    """Get system status"""
    camera_active = camera_manager.is_camera_active()
    
    status = {
        "camera": "active" if camera_active else "inactive",
        "camera_opened": camera_active,
        "processing": is_processing,
        "pipeline_initialized": pipeline is not None
    }
    
    # Add performance metrics if pipeline is active
    if pipeline:
        metrics = pipeline.get_metrics()
        status.update({
            "performance": metrics
        })
    
    return status


@app.get("/api/metrics")
async def get_metrics():
    """Get detailed performance metrics"""
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    metrics = pipeline.get_metrics()
    
    # Add system metrics
    metrics.update({
        "timestamp": time.time(),
        "camera_active": camera_manager.is_camera_active(),
        "processing": is_processing
    })
    
    return metrics


@app.get("/api/live")
async def live_stream():
    """Live video stream with enterprise detection"""
    
    def gen_frames():
        global is_processing
        is_processing = True
        
        logger.info("🎥 Starting live stream with enterprise pipeline")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while is_processing:
                # Get frame from camera
                frame = camera_manager.get_frame()
                if frame is None:
                    logger.warning("No frame from camera")
                    time.sleep(0.1)
                    continue
                
                # Process through enterprise pipeline
                try:
                    annotated, detections, metrics = pipeline.process_frame(frame)
                    
                    # Log every 30 frames
                    frame_count += 1
                    if frame_count % 30 == 0:
                        elapsed = time.time() - start_time
                        avg_fps = frame_count / elapsed
                        logger.info(
                            f"Frame {frame_count} | "
                            f"FPS: {metrics.get('fps', 0):.1f} | "
                            f"Detections: {len(detections)} | "
                            f"Tracks: {metrics.get('active_tracks', 0)} | "
                            f"Locked: {metrics.get('locked_tracks', 0)}"
                        )
                    
                    # Draw metrics overlay
                    annotated = _draw_metrics(annotated, metrics, len(detections))
                    
                except Exception as e:
                    logger.error(f"Pipeline error: {e}")
                    annotated = frame
                
                # Encode frame
                ret, buffer = cv2.imencode('.jpg', annotated, [
                    cv2.IMWRITE_JPEG_QUALITY, 85
                ])
                
                if not ret:
                    continue
                
                # Yield frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        except Exception as e:
            logger.error(f"Stream error: {e}")
        
        finally:
            is_processing = False
            logger.info(f"🛑 Stream stopped | Total frames: {frame_count}")
    
    return StreamingResponse(
        gen_frames(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )


@app.get("/api/detections")
async def get_current_detections():
    """Get current frame detections (JSON)"""
    if not camera_manager.is_camera_active():
        raise HTTPException(status_code=503, detail="Camera not active")
    
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    # Get frame and process
    frame = camera_manager.get_frame()
    if frame is None:
        raise HTTPException(status_code=503, detail="No frame available")
    
    _, detections, metrics = pipeline.process_frame(frame)
    
    # Convert detections to JSON
    detection_list = []
    for det in detections:
        detection_list.append({
            "bbox": det.bbox,
            "confidence": round(det.confidence, 3),
            "class_name": det.class_name,
            "track_id": det.track_id,
            "stage": det.stage,
            "locked": _is_track_locked(det.track_id) if det.track_id else False
        })
    
    return {
        "timestamp": time.time(),
        "detections": detection_list,
        "count": len(detection_list),
        "metrics": metrics
    }


@app.get("/api/config")
async def get_config():
    """Get current pipeline configuration"""
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    return {
        "use_openvino": pipeline.use_openvino,
        "target_fps": pipeline.target_fps,
        "confidence_threshold": pipeline.confidence_threshold,
        "enable_stage2": pipeline.enable_stage2,
        "yolo_model": "yolov8s_fp16.xml" if pipeline.use_openvino else "yolov8s.pt",
        "stage2_status": "enabled" if pipeline.grounding_dino else "disabled",
        "prompt_classes_count": len(pipeline.prompt_classes) if pipeline.enable_stage2 else 0
    }


@app.post("/api/config")
async def update_config(
    confidence_threshold: Optional[float] = None,
    enable_stage2: Optional[bool] = None
):
    """Update pipeline configuration (hot reload)"""
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    updated = {}
    
    if confidence_threshold is not None:
        pipeline.confidence_threshold = confidence_threshold
        updated["confidence_threshold"] = confidence_threshold
    
    if enable_stage2 is not None:
        pipeline.enable_stage2 = enable_stage2
        updated["enable_stage2"] = enable_stage2
    
    logger.info(f"Configuration updated: {updated}")
    
    return {
        "status": "updated",
        "changes": updated,
        "message": "Configuration updated successfully"
    }


def _draw_metrics(frame: np.ndarray, metrics: Dict, detection_count: int) -> np.ndarray:
    """Draw performance metrics overlay"""
    overlay = frame.copy()
    
    # Background
    cv2.rectangle(overlay, (10, 10), (350, 140), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # Text
    fps = metrics.get('fps', 0)
    stage1_ms = metrics.get('stage1_ms', 0)
    stage2_ms = metrics.get('stage2_ms', 0)
    stage3_ms = metrics.get('stage3_ms', 0)
    active_tracks = metrics.get('active_tracks', 0)
    locked_tracks = metrics.get('locked_tracks', 0)
    
    y = 35
    cv2.putText(frame, f"FPS: {fps:.1f}", (20, y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    y += 25
    cv2.putText(frame, f"Detections: {detection_count}", (20, y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    y += 20
    cv2.putText(frame, f"Tracks: {active_tracks} (Locked: {locked_tracks})", (20, y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    y += 20
    cv2.putText(frame, f"Stage1: {stage1_ms:.1f}ms | Stage2: {stage2_ms:.1f}ms", (20, y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    y += 18
    cv2.putText(frame, f"Stage3: {stage3_ms:.1f}ms", (20, y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    return frame


def _is_track_locked(track_id: int) -> bool:
    """Check if track is locked"""
    if not pipeline or track_id not in pipeline.track_memory:
        return False
    return pipeline.track_memory[track_id].locked_class is not None


if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Enterprise Backend Server")
    logger.info("=" * 60)
    logger.info("Multi-Stage Detection Pipeline")
    logger.info("Stage 1: YOLOv8 ONNX + OpenVINO (Dynamic agents)")
    logger.info("Stage 2: Grounding DINO (Open vocabulary)")
    logger.info("Stage 3: Temporal reasoning + Embedding memory")
    logger.info("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
