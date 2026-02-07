"""
Production AI Pipeline - Complete Integration
camera → tracker → event_detector → agent → recorder → UI

NO DUMMY DATA - Everything is real

Data Flow:
1. Frame from camera
2. YOLOv8 + ByteTrack tracking
3. Event detection (motion, loitering, ROI breach, etc.)
4. AI Agent reasoning and escalation
5. Evidence recording (if needed)
6. Real-time alerts to frontend
"""

import cv2
import time
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import deque
import logging

from core.object_tracker import tracker
from core.event_detector import event_detector
from core.security_agent import security_agent
from core.evidence_recorder import evidence_recorder

logger = logging.getLogger(__name__)


class ProductionPipeline:
    """
    Production-grade AI processing pipeline
    
    Thread-safe, non-blocking, handles full security intelligence workflow
    """
    
    def __init__(self):
        """Initialize production pipeline"""
        # Use global singletons (already initialized)
        self.tracker = tracker
        self.event_detector = event_detector
        self.agent = security_agent
        self.recorder = evidence_recorder
        
        # Pipeline state
        self.frame_count = 0
        self.start_time = time.time()
        self.fps_history = deque(maxlen=30)
        
        # Alert queue for frontend
        self.alert_queue: List[Dict] = []
        self.max_alert_history = 100
        
        # Performance metrics
        self.metrics = {
            "total_frames": 0,
            "total_detections": 0,
            "total_events": 0,
            "total_alerts": 0,
            "total_recordings": 0,
            "avg_fps": 0.0
        }
        
        logger.info("🚀 ProductionPipeline initialized")
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Process single frame through complete pipeline
        
        Args:
            frame: Input BGR image
            
        Returns:
            Tuple of (annotated_frame, pipeline_data)
        """
        start_time = time.time()
        self.frame_count += 1
        self.metrics["total_frames"] += 1
        
        # STEP 1: Add frame to evidence pre-buffer
        self.recorder.add_frame(frame)
        
        # STEP 2: Object Detection + Tracking (YOLOv8 + ByteTrack)
        annotated_frame, tracked_objects = self.tracker.track(frame)
        self.metrics["total_detections"] += len(tracked_objects)
        
        # STEP 3: Event Detection
        events = self.event_detector.detect_events(tracked_objects, frame.shape)
        self.metrics["total_events"] += len(events)
        
        # STEP 4: AI Agent Analysis & Decision Making
        alerts = []
        for event in events:
            # Add timestamp_unix for agent processing
            event_dict = event.to_dict() if hasattr(event, 'to_dict') else event
            event_dict["timestamp_unix"] = time.time()
            
            # Agent analyzes event and makes decision
            decision = self.agent.analyze_event(event_dict)
            
            # Log decision
            if decision.action.value == "ALERT":
                logger.info(
                    f"🚨 ALERT: {event_dict['event_type']} | "
                    f"Severity: {decision.severity} | "
                    f"Confidence: {decision.confidence:.2f}"
                )
            
            # STEP 5: Evidence Recording
            if decision.should_record:
                recording_started = self.recorder.start_recording(
                    event_id=event_dict["event_id"],
                    event_data=event_dict,
                    duration=decision.recording_duration
                )
                
                if recording_started:
                    self.metrics["total_recordings"] += 1
            
            # STEP 6: Alert Queue Management
            if decision.action.value in ["ALERT", "RECORD"]:
                alert = {
                    "alert_id": event_dict["event_id"],
                    "event": event_dict,
                    "decision": {
                        "action": decision.action.value,
                        "confidence": decision.confidence,
                        "severity": decision.severity,
                        "reasoning": decision.reasoning,
                        "message": decision.alert_message,
                        "metadata": decision.metadata
                    },
                    "timestamp": event_dict["timestamp"],
                    "status": "ACTIVE"
                }
                alerts.append(alert)
                self.alert_queue.append(alert)
                self.metrics["total_alerts"] += 1
        
        # Keep alert queue bounded
        if len(self.alert_queue) > self.max_alert_history:
            self.alert_queue = self.alert_queue[-self.max_alert_history:]
        
        # STEP 7: Update Active Recordings
        self.recorder.update_recordings(frame)
        
        # Calculate FPS
        elapsed = time.time() - start_time
        fps = 1.0 / elapsed if elapsed > 0 else 0
        self.fps_history.append(fps)
        self.metrics["avg_fps"] = float(np.mean(self.fps_history))
        
        # Compile pipeline data
        pipeline_data = {
            "frame_number": self.frame_count,
            "fps": self.metrics["avg_fps"],
            "tracked_objects": len(tracked_objects),
            "active_tracks": len(self.tracker.get_active_tracks()),
            "loitering_tracks": len(self.tracker.get_loitering_tracks()),
            "events_detected": len(events),
            "alerts_raised": len(alerts),
            "active_recordings": len(self.agent.get_active_recordings()),
            "alerts": alerts,
            "metrics": self.metrics
        }
        
        # Add overlay with pipeline stats
        annotated_frame = self._draw_pipeline_stats(annotated_frame, pipeline_data)
        
        return annotated_frame, pipeline_data
    
    def _draw_pipeline_stats(self, frame: np.ndarray, data: Dict) -> np.ndarray:
        """Draw production pipeline statistics on frame"""
        height, width = frame.shape[:2]
        
        # Background panel
        panel_height = 100
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, panel_height), (20, 20, 20), -1)
        frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
        
        # Stats
        stats = [
            f"FPS: {data['fps']:.1f}",
            f"Tracks: {data['tracked_objects']} ({data['active_tracks']} active)",
            f"Events: {data['events_detected']}",
            f"Alerts: {data['alerts_raised']}",
            f"Recording: {data['active_recordings']}",
        ]
        
        y = 20
        for stat in stats:
            cv2.putText(frame, stat, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0, 255, 255), 1)
            y += 18
        
        # Loitering warning
        if data['loitering_tracks'] > 0:
            cv2.putText(frame, f"⚠️ LOITERING: {data['loitering_tracks']}", 
                       (width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (0, 0, 255), 2)
        
        # Active alerts
        if data['alerts_raised'] > 0:
            cv2.putText(frame, "🚨 ALERT", (width - 200, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        return frame
    
    def get_recent_alerts(self, limit: int = 50) -> List[Dict]:
        """Get recent alerts for frontend"""
        return self.alert_queue[-limit:] if self.alert_queue else []
    
    def get_evidence_list(self, limit: int = 50, severity: Optional[str] = None) -> List[Dict]:
        """Get evidence clips"""
        return self.recorder.get_evidence_list(limit, severity)
    
    def get_pipeline_stats(self) -> Dict:
        """Get comprehensive pipeline statistics"""
        return {
            "pipeline": {
                "uptime": time.time() - self.start_time,
                "frame_count": self.frame_count,
                "fps": self.metrics["avg_fps"]
            },
            "tracker": self.tracker.get_stats(),
            "agent": self.agent.get_stats(),
            "recorder": self.recorder.get_stats(),
            "metrics": self.metrics
        }
    
    def reset(self):
        """Reset pipeline state"""
        logger.info("🔄 Resetting ProductionPipeline")
        self.tracker.reset()
        self.event_detector.reset()
        self.agent.reset()
        self.recorder.reset()
        
        self.frame_count = 0
        self.start_time = time.time()
        self.alert_queue.clear()
        
        self.metrics = {
            "total_frames": 0,
            "total_detections": 0,
            "total_events": 0,
            "total_alerts": 0,
            "total_recordings": 0,
            "avg_fps": 0.0
        }


# Global singleton
production_pipeline = ProductionPipeline()
