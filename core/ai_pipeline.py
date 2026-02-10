"""
AI Processing Pipeline for Smart Edge-AI CCTV System
Integrates motion detection, ROI validation, overlay rendering, and alert logic.
Enhanced with behavioral analysis and anomaly detection.
"""

import cv2
import time
from core.motion_detector import MotionDetector
from core.behavior_analyzer import BehaviorAnalyzer
from core.intelligence_layer import IntelligenceLayer
from core.roi import inside_roi, draw_roi
from utils.timer import get_time_string
from config.settings import MIN_CONTOUR_AREA


class AIProcessingPipeline:
    """
    Unified AI pipeline that processes each frame through:
    1. Motion detection
    2. ROI validation
    3. Context classification (IDLE/MOTION/ALERT)
    4. Visual overlays (bounding boxes, labels, status, timer)
    """
    
    def __init__(self):
        self.detector = MotionDetector()
        self.behavior_analyzer = BehaviorAnalyzer(learning_window=100, sensitivity=2.0)
        self.intelligence = IntelligenceLayer(learning_window=500, adaptation_rate=0.01)
        self.state = {
            "motion_start": None,
            "status": "IDLE",
            "snapshot_taken": False,
            "last_alert_time": 0,
            "banner_text": None,
            "banner_color": None,
            "banner_start_time": None,
            "anomaly_status": None,  # Legacy anomaly detection
            "intelligence_result": None  # New Intelligence Layer result
        }
        
        # Configuration
        self.MIN_MOTION_SECONDS = 0.5
        self.COOLDOWN_SECONDS = 5
        self.BANNER_DURATION = 3
        self.BANNER_HEIGHT = 50
    
    def process_frame(self, frame):
        """
        Main processing pipeline: capture → detect → classify → return clean frame
        
        All detection/analysis runs silently in the background.
        The output is always the raw, unmodified camera frame.
        
        Args:
            frame: Raw BGR frame from camera
            
        Returns:
            processed_frame: Clean raw frame (no overlays)
        """
        current_time = time.time()
        display = frame.copy()
        
        # Step 1: Motion Detection
        boxes, thresh = self.detector.detect(frame)
        
        # Step 2: ROI Analysis & Data Collection (silent — no drawing)
        motion_detected = False
        roi_triggered = False
        motion_count = 0
        largest_area = 0
        centroids = []
        
        for (x, y, w, h) in boxes:
            motion_detected = True
            motion_count += 1
            
            # Track largest object and centroids for behavior analysis
            area = w * h
            if area > largest_area:
                largest_area = area
            centroids.append((x + w // 2, y + h // 2))
            
            # Check if motion is inside ROI
            in_roi = inside_roi(x, y, w, h)
            if in_roi:
                roi_triggered = True
            
            # All visual rendering removed — analysis is silent
        
        # Step 3: Behavioral Analysis (silent background processing)
        motion_data = {
            'motion_detected': motion_detected,
            'num_motions': motion_count,
            'largest_area': largest_area,
            'centroids': centroids,
            'roi_triggered': roi_triggered,
            'timestamp': current_time
        }
        anomaly_result = self.behavior_analyzer.analyze_frame(motion_data)
        self.state["anomaly_status"] = anomaly_result
        
        # Step 3.5: Intelligence Layer Processing
        intelligence_result = self.intelligence.process_frame(motion_data)
        self.state["intelligence_result"] = intelligence_result
        
        # Step 4: State Machine (Context Classification)
        self._update_state(motion_detected, roi_triggered, current_time, anomaly_result)
        
        # No visual overlays — return clean raw frame
        return display
    
    def _update_state(self, motion_detected, roi_triggered, current_time, anomaly_result):
        """Update internal state machine based on detections and anomalies"""
        
        if motion_detected:
            if self.state["motion_start"] is None:
                self.state["motion_start"] = current_time
                self.state["snapshot_taken"] = False
                self.state["status"] = "MOTION"
                
                # Set banner
                self.state["banner_text"] = "MOTION DETECTED"
                self.state["banner_color"] = (0, 255, 255)  # Yellow
                self.state["banner_start_time"] = current_time
        else:
            # Motion ended
            if self.state["motion_start"] is not None:
                duration = current_time - self.state["motion_start"]
                
                # Check if should trigger alert (ROI or Anomaly)
                should_alert = (roi_triggered or anomaly_result['is_anomaly'])
                
                if should_alert and (current_time - self.state["last_alert_time"]) > self.COOLDOWN_SECONDS:
                    self.state["last_alert_time"] = current_time
                    self.state["status"] = "ALERT"
                    
                    # Set alert banner based on anomaly severity
                    if anomaly_result['is_anomaly']:
                        severity = anomaly_result['severity']
                        anomaly_type = anomaly_result['anomaly_type'].upper().replace('_', ' ')
                        self.state["banner_text"] = f"⚠ ANOMALY: {anomaly_type} [{severity}]"
                        
                        # Color-coded by severity
                        if severity == 'CRITICAL':
                            self.state["banner_color"] = (0, 0, 255)  # Red
                        elif severity == 'HIGH':
                            self.state["banner_color"] = (0, 100, 255)  # Orange-Red
                        elif severity == 'MEDIUM':
                            self.state["banner_color"] = (0, 165, 255)  # Orange
                        else:
                            self.state["banner_color"] = (0, 255, 255)  # Yellow
                    else:
                        self.state["banner_text"] = "⚠ SUSPICIOUS ACTIVITY DETECTED"
                        self.state["banner_color"] = (0, 0, 255)  # Red
                    
                    self.state["banner_start_time"] = current_time
                else:
                    self.state["status"] = "IDLE"
                
                # Reset motion tracking
                self.state["motion_start"] = None
                self.state["snapshot_taken"] = False
    
    def _render_overlays(self, frame, current_time, motion_count, anomaly_result):
        """Render 2050 HUD-style minimal overlays on the frame"""
        h, w = frame.shape[:2]
        
        # 1. Draw ROI boundary with thin neon outline
        draw_roi(frame)
        
        # 2. Timestamp - minimal, bottom-left, muted
        timestamp = get_time_string()
        self._draw_hud_label(
            frame, 
            timestamp, 
            (15, h - 15), 
            (100, 100, 100),  # Muted gray
            scale=0.45,
            thickness=1
        )
        
        # 3. Status indicator - bottom-left, minimal HUD label
        status = self.state["status"]
        if status == "IDLE":
            status_color = (136, 255, 0)  # Green (BGR)
            status_text = "IDLE"
        elif status == "MOTION":
            status_color = (255, 255, 0)  # Cyan (BGR)
            status_text = "PROCESSING"
        elif status == "ALERT":
            status_color = (68, 0, 255)  # Red (BGR)
            status_text = "ANOMALY"
        else:
            status_color = (200, 200, 200)
            status_text = "UNKNOWN"
        
        self._draw_hud_label(
            frame,
            status_text,
            (15, h - 45),
            status_color,
            scale=0.5,
            thickness=1,
            bg_alpha=0.7
        )
        
        # 4. AI status - top-left, minimal HUD badge
        if anomaly_result['is_anomaly']:
            ai_text = f"{anomaly_result['anomaly_type'].upper()}"
            ai_color = (68, 0, 255) if anomaly_result['severity'] in ['CRITICAL', 'HIGH'] else (0, 165, 255)
        else:
            ai_text = "AI ACTIVE"
            ai_color = (136, 255, 0)
        
        self._draw_hud_label(
            frame,
            ai_text,
            (15, 30),
            ai_color,
            scale=0.5,
            thickness=1,
            bg_alpha=0.7
        )
        
        # 5. Motion counter - top-right, minimal
        if motion_count > 0:
            counter_text = f"OBJ: {motion_count}"
            text_size = cv2.getTextSize(counter_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            self._draw_hud_label(
                frame,
                counter_text,
                (w - text_size[0] - 20, 30),
                (255, 255, 0),  # Cyan
                scale=0.5,
                thickness=1,
                bg_alpha=0.7
            )
        
        return frame
    
    def _draw_hud_label(self, frame, text, position, color, scale=0.5, thickness=1, bg_alpha=0.7):
        """Draw a HUD-style label with semi-transparent background"""
        x, y = position
        
        # Get text dimensions
        text_size, baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)
        text_w, text_h = text_size
        
        # Background padding
        padding = 6
        bg_x1 = x - padding
        bg_y1 = y - text_h - padding
        bg_x2 = x + text_w + padding
        bg_y2 = y + padding
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (bg_x1, bg_y1), (bg_x2, bg_y2), (0, 0, 0), -1)
        cv2.addWeighted(overlay, bg_alpha, frame, 1 - bg_alpha, 0, frame)
        
        # Draw border (thin cyan outline)
        cv2.rectangle(frame, (bg_x1, bg_y1), (bg_x2, bg_y2), (255, 255, 0), 1, cv2.LINE_AA)
        
        # Draw text with anti-aliasing
        cv2.putText(
            frame,
            text,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            color,
            thickness,
            cv2.LINE_AA
        )
    
    def reset(self):
        """Reset pipeline state (useful when stopping/restarting stream)"""
        if hasattr(self, 'intelligence'):
            self.intelligence.reset()
        self.detector = MotionDetector()
        self.behavior_analyzer = BehaviorAnalyzer(learning_window=100, sensitivity=2.0)
        self.state = {
            "motion_start": None,
            "status": "IDLE",
            "snapshot_taken": False,
            "last_alert_time": 0,
            "banner_text": None,
            "banner_color": None,
            "banner_start_time": None,
            "anomaly_status": None
        }
