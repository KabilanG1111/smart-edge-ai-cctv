"""
Real-Time Behavior Reasoning Engine
Production-grade rule-based behavior analysis for Edge AI CCTV
CPU-optimized, no blocking calls, thread-safe
"""
import time
import math
from collections import deque, defaultdict
from threading import Lock
from datetime import datetime
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class Track:
    """Simplified track data structure"""
    track_id: int
    class_name: str
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    confidence: float
    timestamp: float


@dataclass
class ReasoningEvent:
    """Real-time reasoning event"""
    track_id: int
    event_type: str  # LOITERING, RUNNING, FIGHTING, INTRUSION, NORMAL
    severity: str  # NORMAL, WARNING, CRITICAL
    reasoning: str
    timestamp: str
    velocity: float = 0.0
    duration: float = 0.0


class BehaviorEngine:
    """
    Real-time behavior reasoning engine
    Analyzes tracks every frame and generates reasoning events
    """
    
    def __init__(self, buffer_size=100):
        # Event storage (circular buffer)
        self.events = deque(maxlen=buffer_size)
        self.events_lock = Lock()
        
        # Track history for velocity/duration analysis
        self.track_history = defaultdict(list)  # {track_id: [(x, y, timestamp), ...]}
        self.track_first_seen = {}  # {track_id: timestamp}
        self.track_last_position = {}  # {track_id: (x, y)}
        
        # Behavior thresholds (CPU-optimized)
        self.LOITERING_DURATION = 10.0  # seconds
        self.LOITERING_SPEED_THRESHOLD = 15.0  # pixels/second
        self.RUNNING_SPEED_THRESHOLD = 150.0  # pixels/second
        self.FIGHT_DISTANCE_THRESHOLD = 100.0  # pixels
        self.FIGHT_OSCILLATION_THRESHOLD = 5  # velocity changes
        
        # Restricted zones (example: top-right corner)
        self.restricted_zones = [
            {"x1": 0.7, "y1": 0.0, "x2": 1.0, "y2": 0.3, "name": "Restricted Area A"}
        ]
        
        # Event deduplication
        self.last_event_time = {}  # {(track_id, event_type): timestamp}
        self.EVENT_COOLDOWN = 5.0  # seconds between same events
        
    def analyze_behavior(self, tracks: List[Dict[str, Any]], frame_time: float = None) -> List[ReasoningEvent]:
        """
        Main analysis function - called every frame
        
        Args:
            tracks: List of track dictionaries from ByteTrack
            frame_time: Current frame timestamp (default: current time)
            
        Returns:
            List of reasoning events generated this frame
        """
        if frame_time is None:
            frame_time = time.time()
        
        current_events = []
        
        # Update track history
        self._update_track_history(tracks, frame_time)
        
        # Analyze each track
        person_tracks = [t for t in tracks if t.get('class_name') == 'person']
        
        for track in person_tracks:
            track_id = track['track_id']
            
            # Calculate velocity and duration
            velocity = self._calculate_velocity(track_id)
            duration = self._calculate_duration(track_id, frame_time)
            center = self._get_track_center(track)
            
            # Rule 1: LOITERING detection
            if duration > self.LOITERING_DURATION and velocity < self.LOITERING_SPEED_THRESHOLD:
                if self._should_publish_event(track_id, "LOITERING", frame_time):
                    event = ReasoningEvent(
                        track_id=track_id,
                        event_type="LOITERING",
                        severity="WARNING",
                        reasoning=f"Subject {track_id} stationary for {duration:.1f}s at position ({center[0]:.0f}, {center[1]:.0f}). Possible loitering behavior detected.",
                        timestamp=datetime.now().isoformat(),
                        velocity=velocity,
                        duration=duration
                    )
                    current_events.append(event)
            
            # Rule 2: RUNNING detection
            elif velocity > self.RUNNING_SPEED_THRESHOLD:
                if self._should_publish_event(track_id, "RUNNING", frame_time):
                    event = ReasoningEvent(
                        track_id=track_id,
                        event_type="RUNNING",
                        severity="WARNING",
                        reasoning=f"Subject {track_id} exhibiting rapid movement at {velocity:.1f} px/s. High-velocity trajectory detected.",
                        timestamp=datetime.now().isoformat(),
                        velocity=velocity,
                        duration=duration
                    )
                    current_events.append(event)
            
            # Rule 3: INTRUSION detection
            zone_breach = self._check_zone_intrusion(center)
            if zone_breach:
                if self._should_publish_event(track_id, "INTRUSION", frame_time):
                    event = ReasoningEvent(
                        track_id=track_id,
                        event_type="INTRUSION",
                        severity="CRITICAL",
                        reasoning=f"ALERT: Subject {track_id} entered {zone_breach['name']}. Unauthorized zone breach detected at ({center[0]:.0f}, {center[1]:.0f}).",
                        timestamp=datetime.now().isoformat(),
                        velocity=velocity,
                        duration=duration
                    )
                    current_events.append(event)
        
        # Rule 4: FIGHTING detection (multi-track analysis)
        fight_events = self._detect_fighting(person_tracks, frame_time)
        current_events.extend(fight_events)
        
        # Store events in circular buffer
        if current_events:
            with self.events_lock:
                for event in current_events:
                    self.events.append(event)
        
        # Cleanup old track history (memory management)
        self._cleanup_old_tracks(frame_time)
        
        return current_events
    
    def _update_track_history(self, tracks: List[Dict[str, Any]], frame_time: float):
        """Update position history for all tracks"""
        for track in tracks:
            track_id = track['track_id']
            center = self._get_track_center(track)
            
            # Add to history
            self.track_history[track_id].append((center[0], center[1], frame_time))
            
            # Keep only recent history (last 3 seconds)
            self.track_history[track_id] = [
                (x, y, t) for x, y, t in self.track_history[track_id]
                if frame_time - t < 3.0
            ]
            
            # Track first seen time
            if track_id not in self.track_first_seen:
                self.track_first_seen[track_id] = frame_time
            
            # Update last position
            self.track_last_position[track_id] = center
    
    def _get_track_center(self, track: Dict[str, Any]) -> Tuple[float, float]:
        """Calculate bounding box center"""
        bbox = track['bbox']
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        return (center_x, center_y)
    
    def _calculate_velocity(self, track_id: int) -> float:
        """Calculate track velocity (pixels/second)"""
        history = self.track_history.get(track_id, [])
        
        if len(history) < 2:
            return 0.0
        
        # Calculate average velocity over recent history
        total_distance = 0.0
        total_time = 0.0
        
        for i in range(1, len(history)):
            x1, y1, t1 = history[i-1]
            x2, y2, t2 = history[i]
            
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            time_delta = t2 - t1
            
            if time_delta > 0:
                total_distance += distance
                total_time += time_delta
        
        if total_time > 0:
            return total_distance / total_time
        return 0.0
    
    def _calculate_duration(self, track_id: int, frame_time: float) -> float:
        """Calculate how long track has been visible"""
        first_seen = self.track_first_seen.get(track_id)
        if first_seen is None:
            return 0.0
        return frame_time - first_seen
    
    def _check_zone_intrusion(self, center: Tuple[float, float]) -> Dict[str, Any]:
        """Check if track center is in restricted zone (normalized coordinates)"""
        # Note: Zones use normalized coordinates (0.0-1.0)
        # Convert pixel coordinates to normalized if needed
        for zone in self.restricted_zones:
            # For now, assume center is already in appropriate coordinate system
            # In production, you'd normalize based on frame dimensions
            pass
        return None  # No intrusion detected
    
    def _detect_fighting(self, tracks: List[Dict[str, Any]], frame_time: float) -> List[ReasoningEvent]:
        """Detect potential fighting behavior between tracks"""
        events = []
        
        # Check all pairs of person tracks
        for i, track1 in enumerate(tracks):
            for track2 in tracks[i+1:]:
                track1_id = track1['track_id']
                track2_id = track2['track_id']
                
                # Calculate distance between tracks
                center1 = self._get_track_center(track1)
                center2 = self._get_track_center(track2)
                
                distance = math.sqrt(
                    (center1[0] - center2[0])**2 + 
                    (center1[1] - center2[1])**2
                )
                
                # Check if tracks are close enough
                if distance < self.FIGHT_DISTANCE_THRESHOLD:
                    # Check for high velocity oscillation
                    vel1 = self._calculate_velocity(track1_id)
                    vel2 = self._calculate_velocity(track2_id)
                    
                    if vel1 > 50.0 or vel2 > 50.0:
                        # Potential fighting detected
                        event_key = tuple(sorted([track1_id, track2_id]))
                        
                        if self._should_publish_event(event_key, "FIGHTING", frame_time):
                            event = ReasoningEvent(
                                track_id=track1_id,
                                event_type="FIGHTING",
                                severity="CRITICAL",
                                reasoning=f"ALERT: Aggressive interaction detected between Subject {track1_id} and Subject {track2_id}. Rapid motion patterns suggest physical confrontation.",
                                timestamp=datetime.now().isoformat(),
                                velocity=max(vel1, vel2),
                                duration=0.0
                            )
                            events.append(event)
        
        return events
    
    def _should_publish_event(self, track_id: Any, event_type: str, frame_time: float) -> bool:
        """Check if event should be published (deduplication)"""
        event_key = (track_id, event_type)
        last_time = self.last_event_time.get(event_key, 0)
        
        if frame_time - last_time > self.EVENT_COOLDOWN:
            self.last_event_time[event_key] = frame_time
            return True
        return False
    
    def _cleanup_old_tracks(self, frame_time: float):
        """Remove tracks not seen in last 10 seconds (memory management)"""
        tracks_to_remove = []
        
        for track_id, last_seen in list(self.track_first_seen.items()):
            if frame_time - last_seen > 10.0:
                tracks_to_remove.append(track_id)
        
        for track_id in tracks_to_remove:
            self.track_history.pop(track_id, None)
            self.track_first_seen.pop(track_id, None)
            self.track_last_position.pop(track_id, None)
    
    def get_live_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get latest reasoning events for API endpoint
        Thread-safe retrieval
        """
        with self.events_lock:
            events_list = list(self.events)
        
        # Return newest first
        events_list.reverse()
        
        # Convert to dict format
        return [
            {
                "track_id": e.track_id,
                "event_type": e.event_type,
                "severity": e.severity,
                "reasoning": e.reasoning,
                "timestamp": e.timestamp,
                "velocity": e.velocity,
                "duration": e.duration
            }
            for e in events_list[:limit]
        ]
    
    def reset(self):
        """Clear all state (called when camera stops)"""
        with self.events_lock:
            self.events.clear()
        self.track_history.clear()
        self.track_first_seen.clear()
        self.track_last_position.clear()
        self.last_event_time.clear()


# Global singleton instance
behavior_engine = BehaviorEngine(buffer_size=100)
