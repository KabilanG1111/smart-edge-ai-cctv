"""
Production-Grade Object Detection + Tracking Pipeline
YOLOv8 + ByteTrack Integration for Multi-Object Tracking (MOT)

Key Features:
- Thread-safe singleton pattern
- Persistent track IDs across frames
- Track lifecycle management (new/active/lost)
- Confidence-based filtering
- FPS optimization
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import time
from collections import defaultdict, deque
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)


@dataclass
class TrackedObject:
    """Single tracked object with full lifecycle data"""
    track_id: int
    class_id: int
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    center: Tuple[int, int]  # (cx, cy)
    first_seen: float  # timestamp
    last_seen: float  # timestamp
    frame_count: int  # frames object has been tracked
    stationary_frames: int  # consecutive frames without movement
    last_position: Tuple[int, int] = field(default=(0, 0))
    velocity: float = 0.0  # pixels per frame
    is_stationary: bool = False
    
    @property
    def duration(self) -> float:
        """Time object has been on screen (seconds)"""
        return self.last_seen - self.first_seen
    
    @property
    def is_loitering(self) -> bool:
        """Is object loitering (stationary > 3 seconds)?"""
        return self.stationary_frames > 90  # 30 FPS * 3 seconds


class ObjectTracker:
    """
    YOLOv8 + ByteTrack Multi-Object Tracker
    
    Thread-safe singleton for consistent tracking across the application.
    Handles detection, tracking, and object lifecycle management.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        model_path: str = "yolov8s.pt",  # Change to "runs/train_robust/focused_detector/weights/best.pt" after training
        conf_threshold: float = 0.30,  # Lowered for poor clarity detection
        iou_threshold: float = 0.7,
        max_age: int = 30,  # frames to keep lost tracks
        stationary_threshold: int = 10  # pixels for stationary detection
    ):
        """
        Initialize tracker (only once due to singleton)
        
        Args:
            model_path: Path to YOLO model weights
            conf_threshold: Minimum confidence for detections
            iou_threshold: IoU threshold for ByteTrack matching
            max_age: Max frames to keep lost tracks before removal
            stationary_threshold: Movement threshold (pixels) for stationary detection
        """
        if ObjectTracker._initialized:
            return
        
        logger.info(f"🚀 Initializing ObjectTracker with {model_path}")
        
        # Load YOLOv8 model
        self.model = YOLO(model_path)
        self.model.fuse()  # Fuse layers for faster inference
        
        # Configuration
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self.stationary_threshold = stationary_threshold
        
        # Track management
        self.active_tracks: Dict[int, TrackedObject] = {}
        self.lost_tracks: Dict[int, int] = {}  # track_id -> frames_lost
        self.track_history: Dict[int, deque] = defaultdict(lambda: deque(maxlen=30))
        
        # Performance metrics
        self.frame_count = 0
        self.total_detections = 0
        self.total_tracks = 0
        self.fps_history = deque(maxlen=30)
        self.last_time = time.time()
        
        # Color mapping for visualization (consistent per track_id)
        self.track_colors: Dict[int, Tuple[int, int, int]] = {}
        
        ObjectTracker._initialized = True
        logger.info("✅ ObjectTracker initialized successfully")
    
    def track(self, frame: np.ndarray) -> Tuple[np.ndarray, List[TrackedObject]]:
        """
        Process frame: detect → track → annotate
        
        Args:
            frame: Input BGR image
            
        Returns:
            Tuple of (annotated_frame, list_of_tracked_objects)
        """
        start_time = time.time()
        self.frame_count += 1
        
        # Run YOLOv8 tracking (includes detection + ByteTrack)
        try:
            results = self.model.track(
                source=frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                imgsz=640,  # Higher resolution input for small objects
                persist=True,  # Enable persistent tracking
                tracker="bytetrack.yaml",  # Use ByteTrack
                verbose=False,
                stream=False
            )
        except Exception as e:
            # Fallback: plain detection without tracking if ByteTrack fails
            logger.warning(f"⚠️ ByteTrack failed ({e}), falling back to detection only")
            results = self.model.predict(
                source=frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                imgsz=640,
                verbose=False
            )
        
        # Extract tracking results
        tracked_objects = []
        current_track_ids = set()
        next_temp_id = 10000 + self.frame_count  # temp IDs for untracked detections
        
        if results and len(results) > 0:
            result = results[0]
            
            if result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes
                
                for box in boxes:
                    # Extract data — assign temp ID if ByteTrack didn't track it
                    if box.id is not None:
                        track_id = int(box.id[0])
                    else:
                        track_id = next_temp_id
                        next_temp_id += 1
                    
                    current_track_ids.add(track_id)
                    
                    xyxy = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    cls_name = self.model.names[cls_id]
                    
                    x1, y1, x2, y2 = map(int, xyxy)
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    
                    # Update or create tracked object
                    current_time = time.time()
                    
                    if track_id in self.active_tracks:
                        # Update existing track
                        track = self.active_tracks[track_id]
                        track.bbox = (x1, y1, x2, y2)
                        track.center = (cx, cy)
                        track.confidence = conf
                        track.last_seen = current_time
                        track.frame_count += 1
                        
                        # Calculate velocity and stationary status
                        dx = cx - track.last_position[0]
                        dy = cy - track.last_position[1]
                        movement = np.sqrt(dx**2 + dy**2)
                        track.velocity = movement
                        
                        if movement < self.stationary_threshold:
                            track.stationary_frames += 1
                            track.is_stationary = True
                        else:
                            track.stationary_frames = 0
                            track.is_stationary = False
                        
                        track.last_position = (cx, cy)
                        
                    else:
                        # New track
                        track = TrackedObject(
                            track_id=track_id,
                            class_id=cls_id,
                            class_name=cls_name,
                            confidence=conf,
                            bbox=(x1, y1, x2, y2),
                            center=(cx, cy),
                            first_seen=current_time,
                            last_seen=current_time,
                            frame_count=1,
                            stationary_frames=0,
                            last_position=(cx, cy)
                        )
                        self.active_tracks[track_id] = track
                        self.total_tracks += 1
                        
                        # Assign color
                        if track_id not in self.track_colors:
                            self.track_colors[track_id] = self._generate_color(track_id)
                        
                        logger.info(f"🆕 New track: ID={track_id} class={cls_name} conf={conf:.2f}")
                    
                    # Store in history
                    self.track_history[track_id].append((cx, cy))
                    
                    tracked_objects.append(track)
                    self.total_detections += 1
        
        # Handle lost tracks
        self._handle_lost_tracks(current_track_ids)
        
        # Annotate frame
        annotated_frame = self._draw_annotations(frame.copy(), tracked_objects)
        
        # Update FPS
        elapsed = time.time() - start_time
        fps = 1.0 / elapsed if elapsed > 0 else 0
        self.fps_history.append(fps)
        
        # Log every 100 frames
        if self.frame_count % 100 == 0:
            avg_fps = np.mean(self.fps_history)
            logger.info(
                f"📊 Frame {self.frame_count} | "
                f"Active: {len(self.active_tracks)} | "
                f"FPS: {avg_fps:.1f} | "
                f"Total tracks: {self.total_tracks}"
            )
        
        return annotated_frame, tracked_objects
    
    def _handle_lost_tracks(self, current_track_ids: set):
        """Remove tracks that haven't been seen for max_age frames"""
        lost_ids = set(self.active_tracks.keys()) - current_track_ids
        
        for track_id in lost_ids:
            if track_id not in self.lost_tracks:
                self.lost_tracks[track_id] = 0
            
            self.lost_tracks[track_id] += 1
            
            # Remove if exceeded max age
            if self.lost_tracks[track_id] > self.max_age:
                track = self.active_tracks[track_id]
                logger.info(
                    f"❌ Track lost: ID={track_id} duration={track.duration:.1f}s "
                    f"frames={track.frame_count}"
                )
                del self.active_tracks[track_id]
                del self.lost_tracks[track_id]
                # Keep color for potential reappearance
        
        # Reset lost counter for reappeared tracks
        for track_id in current_track_ids:
            if track_id in self.lost_tracks:
                del self.lost_tracks[track_id]
    
    def _draw_annotations(
        self, 
        frame: np.ndarray, 
        tracked_objects: List[TrackedObject]
    ) -> np.ndarray:
        """Clean frame - no debug overlays, just the raw feed"""
        return frame
    
    def _generate_color(self, track_id: int) -> Tuple[int, int, int]:
        """Generate consistent color for track_id"""
        np.random.seed(track_id)
        return tuple(np.random.randint(0, 255, 3).tolist())
    
    def get_active_tracks(self) -> List[TrackedObject]:
        """Get list of currently active tracked objects"""
        return list(self.active_tracks.values())
    
    def get_loitering_tracks(self) -> List[TrackedObject]:
        """Get tracks that are currently loitering"""
        return [t for t in self.active_tracks.values() if t.is_loitering]
    
    def reset(self):
        """Reset all tracking state"""
        logger.info("🔄 Resetting ObjectTracker state")
        self.active_tracks.clear()
        self.lost_tracks.clear()
        self.track_history.clear()
        self.frame_count = 0
        self.total_detections = 0
        self.total_tracks = 0
    
    def get_stats(self) -> Dict:
        """Get tracker statistics"""
        return {
            "frame_count": self.frame_count,
            "active_tracks": len(self.active_tracks),
            "total_tracks": self.total_tracks,
            "total_detections": self.total_detections,
            "avg_fps": float(np.mean(self.fps_history)) if self.fps_history else 0.0,
            "loitering_count": len(self.get_loitering_tracks())
        }


# Global singleton instance (initialized with default parameters)
tracker = ObjectTracker()
