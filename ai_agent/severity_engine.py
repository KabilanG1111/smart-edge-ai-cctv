"""
⚖️ SEVERITY SCORING ENGINE
==========================

Multi-factor severity assessment for events and violations.

Scoring Factors:
- Duration weight (how long has behavior persisted)
- Zone weight (severity based on zone importance)
- Object class weight (person > vehicle > object)
- Speed anomaly weight (unusual velocity patterns)
- Time-of-day weight (higher at night, lower during business hours)
- Crowd density weight (higher in crowded areas)
- Historical pattern weight (repeat offender)

Severity Categories:
- LOW (0.0-0.3): Normal, no action
- MEDIUM (0.3-0.5): Monitor, log event
- HIGH (0.5-0.7): Alert, review required
- CRITICAL (0.7-1.0): Immediate response, alarm

CPU Optimizations:
- Vectorized scoring calculations
- Cached weight matrices
- Efficient lookup tables
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, time
from enum import Enum
import threading
import logging

logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    """Severity classification levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    
    @classmethod
    def from_score(cls, score: float) -> 'SeverityLevel':
        """Convert numeric score to severity level"""
        if score < 0.3:
            return cls.LOW
        elif score < 0.5:
            return cls.MEDIUM
        elif score < 0.7:
            return cls.HIGH
        else:
            return cls.CRITICAL


class SeverityScoreEngine:
    """
    Severity Scoring Engine - Multi-factor risk assessment.
    
    Computes weighted severity scores for events and violations.
    Thread-safe, CPU-optimized.
    """
    
    def __init__(
        self,
        # Weight configuration
        duration_weight: float = 0.25,
        zone_weight: float = 0.20,
        class_weight: float = 0.15,
        speed_weight: float = 0.15,
        time_weight: float = 0.10,
        crowd_weight: float = 0.10,
        history_weight: float = 0.05,
        
        # Thresholds
        loitering_duration_threshold: float = 10.0,  # seconds
        high_speed_threshold: float = 100.0,  # pixels/sec
        night_start: time = time(22, 0),  # 10 PM
        night_end: time = time(6, 0),     # 6 AM
        crowd_threshold: int = 20
    ):
        """
        Initialize Severity Scoring Engine
        
        Args:
            duration_weight: Weight for duration factor
            zone_weight: Weight for zone importance
            class_weight: Weight for object class
            speed_weight: Weight for speed anomaly
            time_weight: Weight for time-of-day
            crowd_weight: Weight for crowd density
            history_weight: Weight for historical patterns
            loitering_duration_threshold: Seconds to consider loitering
            high_speed_threshold: Pixels/sec for high speed
            night_start: Start of night hours (higher weight)
            night_end: End of night hours
            crowd_threshold: Person count for crowd density factor
        """
        # Validate weights sum to 1.0
        total_weight = (duration_weight + zone_weight + class_weight +
                       speed_weight + time_weight + crowd_weight + history_weight)
        
        if not np.isclose(total_weight, 1.0):
            logger.warning(f"⚠️ Weights sum to {total_weight}, normalizing to 1.0")
            norm_factor = 1.0 / total_weight
            duration_weight *= norm_factor
            zone_weight *= norm_factor
            class_weight *= norm_factor
            speed_weight *= norm_factor
            time_weight *= norm_factor
            crowd_weight *= norm_factor
            history_weight *= norm_factor
        
        self.weights = {
            'duration': duration_weight,
            'zone': zone_weight,
            'class': class_weight,
            'speed': speed_weight,
            'time': time_weight,
            'crowd': crowd_weight,
            'history': history_weight
        }
        
        self.loitering_duration_threshold = loitering_duration_threshold
        self.high_speed_threshold = high_speed_threshold
        self.night_start = night_start
        self.night_end = night_end
        self.crowd_threshold = crowd_threshold
        
        # Class priority lookup (higher = more important)
        self.class_priority = {
            'person': 1.0,
            'car': 0.7,
            'truck': 0.7,
            'bus': 0.6,
            'motorcycle': 0.8,
            'bicycle': 0.6,
            'knife': 1.0,  # Weapon (if detected)
            'gun': 1.0,
            'backpack': 0.5,
            'handbag': 0.4,
            'suitcase': 0.5,
            'default': 0.3  # Unknown classes
        }
        
        # Historical violation tracking
        self.violation_history: Dict[int, List[datetime]] = {}  # track_id -> timestamps
        self.lock = threading.RLock()
        
        logger.info("✅ Severity Scoring Engine initialized")
    
    def compute_severity(
        self,
        object_state,
        zone_info: Optional[Dict] = None,
        crowd_count: int = 0,
        timestamp: Optional[datetime] = None
    ) -> Tuple[float, SeverityLevel, Dict[str, float]]:
        """
        Compute comprehensive severity score.
        
        Args:
            object_state: ObjectState from context engine
            zone_info: Current zone information
            crowd_count: Number of people in nearby area
            timestamp: Current timestamp
            
        Returns:
            Tuple of (score, severity_level, factor_breakdown)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        with self.lock:
            # Compute individual factors
            factors = {}
            
            # 1. Duration factor
            factors['duration'] = self._compute_duration_factor(object_state)
            
            # 2. Zone factor
            factors['zone'] = self._compute_zone_factor(zone_info)
            
            # 3. Class factor
            factors['class'] = self._compute_class_factor(object_state.class_name)
            
            # 4. Speed factor
            factors['speed'] = self._compute_speed_factor(object_state)
            
            # 5. Time-of-day factor
            factors['time'] = self._compute_time_factor(timestamp)
            
            # 6. Crowd density factor
            factors['crowd'] = self._compute_crowd_factor(crowd_count)
            
            # 7. Historical pattern factor
            factors['history'] = self._compute_history_factor(object_state.track_id)
            
            # Compute weighted score
            score = sum(self.weights[key] * value for key, value in factors.items())
            
            # Clamp to [0, 1]
            score = np.clip(score, 0.0, 1.0)
            
            # Get severity level
            severity = SeverityLevel.from_score(score)
            
            return score, severity, factors
    
    def _compute_duration_factor(self, object_state) -> float:
        """
        Compute duration factor based on dwell time.
        
        Longer dwell time (loitering) = higher score
        """
        dwell = object_state.dwell_time
        
        if dwell < self.loitering_duration_threshold:
            # Normal, proportional to threshold
            return (dwell / self.loitering_duration_threshold) * 0.3
        else:
            # Loitering detected
            # Score increases logarithmically with time
            excess = dwell - self.loitering_duration_threshold
            return 0.3 + min(0.7, 0.1 * np.log1p(excess))
    
    def _compute_zone_factor(self, zone_info: Optional[Dict]) -> float:
        """
        Compute zone importance factor.
        
        Restricted zones have higher weight.
        """
        if not zone_info:
            return 0.1  # No zone = low priority
        
        zone_type = zone_info.get('type', 'normal')
        severity_weight = zone_info.get('severity_weight', 1.0)
        
        # Base scores by zone type
        base_scores = {
            'restricted': 0.9,
            'time_restricted': 0.7,
            'entry_only': 0.6,
            'exit_only': 0.6,
            'crowd_limit': 0.5,
            'normal': 0.3
        }
        
        base = base_scores.get(zone_type, 0.3)
        
        return base * severity_weight
    
    def _compute_class_factor(self, class_name: str) -> float:
        """
        Compute object class priority factor.
        
        Person = high priority, objects = lower priority
        """
        return self.class_priority.get(class_name, self.class_priority['default'])
    
    def _compute_speed_factor(self, object_state) -> float:
        """
        Compute speed anomaly factor.
        
        Very high or very low speeds are suspicious.
        """
        velocity = object_state.get_velocity_magnitude()
        
        # Stopped/loitering (very low speed)
        if velocity < 5.0:
            return 0.6
        
        # High speed
        elif velocity > self.high_speed_threshold:
            # Score increases with speed
            excess = velocity - self.high_speed_threshold
            return min(1.0, 0.6 + 0.004 * excess)
        
        # Sudden acceleration
        elif object_state.is_accelerating:
            return 0.7
        
        # Normal speed
        else:
            return 0.2
    
    def _compute_time_factor(self, timestamp: datetime) -> float:
        """
        Compute time-of-day factor.
        
        Night hours = higher suspicion, business hours = lower.
        """
        current_time = timestamp.time()
        
        # Check if in night hours
        if self.night_start <= current_time or current_time <= self.night_end:
            # Night: 10 PM - 6 AM
            return 0.8
        elif time(6, 0) <= current_time <= time(9, 0):
            # Early morning: 6 AM - 9 AM
            return 0.4
        elif time(9, 0) <= current_time <= time(17, 0):
            # Business hours: 9 AM - 5 PM
            return 0.2
        elif time(17, 0) <= current_time <= time(22, 0):
            # Evening: 5 PM - 10 PM
            return 0.5
        else:
            return 0.5
    
    def _compute_crowd_factor(self, crowd_count: int) -> float:
        """
        Compute crowd density factor.
        
        Higher density = harder to monitor = higher score.
        """
        if crowd_count < self.crowd_threshold / 2:
            # Low crowd, easy to monitor
            return 0.2
        elif crowd_count < self.crowd_threshold:
            # Moderate crowd
            return 0.4
        else:
            # High crowd density
            excess = crowd_count - self.crowd_threshold
            return min(0.9, 0.5 + 0.02 * excess)
    
    def _compute_history_factor(self, track_id: int) -> float:
        """
        Compute historical pattern factor.
        
        Repeat violators get higher scores.
        """
        if track_id not in self.violation_history:
            return 0.1  # First time
        
        violations = self.violation_history[track_id]
        
        if not violations:
            return 0.1
        
        # Recent violations (last 24 hours)
        now = datetime.now()
        recent = [v for v in violations if (now - v).total_seconds() < 86400]
        
        if len(recent) == 0:
            return 0.2  # Old violations only
        elif len(recent) == 1:
            return 0.4
        elif len(recent) == 2:
            return 0.6
        else:
            return 0.9  # Repeat offender
    
    def record_violation(self, track_id: int, timestamp: Optional[datetime] = None):
        """Record a violation for historical tracking"""
        if timestamp is None:
            timestamp = datetime.now()
        
        with self.lock:
            if track_id not in self.violation_history:
                self.violation_history[track_id] = []
            
            self.violation_history[track_id].append(timestamp)
            
            # Keep only recent history (last 7 days)
            cutoff = timestamp - timedelta(days=7)
            self.violation_history[track_id] = [
                v for v in self.violation_history[track_id] if v > cutoff
            ]
    
    def get_high_severity_objects(
        self,
        object_states: Dict,
        threshold: float = 0.7
    ) -> List[Tuple[int, float]]:
        """
        Get objects with severity above threshold.
        
        Returns:
            List of (track_id, severity_score) tuples
        """
        high_severity = []
        
        for track_id, obj_state in object_states.items():
            if obj_state.disappeared:
                continue
            
            score, level, _ = self.compute_severity(obj_state)
            
            if score >= threshold:
                high_severity.append((track_id, score))
        
        # Sort by severity (highest first)
        high_severity.sort(key=lambda x: x[1], reverse=True)
        
        return high_severity
    
    def get_stats(self) -> Dict:
        """Get severity engine statistics"""
        with self.lock:
            return {
                "tracked_violators": len(self.violation_history),
                "total_violations_recorded": sum(len(v) for v in self.violation_history.values()),
                "weights": self.weights
            }


from datetime import timedelta  # Import at top with other imports
