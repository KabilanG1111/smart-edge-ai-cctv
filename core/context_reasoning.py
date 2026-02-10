"""
Context-Aware Reasoning Engine
Temporal logic for track-based surveillance intelligence

Eliminates per-frame decisions in favor of multi-second context windows
"""

import time
import numpy as np
from typing import Dict, List, Tuple, Set, Optional, Counter
from dataclasses import dataclass, field
from collections import deque, Counter as CounterType
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Three-state surveillance alert system"""
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    SUSPICIOUS = "SUSPICIOUS"


@dataclass
class ContextFeatures:
    """Behavioral features extracted from track history"""
    # Temporal
    duration: float
    time_of_day: str
    
    # Spatial
    zone_transitions: int
    restricted_zone_entry: bool
    zone_loitering: bool
    
    # Movement
    avg_speed: float
    direction_stability: float
    is_stationary: bool
    
    # Interactions
    multi_person_group: bool
    isolated: bool
    
    # Classification
    class_confidence: float
    class_flicker: bool


@dataclass
class TrackState:
    """
    Persistent state for each ByteTrack ID
    Accumulates context over time (not per-frame)
    """
    track_id: int
    class_name: str
    first_seen: float
    last_seen: float
    
    # Spatial history
    positions: deque = field(default_factory=lambda: deque(maxlen=60))  # 2 seconds @ 30 FPS
    zones_entered: Set[str] = field(default_factory=set)
    current_zone: Optional[str] = None
    
    # Classification stability
    class_history: CounterType = field(default_factory=CounterType)
    confidence_history: deque = field(default_factory=lambda: deque(maxlen=30))
    
    # Behavioral metrics
    stationary_frames: int = 0
    direction_changes: int = 0
    last_direction: Optional[float] = None
    interaction_count: int = 0
    
    # Reasoning state
    intent_score: float = 0.0
    alert_level: AlertLevel = AlertLevel.NORMAL
    reasoning: List[str] = field(default_factory=list)
    last_alert_time: float = 0.0
    
    @property
    def duration(self) -> float:
        """Time on screen (seconds)"""
        return self.last_seen - self.first_seen
    
    @property
    def avg_velocity(self) -> float:
        """Average movement speed (pixels per second)"""
        if len(self.positions) < 2:
            return 0.0
        
        total_distance = 0.0
        for i in range(1, len(self.positions)):
            x1, y1 = self.positions[i-1]
            x2, y2 = self.positions[i]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_distance += distance
        
        time_span = len(self.positions) / 30.0  # Assume 30 FPS
        return total_distance / max(time_span, 0.1)


class ContextEngine:
    """
    Multi-track context management
    Maintains temporal state for all active tracks
    """
    
    def __init__(
        self,
        zone_definitions: Optional[Dict[str, List]] = None,
        stationary_threshold: float = 5.0,  # pixels/second
        loitering_time: float = 120.0  # seconds
    ):
        """
        Initialize context engine
        
        Args:
            zone_definitions: Dict of zone_name → [x1, y1, x2, y2]
            stationary_threshold: Speed below which object is stationary
            loitering_time: Time in zone before flagged as loitering
        """
        self.tracks: Dict[int, TrackState] = {}
        self.zone_definitions = zone_definitions or self._default_zones()
        self.stationary_threshold = stationary_threshold
        self.loitering_time = loitering_time
        
        logger.info(f"🧠 ContextEngine initialized with {len(self.zone_definitions)} zones")
    
    def _default_zones(self) -> Dict[str, List]:
        """Default zone definitions (full frame)"""
        return {
            "entrance": [0, 0, 320, 240],  # Top-left quadrant
            "restricted": [480, 0, 640, 240],  # Top-right quadrant
            "main_area": [0, 240, 640, 480],  # Bottom half
        }
    
    def update_track(
        self,
        track_id: int,
        class_name: str,
        confidence: float,
        bbox: Tuple[int, int, int, int],
        timestamp: float
    ) -> TrackState:
        """
        Update track state with new detection
        
        Args:
            track_id: ByteTrack persistent ID
            class_name: Detected class
            confidence: Detection confidence
            bbox: Bounding box (x1, y1, x2, y2)
            timestamp: Unix timestamp
            
        Returns:
            Updated TrackState
        """
        # Create new track if first time seen
        if track_id not in self.tracks:
            track = TrackState(
                track_id=track_id,
                class_name=class_name,
                first_seen=timestamp,
                last_seen=timestamp
            )
            self.tracks[track_id] = track
            logger.info(f"🆕 New track: ID={track_id} class={class_name}")
        else:
            track = self.tracks[track_id]
        
        # Update temporal info
        track.last_seen = timestamp
        track.confidence_history.append(confidence)
        track.class_history[class_name] += 1
        
        # Update primary class (most frequent)
        track.class_name = track.class_history.most_common(1)[0][0]
        
        # Update position history
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        track.positions.append((center_x, center_y))
        
        # Update zone
        track.current_zone = self._get_zone(center_x, center_y)
        if track.current_zone:
            track.zones_entered.add(track.current_zone)
        
        # Calculate movement metrics
        self._update_movement(track)
        
        return track
    
    def _get_zone(self, x: int, y: int) -> Optional[str]:
        """Get zone name for given position"""
        for zone_name, (x1, y1, x2, y2) in self.zone_definitions.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                return zone_name
        return None
    
    def _update_movement(self, track: TrackState):
        """Update movement metrics (velocity, direction changes)"""
        if len(track.positions) < 2:
            return
        
        # Check if stationary
        velocity = track.avg_velocity
        if velocity < self.stationary_threshold:
            track.stationary_frames += 1
        else:
            track.stationary_frames = 0
        
        # Track direction changes
        if len(track.positions) >= 3:
            x1, y1 = track.positions[-3]
            x2, y2 = track.positions[-2]
            x3, y3 = track.positions[-1]
            
            # Calculate direction vectors
            dx1, dy1 = x2 - x1, y2 - y1
            dx2, dy2 = x3 - x2, y3 - y2
            
            # Calculate angle change
            angle1 = np.arctan2(dy1, dx1)
            angle2 = np.arctan2(dy2, dx2)
            angle_change = abs(angle2 - angle1)
            
            # Detect direction change (>90 degrees)
            if angle_change > np.pi / 2:
                track.direction_changes += 1
    
    def extract_features(self, track_id: int) -> Optional[ContextFeatures]:
        """
        Extract behavioral features for reasoning
        
        Args:
            track_id: Track to extract features from
            
        Returns:
            ContextFeatures or None if track not found
        """
        if track_id not in self.tracks:
            return None
        
        track = self.tracks[track_id]
        
        # Time of day bucket
        hour = time.localtime().tm_hour
        if 0 <= hour < 6:
            time_of_day = "night"
        elif 6 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 18:
            time_of_day = "afternoon"
        else:
            time_of_day = "evening"
        
        # Classification stability
        if len(track.class_history) > 0:
            total_detections = sum(track.class_history.values())
            class_confidence = track.class_history[track.class_name] / total_detections
        else:
            class_confidence = 0.0
        
        # Movement stability
        if len(track.positions) > 0:
            direction_stability = 1.0 - (track.direction_changes / max(1, len(track.positions)))
        else:
            direction_stability = 1.0
        
        # Zone loitering check
        stationary_time = track.stationary_frames / 30.0  # Assume 30 FPS
        zone_loitering = stationary_time > self.loitering_time
        
        return ContextFeatures(
            duration=track.duration,
            time_of_day=time_of_day,
            zone_transitions=len(track.zones_entered),
            restricted_zone_entry="restricted" in track.zones_entered,
            zone_loitering=zone_loitering,
            avg_speed=track.avg_velocity,
            direction_stability=direction_stability,
            is_stationary=track.avg_velocity < self.stationary_threshold,
            multi_person_group=track.interaction_count > 2,
            isolated=track.interaction_count == 0,
            class_confidence=class_confidence,
            class_flicker=len(track.class_history) > 2
        )
    
    def remove_track(self, track_id: int):
        """Remove track when lost"""
        if track_id in self.tracks:
            track = self.tracks[track_id]
            logger.info(f"❌ Track {track_id} removed after {track.duration:.1f}s")
            del self.tracks[track_id]
    
    def get_track(self, track_id: int) -> Optional[TrackState]:
        """Get track state by ID"""
        return self.tracks.get(track_id)
    
    def get_all_tracks(self) -> List[TrackState]:
        """Get all active tracks"""
        return list(self.tracks.values())
    
    def reset(self):
        """Clear all tracks"""
        self.tracks.clear()
        logger.info("🔄 ContextEngine reset")


class ReasoningAgent:
    """
    AI decision engine using rule-based temporal logic
    Deterministic, explainable, production-ready
    """
    
    def __init__(
        self,
        alert_cooldown: float = 120.0,  # seconds
        warning_threshold: float = 0.3,
        suspicious_threshold: float = 0.7
    ):
        """
        Initialize reasoning agent
        
        Args:
            alert_cooldown: Minimum time between alerts for same track
            warning_threshold: Intent score threshold for WARNING
            suspicious_threshold: Intent score threshold for SUSPICIOUS
        """
        self.alert_cooldown = alert_cooldown
        self.warning_threshold = warning_threshold
        self.suspicious_threshold = suspicious_threshold
        
        logger.info("🤖 ReasoningAgent initialized")
    
    def analyze_track(
        self,
        track: TrackState,
        features: ContextFeatures
    ) -> Tuple[AlertLevel, float, List[str]]:
        """
        Analyze track and determine alert level
        
        Args:
            track: Track state
            features: Context features
            
        Returns:
            Tuple of (alert_level, intent_score, reasoning_list)
        """
        intent_score = 0.0
        reasons = []
        
        # RULE 1: Restricted Zone Entry (HIGH PRIORITY)
        if features.restricted_zone_entry:
            intent_score += 0.4
            reasons.append("⚠️ Entered restricted area")
        
        # RULE 2: Loitering (MEDIUM PRIORITY)
        if features.zone_loitering:
            intent_score += 0.3
            reasons.append(f"⏱️ Stationary for {track.stationary_frames / 30:.0f}s")
        
        # RULE 3: Unusual Time (LOW-MEDIUM PRIORITY)
        if features.time_of_day == "night" and track.class_name == "person":
            intent_score += 0.2
            reasons.append("🌙 Activity during off-hours")
        
        # RULE 4: Erratic Movement (LOW PRIORITY)
        if features.direction_stability < 0.5 and features.duration > 10:
            intent_score += 0.15
            reasons.append("🔀 Erratic movement pattern")
        
        # RULE 5: Object Carrying in Sensitive Area (HIGH PRIORITY)
        if track.class_name in ["handbag", "backpack", "suitcase"]:
            if features.restricted_zone_entry or features.zone_loitering:
                intent_score += 0.25
                reasons.append(f"💼 Carrying {track.class_name} in sensitive area")
        
        # RULE 6: Rapid Zone Scanning (MEDIUM PRIORITY)
        if features.zone_transitions > 5 and features.duration < 30:
            intent_score += 0.2
            reasons.append("🔍 Rapid zone scanning behavior")
        
        # RULE 7: Group Activity in Restricted Area (HIGH PRIORITY)
        if features.multi_person_group and features.restricted_zone_entry:
            intent_score += 0.3
            reasons.append("👥 Group activity in restricted zone")
        
        # RULE 8: Prolonged Stationary Behavior
        if features.is_stationary and features.duration > 180:  # 3 minutes
            intent_score += 0.2
            reasons.append("🚫 Prolonged stationary presence")
        
        # Classification confidence penalty
        if features.class_confidence < 0.7:
            intent_score *= 0.8  # Reduce by 20%
            if features.class_flicker:
                reasons.append("⚠️ Unstable classification")
        
        # Clamp to [0, 1]
        intent_score = min(1.0, max(0.0, intent_score))
        
        # Determine alert level
        if intent_score < self.warning_threshold:
            alert_level = AlertLevel.NORMAL
        elif intent_score < self.suspicious_threshold:
            alert_level = AlertLevel.WARNING
        else:
            alert_level = AlertLevel.SUSPICIOUS
        
        return alert_level, intent_score, reasons
    
    def should_alert(self, track: TrackState, new_alert_level: AlertLevel) -> bool:
        """
        Check if alert should be raised (considering cooldown)
        
        Args:
            track: Track state
            new_alert_level: Proposed alert level
            
        Returns:
            True if should alert, False otherwise
        """
        now = time.time()
        
        # First time alert
        if track.last_alert_time == 0:
            return new_alert_level != AlertLevel.NORMAL
        
        # Cooldown not expired
        time_since_alert = now - track.last_alert_time
        if time_since_alert < self.alert_cooldown:
            return False
        
        # Severity escalation
        severity_order = {AlertLevel.NORMAL: 0, AlertLevel.WARNING: 1, AlertLevel.SUSPICIOUS: 2}
        if severity_order[new_alert_level] > severity_order[track.alert_level]:
            return True
        
        # Cooldown expired, re-alert if still warning/suspicious
        return new_alert_level != AlertLevel.NORMAL
