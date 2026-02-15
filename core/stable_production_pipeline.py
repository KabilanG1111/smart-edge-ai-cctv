"""
Stable Production AI Pipeline
OpenVINO + ByteTrack + Context Reasoning

Deterministic, enterprise-grade surveillance intelligence
NO per-frame decisions - temporal logic only
"""

import cv2
import numpy as np
import time
import yaml
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from collections import deque
import logging

from core.openvino_inference import create_inference_engine
from core.context_reasoning import ContextEngine, ReasoningAgent, AlertLevel

logger = logging.getLogger(__name__)


class ByteTrackIntegration:
    """
    Lightweight ByteTrack wrapper for multi-object tracking
    Provides persistent track IDs across frames
    """
    
    def __init__(self, track_thresh: float = 0.5, track_buffer: int = 30):
        """
        Initialize ByteTrack
        
        Args:
            track_thresh: Detection confidence threshold for tracking
            track_buffer: Number of frames to keep lost tracks
        """
        try:
            from boxmot import ByteTrack as BYTETracker
            self.tracker = BYTETracker(
                track_thresh=track_thresh,
                track_buffer=track_buffer,
                match_thresh=0.8,
                frame_rate=30
            )
            logger.info("✅ ByteTrack initialized")
        except ImportError:
            logger.warning("⚠️ boxmot not installed. Using fallback tracker.")
            self.tracker = None
    
    def update(self, detections: List, frame_shape: Tuple[int, int]) -> List:
        """
        Update tracker with new detections
        
        Args:
            detections: List of Detection objects
            frame_shape: (height, width)
            
        Returns:
            List of tracked detections with track_id
        """
        if self.tracker is None:
            # Fallback: assign sequential IDs
            for i, det in enumerate(detections):
                det.track_id = i
            return detections
        
        if len(detections) == 0:
            return []
        
        # Convert to ByteTrack format: [x1, y1, x2, y2, conf, class_id]
        dets_array = np.array([
            [*det.bbox, det.confidence, det.class_id]
            for det in detections
        ])
        
        # Update tracker
        tracks = self.tracker.update(dets_array, frame_shape)
        
        # Map track IDs back to detections
        for i, track in enumerate(tracks):
            if i < len(detections):
                detections[i].track_id = int(track[4])  # Track ID is 5th column
        
        return detections


class StableProductionPipeline:
    """
    Production-grade AI surveillance pipeline
    
    Pipeline flow:
    1. GStreamer → Frame Buffer
    2. OpenVINO ONNX Inference (YOLOv8)
    3. ByteTrack Multi-Object Tracking
    4. Context Engine (track history accumulation)
    5. Reasoning Agent (temporal logic)
    6. Decision Engine (NORMAL/WARNING/SUSPICIOUS)
    """
    
    def __init__(
        self,
        model_path: str = "models/openvino/yolov8s.xml",  # Using SMALL model for better accuracy
        zone_config_path: str = "config/zones.yaml",
        use_openvino: bool = True,
        conf_threshold: float = 0.20,  # Lowered to 20% for better detection coverage
        input_size: int = 640  # Increased to 640 for production-grade accuracy
    ):
        """
        Initialize stable production pipeline
        
        Args:
            model_path: Path to OpenVINO IR (.xml) or PyTorch (.pt)
            zone_config_path: Path to zone definitions YAML
            use_openvino: Try to use OpenVINO if available
            conf_threshold: Detection confidence threshold (20% = more detections, 50% = fewer but more confident)
            input_size: Model input size (320 for speed, 640 for accuracy)
        """
        logger.info("=" * 60)
        logger.info("🏢 STABLE PRODUCTION PIPELINE INITIALIZATION")
        logger.info("=" * 60)
        
        # Auto-fallback to PyTorch if OpenVINO model not found
        model_path_obj = Path(model_path)
        if not model_path_obj.exists():
            logger.warning(f"⚠️ OpenVINO model not found: {model_path}")
            logger.info("📦 Falling back to PyTorch YOLOv8")
            # Try common YOLOv8 model paths (prefer SMALL model for better accuracy)
            fallback_paths = ["yolov8s.pt", "yolov8n.pt", "models/yolov8s.pt", "models/yolov8n.pt"]
            for fallback in fallback_paths:
                if Path(fallback).exists():
                    model_path = fallback
                    use_openvino = False
                    logger.info(f"✅ Using PyTorch model: {model_path}")
                    break
            else:
                logger.warning("❌ No YOLOv8 model found locally!")
                logger.info("📥 Auto-downloading YOLOv8-SMALL for better accuracy...")
                model_path = "yolov8s.pt"  # Will auto-download SMALL model (11MB vs 6MB nano)
                use_openvino = False
        
        # Load zone configuration
        zone_config = self._load_zone_config(zone_config_path)
        zones = {
            name: cfg["coordinates"]
            for name, cfg in zone_config.get("zones", {}).items()
        }
        
        # Initialize components
        self.inference_engine = create_inference_engine(
            model_path,
            use_openvino=use_openvino,
            conf_threshold=conf_threshold,
            input_size=input_size
        )
        
        self.tracker = ByteTrackIntegration()
        
        self.context_engine = ContextEngine(
            zone_definitions=zones,
            stationary_threshold=zone_config["settings"]["stationary_threshold"],
            loitering_time=zone_config["settings"]["loitering_timeout_default"]
        )
        
        self.reasoning_agent = ReasoningAgent(
            alert_cooldown=zone_config["settings"]["alert_cooldown"],
            warning_threshold=zone_config["settings"]["warning_threshold"],
            suspicious_threshold=zone_config["settings"]["suspicious_threshold"]
        )
        
        # Performance tracking
        self.frame_count = 0
        self.fps_history = deque(maxlen=30)
        self.start_time = time.time()
        
        # Alert queue for frontend
        self.alert_queue = deque(maxlen=100)
        self.detection_feed = deque(maxlen=200)
        
        # State tracking
        self.last_announced = {}  # track_id → last_announce_time
        self.announce_cooldown = 3.0  # seconds
        
        logger.info("✅ Stable Production Pipeline initialized")
        logger.info("=" * 60)
    
    def _load_zone_config(self, config_path: str) -> dict:
        """Load zone configuration from YAML"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"📋 Loaded zone config from {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"⚠️ Zone config not found: {config_path}. Using defaults.")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Default configuration if YAML not found"""
        return {
            "zones": {
                "entrance": {"coordinates": [0, 0, 320, 240]},
                "restricted": {"coordinates": [480, 0, 640, 240]},
                "main_area": {"coordinates": [0, 240, 640, 480]}
            },
            "settings": {
                "loiter ing_timeout_default": 120,
                "stationary_threshold": 5.0,
                "warning_threshold": 0.3,
                "suspicious_threshold": 0.7,
                "alert_cooldown": 120
            }
        }    
    def annotate_frame(self, frame: np.ndarray, detections: List, tracked_detections: List) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: Input BGR image
            detections: Raw detections from inference
            tracked_detections: Detections with track IDs
            
        Returns:
            Annotated frame with bounding boxes
        """
        annotated = frame.copy()
        
        # Color scheme
        COLOR_BOX = (0, 255, 0)  # Green
        COLOR_TEXT = (0, 255, 0)  # Green
        COLOR_TRACK_ID = (0, 255, 255)  # Cyan
        
        for det in tracked_detections:
            # Extract bbox coordinates
            x1, y1, x2, y2 = map(int, det.bbox)
            
            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), COLOR_BOX, 2)
            
            # Prepare label text
            conf_pct = int(det.confidence * 100)
            label = f"{det.class_name} {conf_pct}%"
            
            # Add track ID if available
            if hasattr(det, 'track_id'):
                label += f" ID:{det.track_id}"
            
            # Draw label background
            (label_w, label_h), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                annotated,
                (x1, y1 - label_h - 10),
                (x1 + label_w, y1),
                COLOR_BOX,
                -1
            )
            
            # Draw label text
            cv2.putText(
                annotated,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),  # Black text on green background
                2
            )
        
        # Add frame info overlay
        info_text = f"Detections: {len(tracked_detections)} | Frame: {self.frame_count}"
        cv2.putText(
            annotated,
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        return annotated    
    def process_frame(self, frame: np.ndarray, annotate: bool = True) -> Tuple[np.ndarray, Dict]:
        """
        Process single frame through complete pipeline
        
        Args:
            frame: Input BGR image
            annotate: If True, draw bounding boxes on returned frame
            
        Returns:
            Tuple of (frame, pipeline_data)
            Frame will be annotated if annotate=True, clean if False
        """
        start_time = time.time()
        self.frame_count += 1
        timestamp = time.time()
        
        # STEP 1: OpenVINO Inference (YOLOv8 ONNX)
        detections = self.inference_engine.infer(frame)
        
        # 🔎 DEBUG: Log detection count every 30 frames
        if self.frame_count % 30 == 0:
            logger.info(f"Frame {self.frame_count}: {len(detections)} raw detections")
        
        # STEP 2: ByteTrack Multi-Object Tracking
        tracked_detections = self.tracker.update(detections, frame.shape[:2])
        
        # STEP 3: Context Engine - Update track states
        alerts = []
        for det in tracked_detections:
            if not hasattr(det, 'track_id'):
                continue
            
            # Update track context
            track_state = self.context_engine.update_track(
                track_id=det.track_id,
                class_name=det.class_name,
                confidence=det.confidence,
                bbox=det.bbox,
                timestamp=timestamp
            )
            
            # Extract behavioral features
            features = self.context_engine.extract_features(det.track_id)
            if features is None:
                continue
            
            # STEP 4: AI Reasoning Agent
            alert_level, intent_score, reasoning = self.reasoning_agent.analyze_track(
                track_state, features
            )
            
            # Update track state
            track_state.alert_level = alert_level
            track_state.intent_score = intent_score
            track_state.reasoning = reasoning
            
            # STEP 5: Decision Engine - Should we alert?
            if self.reasoning_agent.should_alert(track_state, alert_level):
                # Create alert
                alert = {
                    "alert_id": f"AL-{int(timestamp)}-{det.track_id}",
                    "track_id": det.track_id,
                    "alert_level": alert_level.value,
                    "intent_score": round(intent_score, 3),
                    "class_name": det.class_name,
                    "confidence": round(det.confidence, 3),
                    "duration": round(track_state.duration, 1),
                    "reasoning": reasoning,
                    "zone": track_state.current_zone,
                    "timestamp": timestamp
                }
                
                alerts.append(alert)
                self.alert_queue.append(alert)
                
                # Update last alert time
                track_state.last_alert_time = timestamp
                
                # Log alert
                logger.warning(
                    f"🚨 {alert_level.value} | Track {det.track_id} | "
                    f"Score: {intent_score:.2f} | {', '.join(reasoning)}"
                )
            
            # Detection feed (throttled per track)
            now = time.time()
            last_announce = self.last_announced.get(det.track_id, 0)
            if now - last_announce >= self.announce_cooldown:
                self.last_announced[det.track_id] = now
                self.detection_feed.append({
                    "id": f"{self.frame_count}-{det.track_id}",
                    "class": det.class_name,
                    "confidence": round(det.confidence * 100),
                    "track_id": det.track_id,
                    "timestamp": now,
                    "duration": round(track_state.duration, 1),
                    "is_new": track_state.duration < 1.0,
                    "alert_level": alert_level.value
                })
        
        # Cleanup stale announce entries
        stale_ids = [
            tid for tid, t in self.last_announced.items()
            if timestamp - t > 30
        ]
        for tid in stale_ids:
            del self.last_announced[tid]
        
        # Calculate FPS
        elapsed = time.time() - start_time
        fps = 1.0 / elapsed if elapsed > 0 else 0
        self.fps_history.append(fps)
        
        # Compile pipeline data
        pipeline_data = {
            "frame_number": self.frame_count,
            "fps": float(np.mean(self.fps_history)) if self.fps_history else 0,
            "detections": len(detections),
            "tracked_objects": len(tracked_detections),
            "active_tracks": len(self.context_engine.get_all_tracks()),
            "alerts": alerts,
            "alert_counts": {
                "WARNING": sum(1 for a in self.alert_queue if a["alert_level"] == "WARNING"),
                "SUSPICIOUS": sum(1 for a in self.alert_queue if a["alert_level"] == "SUSPICIOUS")
            }
        }
        
        # Return annotated frame if requested (default behavior)
        if annotate:
            annotated_frame = self.annotate_frame(frame, detections, tracked_detections)
            return annotated_frame, pipeline_data
        else:
            # Return clean frame (for privacy/recording)
            return frame.copy(), pipeline_data
    
    def get_recent_detections(self, since: float = 0, limit: int = 60) -> List[Dict]:
        """Get recent detection feed entries"""
        results = [d for d in self.detection_feed if d["timestamp"] > since]
        return list(results)[-limit:]
    
    def get_recent_alerts(self, limit: int = 50) -> List[Dict]:
        """Get recent alerts"""
        return list(self.alert_queue)[-limit:]
    
    def get_pipeline_stats(self) -> Dict:
        """Get comprehensive pipeline statistics"""
        inference_stats = self.inference_engine.get_stats()
        
        return {
            "pipeline": {
                "uptime": time.time() - self.start_time,
                "frame_count": self.frame_count,
                "fps": float(np.mean(self.fps_history)) if self.fps_history else 0
            },
            "inference": inference_stats,
            "tracking": {
                "active_tracks": len(self.context_engine.get_all_tracks())
            },
            "alerts": {
                "total_in_queue": len(self.alert_queue),
                "warning_count": sum(1 for a in self.alert_queue if a["alert_level"] == "WARNING"),
                "suspicious_count": sum(1 for a in self.alert_queue if a["alert_level"] == "SUSPICIOUS")
            }
        }
    
    def reset(self):
        """Reset pipeline state"""
        logger.info("🔄 Resetting Stable Production Pipeline")
        self.context_engine.reset()
        self.frame_count = 0
        self.alert_queue.clear()
        self.detection_feed.clear()
        self.last_announced.clear()


# Global singleton
stable_pipeline = StableProductionPipeline()
