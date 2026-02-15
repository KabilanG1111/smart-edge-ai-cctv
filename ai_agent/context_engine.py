"""
🧠 BEHAVIORAL CONTEXT ENGINE
=============================

Tracks object history and analyzes behavioral patterns over time.

Capabilities:
- Object trajectory tracking
- Motion velocity/direction analysis
- Dwell time computation
- Loitering detection
- Sudden acceleration/deceleration
- Abnormal movement patterns
- Object disappearance tracking
- State change detection

CPU Optimizations:
- NumPy vectorized operations
- Circular buffer for memory efficiency
- Lazy computation of expensive metrics
- Thread-safe design with RLock
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
import logging

logger = logging.getLogger(__name__)


@dataclass
class ObjectState:
    """Complete state representation of a tracked object"""
    track_id: int
    class_name: str
    first_seen: datetime
    last_seen: datetime
    
    # Spatial history (circular buffer for memory efficiency)
    positions: deque = field(default_factory=lambda: deque(maxlen=300))  # 10 sec at 30fps
    bboxes: deque = field(default_factory=lambda: deque(maxlen=300))
    confidences: deque = field(default_factory=lambda: deque(maxlen=50))
    
    # Motion metrics (lazy computed)
    _velocity: Optional[Tuple[float, float]] = None
    _acceleration: Optional[float] = None
    _direction: Optional[float] = None
    _distance_traveled: Optional[float] = None
    
    # Behavioral flags
    is_loitering: bool = False
    is_accelerating: bool = False
    disappeared: bool = False
    dwell_time: float = 0.0
    motion_pattern: str = "NORMAL"  # NORMAL, ERRATIC, STOPPED, FAST
    
    # Zone interactions
    zones_entered: Set[str] = field(default_factory=set)
    zones_exited: Set[str] = field(default_factory=set)
    current_zone: Optional[str] = None
    
    def get_centroid(self) -> Optional[Tuple[float, float]]:
        """Get latest centroid position"""
        return self.positions[-1] if self.positions else None
    
    def get_velocity_magnitude(self) -> float:
        """Get speed (magnitude of velocity vector)"""
        if self._velocity:
            vx, vy = self._velocity
            return np.sqrt(vx**2 + vy**2)
        return 0.0
    
    def get_direction_degrees(self) -> float:
        """Get movement direction in degrees [0-360]"""
        if self._direction is not None:
            return np.degrees(self._direction) % 360
        return 0.0


class BehavioralContextEngine:
    """
    Behavioral Context Engine - Tracks and analyzes object behavior over time.
    
    Thread-safe, CPU-optimized, enterprise-grade implementation.
    """
    
    def __init__(
        self,
        loitering_threshold: float = 10.0,  # seconds
        velocity_smoothing: int = 5,         # frames for velocity averaging
        acceleration_threshold: float = 50.0,  # pixels/sec²
        erratic_movement_threshold: float = 3.0,  # std dev threshold
        disappearance_timeout: float = 2.0,   # seconds before marked disappeared
        max_history_size: int = 300,          # frames to keep (10 sec at 30fps)
        fps: int = 30
    ):
        """
        Initialize Behavioral Context Engine
        
        Args:
            loitering_threshold: Seconds of low movement to trigger loitering
            velocity_smoothing: Number of frames to smooth velocity calculation
            acceleration_threshold: Threshold for sudden acceleration detection
            erratic_movement_threshold: Std dev threshold for erratic motion
            disappearance_timeout: Seconds before object marked as disappeared
            max_history_size: Maximum trajectory points to store
            fps: Video frame rate for time calculations
        """
        self.loitering_threshold = loitering_threshold
        self.velocity_smoothing = velocity_smoothing
        self.acceleration_threshold = acceleration_threshold
        self.erratic_movement_threshold = erratic_movement_threshold
        self.disappearance_timeout = disappearance_timeout
        self.max_history_size = max_history_size
        self.fps = fps
        
        # Thread-safe object tracking
        self.objects: Dict[int, ObjectState] = {}
        self.lock = threading.RLock()
        
        # Performance metrics
        self.frame_count = 0
        self.total_objects_tracked = 0
        self.active_objects = 0
        
        logger.info("✅ Behavioral Context Engine initialized")
    
    def update(
        self,
        frame_detections: List[Dict],
        timestamp: datetime,
        frame_shape: Tuple[int, int]
    ) -> Dict[int, ObjectState]:
        """
        Update object states with new frame detections.
        
        Args:
            frame_detections: List of detections from tracker
                [{
                    'track_id': int,
                    'bbox': [x1, y1, x2, y2],
                    'confidence': float,
                    'class_name': str
                }]
            timestamp: Current frame timestamp
            frame_shape: (height, width) for normalization
            
        Returns:
            Updated object states dictionary
        """
        with self.lock:
            self.frame_count += 1
            frame_height, frame_width = frame_shape
            
            # Track which IDs are present in current frame
            current_ids = set()
            
            # Update existing objects and create new ones
            for det in frame_detections:
                track_id = det['track_id']
                current_ids.add(track_id)
                
                # Extract detection data
                bbox = det['bbox']  # [x1, y1, x2, y2]
                centroid = self._compute_centroid(bbox)
                confidence = det.get('confidence', 1.0)
                class_name = det.get('class_name', 'unknown')
                
                # Update or create object state
                if track_id in self.objects:
                    obj = self.objects[track_id]
                    obj.last_seen = timestamp
                    obj.disappeared = False
                else:
                    # New object
                    obj = ObjectState(
                        track_id=track_id,
                        class_name=class_name,
                        first_seen=timestamp,
                        last_seen=timestamp
                    )
                    self.objects[track_id] = obj
                    self.total_objects_tracked += 1
                
                # Update spatial history
                obj.positions.append(centroid)
                obj.bboxes.append(bbox)
                obj.confidences.append(confidence)
                
                # Compute motion metrics (lazy evaluation)
                self._compute_motion_metrics(obj, timestamp)
                
                # Detect behavioral patterns
                self._analyze_behavior(obj, timestamp)
            
            # Mark disappeared objects
            disappeared_ids = set(self.objects.keys()) - current_ids
            for track_id in disappeared_ids:
                obj = self.objects[track_id]
                time_since_seen = (timestamp - obj.last_seen).total_seconds()
                if time_since_seen > self.disappearance_timeout:
                    obj.disappeared = True
            
            # Update active count
            self.active_objects = len([o for o in self.objects.values() if not o.disappeared])
            
            return self.objects
    
    def _compute_centroid(self, bbox: List[float]) -> Tuple[float, float]:
        """Compute centroid from bounding box"""
        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        return (cx, cy)
    
    def _compute_motion_metrics(self, obj: ObjectState, timestamp: datetime):
        """
        Compute velocity, acceleration, direction using vectorized operations.
        CPU-optimized with NumPy.
        """
        if len(obj.positions) < 2:
            return
        
        # Convert to numpy array for vectorized operations
        positions = np.array(list(obj.positions))
        
        # Compute velocity (averaged over smoothing window)
        if len(positions) >= self.velocity_smoothing:
            recent = positions[-self.velocity_smoothing:]
            displacements = np.diff(recent, axis=0)
            avg_displacement = np.mean(displacements, axis=0)
            dt = 1.0 / self.fps  # Time between frames
            obj._velocity = tuple(avg_displacement / dt)
            
            # Direction (angle in radians)
            vx, vy = obj._velocity
            obj._direction = np.arctan2(vy, vx)
        
        # Compute acceleration (change in velocity magnitude)
        if len(positions) >= self.velocity_smoothing * 2:
            # Previous velocity
            prev_window = positions[-self.velocity_smoothing*2 : -self.velocity_smoothing]
            prev_disp = np.mean(np.diff(prev_window, axis=0), axis=0)
            prev_vel = np.linalg.norm(prev_disp) / (1.0 / self.fps)
            
            # Current velocity magnitude
            curr_vel = obj.get_velocity_magnitude()
            
            # Acceleration
            dt = self.velocity_smoothing / self.fps
            obj._acceleration = (curr_vel - prev_vel) / dt
        
        # Total distance traveled
        if len(positions) >= 2:
            distances = np.linalg.norm(np.diff(positions, axis=0), axis=1)
            obj._distance_traveled = np.sum(distances)
        
        # Dwell time
        obj.dwell_time = (timestamp - obj.first_seen).total_seconds()
    
    def _analyze_behavior(self, obj: ObjectState, timestamp: datetime):
        """
        Analyze behavioral patterns and set flags.
        
        Detects:
        - Loitering (low velocity + high dwell time)
        - Sudden acceleration/deceleration
        - Erratic movement
        - Stopped vs moving
        """
        velocity = obj.get_velocity_magnitude()
        dwell = obj.dwell_time
        
        # Loitering detection
        # Low velocity for extended period
        if velocity < 10.0 and dwell > self.loitering_threshold:  # <10 px/sec, >10 sec
            obj.is_loitering = True
            obj.motion_pattern = "LOITERING"
        else:
            obj.is_loitering = False
        
        # Acceleration detection
        if obj._acceleration and abs(obj._acceleration) > self.acceleration_threshold:
            obj.is_accelerating = True
        else:
            obj.is_accelerating = False
        
        # Motion pattern classification
        if velocity < 5.0:
            obj.motion_pattern = "STOPPED"
        elif velocity > 100.0:  # Fast movement (100 px/sec)
            if obj.is_accelerating:
                obj.motion_pattern = "FAST_ACCELERATION"
            else:
                obj.motion_pattern = "FAST"
        elif len(obj.positions) >= 10:
            # Check for erratic movement (high variance in direction)
            positions = np.array(list(obj.positions)[-10:])
            velocities = np.diff(positions, axis=0)
            if len(velocities) > 2:
                vel_std = np.std(velocities, axis=0)
                if np.mean(vel_std) > self.erratic_movement_threshold:
                    obj.motion_pattern = "ERRATIC"
                else:
                    obj.motion_pattern = "NORMAL"
        else:
            obj.motion_pattern = "NORMAL"
    
    def get_object_summary(self, track_id: int) -> Optional[Dict]:
        """
        Get comprehensive summary of object behavior.
        
        Returns:
            Dictionary with all behavioral metrics and flags
        """
        with self.lock:
            if track_id not in self.objects:
                return None
            
            obj = self.objects[track_id]
            
            return {
                "track_id": track_id,
                "class_name": obj.class_name,
                "dwell_time": obj.dwell_time,
                "velocity": obj.get_velocity_magnitude(),
                "direction_degrees": obj.get_direction_degrees(),
                "acceleration": obj._acceleration,
                "distance_traveled": obj._distance_traveled,
                "is_loitering": obj.is_loitering,
                "is_accelerating": obj.is_accelerating,
                "motion_pattern": obj.motion_pattern,
                "disappeared": obj.disappeared,
                "current_zone": obj.current_zone,
                "zones_visited": len(obj.zones_entered),
                "trajectory_length": len(obj.positions),
                "avg_confidence": np.mean(list(obj.confidences)) if obj.confidences else 0.0
            }
    
    def get_loitering_objects(self) -> List[int]:
        """Get all track IDs exhibiting loitering behavior"""
        with self.lock:
            return [tid for tid, obj in self.objects.items() 
                    if obj.is_loitering and not obj.disappeared]
    
    def get_fast_moving_objects(self, threshold: float = 80.0) -> List[int]:
        """Get all track IDs moving faster than threshold"""
        with self.lock:
            return [tid for tid, obj in self.objects.items()
                    if obj.get_velocity_magnitude() > threshold and not obj.disappeared]
    
    def cleanup_old_objects(self, max_age_seconds: float = 60.0):
        """
        Remove objects that haven't been seen for a long time.
        Prevents memory bloat in long-running systems.
        """
        with self.lock:
            now = datetime.now()
            to_remove = []
            
            for track_id, obj in self.objects.items():
                age = (now - obj.last_seen).total_seconds()
                if age > max_age_seconds:
                    to_remove.append(track_id)
            
            for track_id in to_remove:
                del self.objects[track_id]
            
            if to_remove:
                logger.info(f"🧹 Cleaned up {len(to_remove)} old objects")
    
    def get_stats(self) -> Dict:
        """Get engine performance statistics"""
        with self.lock:
            return {
                "total_objects_tracked": self.total_objects_tracked,
                "active_objects": self.active_objects,
                "disappeared_objects": len([o for o in self.objects.values() if o.disappeared]),
                "loitering_count": len(self.get_loitering_objects()),
                "frames_processed": self.frame_count,
                "objects_in_memory": len(self.objects)
            }
