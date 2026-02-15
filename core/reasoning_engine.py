"""
Real-Time Reasoning Engine
Analyzes tracked objects and generates structured reasoning events
"""
import time
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import defaultdict
import math

logger = logging.getLogger(__name__)


@dataclass
class ReasoningEvent:
    """Structured reasoning event"""
    severity: str  # CRITICAL, WARNING, NORMAL
    message: str
    color: str  # red, yellow, cyan
    timestamp: float
    track_id: int = None
    class_name: str = None
    metadata: Dict[str, Any] = None


class ObjectMemory:
    """Temporal memory for tracked objects"""
    def __init__(self):
        self.first_seen = None
        self.last_seen = None
        self.positions = []  # List of (x, y, timestamp)
        self.class_name = None
        self.confidence_history = []
        self.zone_entries = []  # Zones entered
        
    @property
    def duration(self) -> float:
        """How long object has been tracked (seconds)"""
        if self.first_seen is None or self.last_seen is None:
            return 0
        return self.last_seen - self.first_seen
    
    @property
    def velocity(self) -> float:
        """Estimate velocity in pixels/second"""
        if len(self.positions) < 2:
            return 0
        
        # Use last 5 positions for smoothing
        recent = self.positions[-5:]
        if len(recent) < 2:
            return 0
        
        # Calculate distance traveled
        x1, y1, t1 = recent[0]
        x2, y2, t2 = recent[-1]
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        time_delta = t2 - t1
        
        if time_delta == 0:
            return 0
        
        return distance / time_delta
    
    def update(self, bbox, class_name, confidence, timestamp):
        """Update memory with new observation"""
        if self.first_seen is None:
            self.first_seen = timestamp
        
        self.last_seen = timestamp
        self.class_name = class_name
        self.confidence_history.append(confidence)
        
        # Store center position
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        self.positions.append((center_x, center_y, timestamp))
        
        # Keep only last 30 positions (memory limit)
        if len(self.positions) > 30:
            self.positions = self.positions[-30:]
        if len(self.confidence_history) > 30:
            self.confidence_history = self.confidence_history[-30:]


class RealtimeReasoningEngine:
    """
    Real-time reasoning engine that analyzes tracked objects
    and generates structured events
    """
    def __init__(self):
        self.object_memory: Dict[int, ObjectMemory] = {}
        self.frame_count = 0
        self.last_cleanup = time.time()
        
        # Reasoning thresholds
        self.LOITERING_THRESHOLD = 15.0  # seconds
        self.HIGH_SPEED_THRESHOLD = 150.0  # pixels/second
        self.CONFIDENCE_DROP_THRESHOLD = 0.3  # 30% drop
        
        logger.info("🧠 Realtime Reasoning Engine initialized")
    
    def analyze_frame(self, tracked_objects: List[Dict[str, Any]], frame_time: float = None) -> List[ReasoningEvent]:
        """
        Analyze a single frame of tracked objects
        
        Args:
            tracked_objects: List of tracked detections with:
                - track_id: Unique ID
                - bbox: (x1, y1, x2, y2)
                - class_name: Object class
                - confidence: Detection confidence
                - class_id: Class ID
            frame_time: Current timestamp (defaults to time.time())
        
        Returns:
            List of ReasoningEvent objects
        """
        if frame_time is None:
            frame_time = time.time()
        
        self.frame_count += 1
        events = []
        
        # Update memory for each tracked object
        current_track_ids = set()
        
        for obj in tracked_objects:
            track_id = obj.get('track_id')
            if track_id is None:
                continue
            
            current_track_ids.add(track_id)
            
            # Initialize memory if new object
            if track_id not in self.object_memory:
                self.object_memory[track_id] = ObjectMemory()
                events.append(ReasoningEvent(
                    severity="NORMAL",
                    message=f"New {obj['class_name']} detected (ID {track_id})",
                    color="cyan",
                    timestamp=frame_time,
                    track_id=track_id,
                    class_name=obj['class_name']
                ))
            
            # Update memory
            memory = self.object_memory[track_id]
            memory.update(
                bbox=obj['bbox'],
                class_name=obj['class_name'],
                confidence=obj['confidence'],
                timestamp=frame_time
            )
            
            # Run reasoning rules
            events.extend(self._apply_reasoning_rules(track_id, memory, frame_time))
        
        # Cleanup stale objects (not seen in 5 seconds)
        if frame_time - self.last_cleanup > 2.0:
            self._cleanup_stale_objects(current_track_ids, frame_time)
            self.last_cleanup = frame_time
        
        # Log reasoning activity
        if self.frame_count % 30 == 0:
            logger.info(f"🧠 Reasoning: {len(events)} events | Tracking {len(self.object_memory)} objects")
        
        return events
    
    def _apply_reasoning_rules(self, track_id: int, memory: ObjectMemory, timestamp: float) -> List[ReasoningEvent]:
        """Apply reasoning rules to an object"""
        events = []
        
        # Rule 1: Loitering detection
        if memory.duration > self.LOITERING_THRESHOLD:
            # Only emit every 10 seconds to avoid spam
            if int(memory.duration) % 10 == 0 and len(memory.positions) > 0:
                events.append(ReasoningEvent(
                    severity="WARNING",
                    message=f"{memory.class_name.capitalize()} ID {track_id} loitering for {int(memory.duration)}s",
                    color="yellow",
                    timestamp=timestamp,
                    track_id=track_id,
                    class_name=memory.class_name,
                    metadata={"duration": memory.duration}
                ))
        
        # Rule 2: High-speed movement (running, fast vehicle)
        velocity = memory.velocity
        if velocity > self.HIGH_SPEED_THRESHOLD:
            events.append(ReasoningEvent(
                severity="CRITICAL",
                message=f"{memory.class_name.capitalize()} ID {track_id} abnormal movement detected (speed: {int(velocity)}px/s)",
                color="red",
                timestamp=timestamp,
                track_id=track_id,
                class_name=memory.class_name,
                metadata={"velocity": velocity}
            ))
        
        # Rule 3: Confidence drop (possible occlusion or disguise)
        if len(memory.confidence_history) >= 5:
            recent_conf = memory.confidence_history[-1]
            avg_conf = sum(memory.confidence_history[-10:]) / min(10, len(memory.confidence_history))
            
            if avg_conf - recent_conf > self.CONFIDENCE_DROP_THRESHOLD:
                events.append(ReasoningEvent(
                    severity="WARNING",
                    message=f"{memory.class_name.capitalize()} ID {track_id} confidence dropped (occlusion or disguise?)",
                    color="yellow",
                    timestamp=timestamp,
                    track_id=track_id,
                    class_name=memory.class_name,
                    metadata={"confidence_drop": avg_conf - recent_conf}
                ))
        
        # Rule 4: Person-specific behaviors
        if memory.class_name == "person":
            # Stationary person for extended time
            if memory.duration > 30 and velocity < 10:
                if int(memory.duration) % 15 == 0:  # Every 15 seconds
                    events.append(ReasoningEvent(
                        severity="WARNING",
                        message=f"Person ID {track_id} stationary for {int(memory.duration)}s (potential security concern)",
                        color="yellow",
                        timestamp=timestamp,
                        track_id=track_id,
                        class_name=memory.class_name,
                        metadata={"duration": memory.duration, "velocity": velocity}
                    ))
        
        # Rule 5: Multiple people detected (crowding)
        person_count = sum(1 for mem in self.object_memory.values() if mem.class_name == "person")
        if person_count >= 3 and self.frame_count % 60 == 0:  # Every 60 frames
            events.append(ReasoningEvent(
                severity="NORMAL",
                message=f"Multiple people detected: {person_count} individuals in view",
                color="cyan",
                timestamp=timestamp,
                class_name="person",
                metadata={"count": person_count}
            ))
        
        return events
    
    def _cleanup_stale_objects(self, current_track_ids: set, timestamp: float):
        """Remove objects not seen recently"""
        stale_ids = []
        
        for track_id, memory in self.object_memory.items():
            if track_id not in current_track_ids:
                # Object hasn't been seen for 5 seconds
                if timestamp - memory.last_seen > 5.0:
                    stale_ids.append(track_id)
        
        for track_id in stale_ids:
            memory = self.object_memory.pop(track_id)
            logger.debug(f"Removed stale object ID {track_id} ({memory.class_name})")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get reasoning engine statistics"""
        return {
            "tracked_objects": len(self.object_memory),
            "frame_count": self.frame_count,
            "object_durations": {
                track_id: mem.duration 
                for track_id, mem in self.object_memory.items()
            }
        }
    
    def reset(self):
        """Reset reasoning engine state"""
        self.object_memory.clear()
        self.frame_count = 0
        logger.info("🧠 Reasoning engine reset")


# Global reasoning engine instance
_reasoning_engine = None

def get_reasoning_engine() -> RealtimeReasoningEngine:
    """Get or create global reasoning engine instance"""
    global _reasoning_engine
    if _reasoning_engine is None:
        _reasoning_engine = RealtimeReasoningEngine()
    return _reasoning_engine
