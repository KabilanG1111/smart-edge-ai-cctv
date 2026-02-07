"""
Real Event Detection System - NO DUMMY DATA
Produces genuine security events from live CCTV analysis

Event Types:
- MOTION: Object movement detected
- LOITERING: Person/vehicle stationary > threshold
- ROI_BREACH: Object entered restricted zone
- INTRUSION: Unauthorized access during restricted hours
- CROWD: Multiple objects detected simultaneously
- ABANDONED_OBJECT: Object left behind
"""

import time
import uuid
from datetime import datetime, time as dt_time
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Security event classifications"""
    MOTION = "MOTION"
    LOITERING = "LOITERING"
    ROI_BREACH = "ROI_BREACH"
    INTRUSION = "INTRUSION"
    CROWD = "CROWD"
    ABANDONED_OBJECT = "ABANDONED_OBJECT"
    RAPID_MOVEMENT = "RAPID_MOVEMENT"


class Severity(Enum):
    """Event severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class SecurityEvent:
    """
    Real security event (NO dummy data)
    Generated from actual CCTV frame analysis
    """
    event_id: str
    event_type: EventType
    severity: Severity
    confidence: float  # 0.0 to 1.0
    timestamp: str  # ISO format
    camera_id: str
    track_ids: List[int]  # Objects involved
    location: Dict[str, any]  # Bbox or zone info
    metadata: Dict[str, any]  # Additional context
    reasoning: List[str]  # Why this is an event
    frame_number: int
    
    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dict"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "severity": self.severity.value,
            "confidence": round(self.confidence, 3),
            "timestamp": self.timestamp,
            "camera_id": self.camera_id,
            "track_ids": self.track_ids,
            "location": self.location,
            "metadata": self.metadata,
            "reasoning": self.reasoning,
            "frame_number": self.frame_number
        }


class EventDetector:
    """
    Real-time event detection from tracked objects
    NO dummy data - all events are generated from actual analysis
    """
    
    def __init__(
        self,
        camera_id: str = "CAM_001",
        loitering_threshold: float = 5.0,  # seconds
        crowd_threshold: int = 3,  # number of people
        velocity_threshold: float = 100.0,  # pixels/frame for rapid movement
        roi_zones: Optional[List[Dict]] = None,
        restricted_hours: Optional[tuple] = None  # (start_hour, end_hour)
    ):
        """
        Initialize event detector
        
        Args:
            camera_id: Unique camera identifier
            loitering_threshold: Seconds before object is considered loitering
            crowd_threshold: Number of objects to trigger crowd event
            velocity_threshold: Velocity for rapid movement detection
            roi_zones: List of restricted zones [{name, polygon}]
            restricted_hours: Tuple of (start_hour, end_hour) for intrusion detection
        """
        self.camera_id = camera_id
        self.loitering_threshold = loitering_threshold
        self.crowd_threshold = crowd_threshold
        self.velocity_threshold = velocity_threshold
        self.roi_zones = roi_zones or []
        self.restricted_hours = restricted_hours or (22, 6)  # 10 PM to 6 AM
        
        # Event tracking
        self.current_events: Dict[str, SecurityEvent] = {}
        self.event_history: List[SecurityEvent] = []
        self.last_motion_time: float = 0
        self.motion_start_time: Optional[float] = None
        
        # Track states
        self.track_first_seen: Dict[int, float] = {}
        self.track_zones: Dict[int, Set[str]] = {}
        self.notified_tracks: Set[int] = set()  # Prevent duplicate events per track
        
        self.frame_number = 0
        
        logger.info(f"🚨 EventDetector initialized for {camera_id}")
    
    def detect_events(
        self, 
        tracked_objects: List,
        frame_shape: tuple
    ) -> List[SecurityEvent]:
        """
        Analyze tracked objects and generate real security events
        
        Args:
            tracked_objects: List of TrackedObject from object_tracker
            frame_shape: (height, width, channels)
            
        Returns:
            List of SecurityEvent objects
        """
        self.frame_number += 1
        events = []
        current_time = time.time()
        timestamp = datetime.now().isoformat()
        
        # 1. MOTION DETECTION
        if len(tracked_objects) > 0:
            if self.motion_start_time is None:
                self.motion_start_time = current_time
            
            motion_duration = current_time - self.motion_start_time
            
            # Only create motion event if sustained (>0.5s)
            if motion_duration > 0.5 and (current_time - self.last_motion_time > 5.0):
                event = SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.MOTION,
                    severity=Severity.LOW,
                    confidence=0.95,
                    timestamp=timestamp,
                    camera_id=self.camera_id,
                    track_ids=[t.track_id for t in tracked_objects],
                    location={"zone": "monitored_area"},
                    metadata={"object_count": len(tracked_objects)},
                    reasoning=[f"Motion detected with {len(tracked_objects)} object(s)"],
                    frame_number=self.frame_number
                )
                events.append(event)
                self.last_motion_time = current_time
        else:
            self.motion_start_time = None
        
        # 2. LOITERING DETECTION
        for track in tracked_objects:
            if track.is_loitering and track.track_id not in self.notified_tracks:
                confidence = min(0.99, 0.7 + (track.duration / 30.0))  # Increase with time
                
                event = SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.LOITERING,
                    severity=Severity.MEDIUM if track.duration < 15 else Severity.HIGH,
                    confidence=confidence,
                    timestamp=timestamp,
                    camera_id=self.camera_id,
                    track_ids=[track.track_id],
                    location={
                        "bbox": track.bbox,
                        "center": track.center
                    },
                    metadata={
                        "duration": round(track.duration, 2),
                        "class": track.class_name,
                        "stationary_frames": track.stationary_frames
                    },
                    reasoning=[
                        f"{track.class_name} stationary for {track.duration:.1f}s",
                        f"Stationary frames: {track.stationary_frames}"
                    ],
                    frame_number=self.frame_number
                )
                events.append(event)
                self.notified_tracks.add(track.track_id)
        
        # 3. CROWD DETECTION
        if len(tracked_objects) >= self.crowd_threshold:
            person_count = sum(1 for t in tracked_objects if t.class_name == "person")
            
            if person_count >= self.crowd_threshold:
                confidence = min(0.99, 0.6 + (person_count / 10.0))
                
                event = SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.CROWD,
                    severity=Severity.MEDIUM if person_count < 5 else Severity.HIGH,
                    confidence=confidence,
                    timestamp=timestamp,
                    camera_id=self.camera_id,
                    track_ids=[t.track_id for t in tracked_objects if t.class_name == "person"],
                    location={"zone": "monitored_area"},
                    metadata={
                        "person_count": person_count,
                        "total_objects": len(tracked_objects)
                    },
                    reasoning=[
                        f"{person_count} people detected simultaneously",
                        "Crowd density above threshold"
                    ],
                    frame_number=self.frame_number
                )
                events.append(event)
        
        # 4. RAPID MOVEMENT DETECTION
        for track in tracked_objects:
            if track.velocity > self.velocity_threshold:
                event = SecurityEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.RAPID_MOVEMENT,
                    severity=Severity.MEDIUM,
                    confidence=0.85,
                    timestamp=timestamp,
                    camera_id=self.camera_id,
                    track_ids=[track.track_id],
                    location={
                        "bbox": track.bbox,
                        "center": track.center
                    },
                    metadata={
                        "velocity": round(track.velocity, 2),
                        "class": track.class_name
                    },
                    reasoning=[
                        f"Rapid movement detected: {track.velocity:.0f} px/frame",
                        f"Object: {track.class_name}"
                    ],
                    frame_number=self.frame_number
                )
                events.append(event)
        
        # 5. ROI BREACH DETECTION
        if self.roi_zones:
            for track in tracked_objects:
                for zone in self.roi_zones:
                    if self._point_in_polygon(track.center, zone["polygon"]):
                        zone_key = f"{track.track_id}_{zone['name']}"
                        
                        if track.track_id not in self.track_zones:
                            self.track_zones[track.track_id] = set()
                        
                        if zone['name'] not in self.track_zones[track.track_id]:
                            self.track_zones[track.track_id].add(zone['name'])
                            
                            event = SecurityEvent(
                                event_id=str(uuid.uuid4()),
                                event_type=EventType.ROI_BREACH,
                                severity=Severity.HIGH,
                                confidence=0.92,
                                timestamp=timestamp,
                                camera_id=self.camera_id,
                                track_ids=[track.track_id],
                                location={
                                    "zone": zone['name'],
                                    "bbox": track.bbox,
                                    "center": track.center
                                },
                                metadata={
                                    "class": track.class_name,
                                    "confidence": track.confidence
                                },
                                reasoning=[
                                    f"Unauthorized entry into {zone['name']}",
                                    f"Object type: {track.class_name}"
                                ],
                                frame_number=self.frame_number
                            )
                            events.append(event)
        
        # 6. INTRUSION DETECTION (after hours)
        if self._is_restricted_hours():
            if len(tracked_objects) > 0:
                person_tracks = [t for t in tracked_objects if t.class_name == "person"]
                
                if person_tracks:
                    event = SecurityEvent(
                        event_id=str(uuid.uuid4()),
                        event_type=EventType.INTRUSION,
                        severity=Severity.CRITICAL,
                        confidence=0.96,
                        timestamp=timestamp,
                        camera_id=self.camera_id,
                        track_ids=[t.track_id for t in person_tracks],
                        location={"zone": "restricted_hours"},
                        metadata={
                            "hour": datetime.now().hour,
                            "person_count": len(person_tracks)
                        },
                        reasoning=[
                            "Unauthorized activity during restricted hours",
                            f"{len(person_tracks)} person(s) detected",
                            f"Time: {datetime.now().strftime('%H:%M:%S')}"
                        ],
                        frame_number=self.frame_number
                    )
                    events.append(event)
        
        # Store events
        for event in events:
            self.event_history.append(event)
            self.current_events[event.event_id] = event
        
        return events
    
    def _is_restricted_hours(self) -> bool:
        """Check if current time is within restricted hours"""
        current_hour = datetime.now().hour
        start, end = self.restricted_hours
        
        if start < end:
            return start <= current_hour < end
        else:  # Overnight restriction (e.g., 22:00 to 06:00)
            return current_hour >= start or current_hour < end
    
    def _point_in_polygon(self, point: tuple, polygon: List[tuple]) -> bool:
        """Check if point is inside polygon using ray casting"""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def get_recent_events(self, limit: int = 50) -> List[Dict]:
        """Get recent events as dicts"""
        return [e.to_dict() for e in self.event_history[-limit:]]
    
    def get_active_events(self) -> List[Dict]:
        """Get currently active events"""
        return [e.to_dict() for e in self.current_events.values()]
    
    def clear_track(self, track_id: int):
        """Clear track from notification set when track is lost"""
        self.notified_tracks.discard(track_id)
        if track_id in self.track_zones:
            del self.track_zones[track_id]
    
    def reset(self):
        """Reset all event state"""
        logger.info("🔄 Resetting EventDetector")
        self.current_events.clear()
        self.event_history.clear()
        self.notified_tracks.clear()
        self.track_zones.clear()
        self.frame_number = 0


# Global instance
event_detector = EventDetector(
    camera_id="CAM_001",
    loitering_threshold=5.0,
    crowd_threshold=3,
    velocity_threshold=100.0,
    roi_zones=[
        {
            "name": "Restricted Zone A",
            "polygon": [(100, 100), (500, 100), (500, 400), (100, 400)]
        }
    ],
    restricted_hours=(22, 6)  # 10 PM to 6 AM
)
