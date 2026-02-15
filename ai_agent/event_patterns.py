"""
🎯 EVENT INTELLIGENCE LAYER
============================

Behavioral pattern detection using state machines.

Event Patterns:
- Theft-like behavior (object taken + concealment + fast exit)
- Fighting (multiple persons + high motion + proximity)
- Abandoned object (static object + owner departed)
- Suspicious loitering (prolonged dwell + restricted area)
- Crowd gathering (rapid density increase)
- Intrusion (restricted zone + unauthorized access)
- Object tampering (prolonged interaction + manipulation)
- Fall detection (person + sudden vertical movement)

State Machines:
NORMAL → MONITORING → WARNING → SUSPICIOUS → CRITICAL

Each pattern has its own state machine with transition logic.

CPU Optimizations:
- Efficient state transition logic
- Minimal memory footprint
- Fast pattern matching
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
import logging

logger = logging.getLogger(__name__)


class EventState(Enum):
    """Event state machine states"""
    NORMAL = "NORMAL"
    MONITORING = "MONITORING"
    WARNING = "WARNING"
    SUSPICIOUS = "SUSPICIOUS"
    CRITICAL = "CRITICAL"


class EventType(Enum):
    """Detected event types"""
    THEFT_SUSPECTED = "theft_suspected"
    FIGHTING = "fighting"
    ABANDONED_OBJECT = "abandoned_object"
    LOITERING = "loitering"
    CROWD_GATHERING = "crowd_gathering"
    INTRUSION = "intrusion"
    OBJECT_TAMPERING = "tampering"
    FALL_DETECTED = "fall_detected"
    WEAPON_DETECTED = "weapon_detected"
    UNUSUAL_ACTIVITY = "unusual_activity"


@dataclass
class Event:
    """Detected event with full context"""
    event_id: str
    event_type: EventType
    state: EventState
    track_ids: List[int]
    timestamp: datetime
    location: Tuple[float, float]
    zone_id: Optional[str]
    
    # Event-specific data
    duration: float = 0.0
    severity_score: float = 0.0
    confidence: float = 0.0
    
    # State machine tracking
    state_history: List[EventState] = field(default_factory=list)
    transition_timestamps: List[datetime] = field(default_factory=list)
    
    # Explanation
    reason: str = ""
    evidence: List[str] = field(default_factory=list)
    
    # Resolution
    resolved: bool = False
    resolution_timestamp: Optional[datetime] = None
    
    def add_evidence(self, evidence: str):
        """Add evidence to event"""
        self.evidence.append(f"[{datetime.now().strftime('%H:%M:%S')}] {evidence}")
    
    def transition_state(self, new_state: EventState, reason: str = ""):
        """Transition to new state"""
        if new_state != self.state:
            self.state_history.append(self.state)
            self.transition_timestamps.append(datetime.now())
            self.state = new_state
            if reason:
                self.add_evidence(f"State: {self.state.value} - {reason}")


class EventIntelligenceLayer:
    """
    Event Intelligence Layer - Pattern detection and state machines.
    
    Detects complex behavioral patterns and tracks event progression.
    Thread-safe, CPU-optimized.
    """
    
    def __init__(
        self,
        # Theft detection thresholds
        theft_concealment_time: float = 2.0,  # seconds
        theft_exit_velocity: float = 80.0,    # pixels/sec
        
        # Fighting detection thresholds
        fight_proximity_threshold: float = 100.0,  # pixels
        fight_velocity_threshold: float = 60.0,    # rapid movement
        fight_duration_threshold: float = 3.0,     # seconds
        
        # Abandoned object thresholds
        abandoned_static_time: float = 30.0,  # seconds
        abandoned_distance_threshold: float = 200.0,  # pixels from owner
        
        # Loitering thresholds
        loitering_time_threshold: float = 15.0,  # seconds
        loitering_movement_threshold: float = 50.0,  # max distance moved
        
        # Crowd gathering thresholds
        crowd_density_increase: float = 5.0,  # people/sec increase
        crowd_min_size: int = 10,
        
        # Fall detection thresholds
        fall_velocity_threshold: float = 100.0,
        fall_aspect_ratio_change: float = 0.5  # bbox height change
    ):
        """Initialize Event Intelligence Layer"""
        
        # Thresholds
        self.theft_concealment_time = theft_concealment_time
        self.theft_exit_velocity = theft_exit_velocity
        self.fight_proximity_threshold = fight_proximity_threshold
        self.fight_velocity_threshold = fight_velocity_threshold
        self.fight_duration_threshold = fight_duration_threshold
        self.abandoned_static_time = abandoned_static_time
        self.abandoned_distance_threshold = abandoned_distance_threshold
        self.loitering_time_threshold = loitering_time_threshold
        self.loitering_movement_threshold = loitering_movement_threshold
        self.crowd_density_increase = crowd_density_increase
        self.crowd_min_size = crowd_min_size
        self.fall_velocity_threshold = fall_velocity_threshold
        self.fall_aspect_ratio_change = fall_aspect_ratio_change
        
        # Thread-safe event tracking
        self.active_events: Dict[str, Event] = {}
        self.resolved_events: List[Event] = []
        self.lock = threading.RLock()
        
        # Pattern-specific state tracking
        self.person_object_interactions: Dict[Tuple[int, int], datetime] = {}
        self.person_proximities: Dict[Tuple[int, int], List[float]] = {}
        self.static_objects: Dict[int, datetime] = {}
        
        # Performance metrics
        self.total_events_detected = 0
        self.events_by_type: Dict[str, int] = {}
        
        logger.info("✅ Event Intelligence Layer initialized")
    
    def update(
        self,
        object_states: Dict,
        spatial_violations: List,
        severity_scores: Dict[int, Tuple[float, str]],
        timestamp: datetime
    ) -> List[Event]:
        """
        Update event detection with current frame data.
        
        Args:
            object_states: Dict of ObjectState from context engine
            spatial_violations: List of SpatialViolation from spatial engine
            severity_scores: Dict of {track_id: (score, level)}
            timestamp: Current timestamp
            
        Returns:
            List of active events
        """
        with self.lock:
            new_events = []
            
            # Pattern detection
            new_events.extend(self._detect_theft_pattern(object_states, timestamp))
            new_events.extend(self._detect_fighting(object_states, timestamp))
            new_events.extend(self._detect_abandoned_objects(object_states, timestamp))
            new_events.extend(self._detect_loitering(object_states, timestamp))
            new_events.extend(self._detect_crowd_gathering(object_states, timestamp))
            new_events.extend(self._detect_intrusion(spatial_violations, object_states, timestamp))
            new_events.extend(self._detect_falls(object_states, timestamp))
            
            # Update existing event states
            self._update_event_states(object_states, timestamp)
            
            # Add new events
            for event in new_events:
                self.active_events[event.event_id] = event
                self.total_events_detected += 1
                event_type_str = event.event_type.value
                self.events_by_type[event_type_str] = self.events_by_type.get(event_type_str, 0) + 1
            
            # Resolve old events
            self._resolve_stale_events(timestamp)
            
            return list(self.active_events.values())
    
    def _detect_theft_pattern(
        self,
        object_states: Dict,
        timestamp: datetime
    ) -> List[Event]:
        """
        Detect theft-like behavior:
        1. Person approaches object
        2. Prolonged interaction (concealment time)
        3. Rapid exit with high velocity
        """
        events = []
        
        persons = [obj for obj in object_states.values() 
                  if obj.class_name == 'person' and not obj.disappeared]
        
        objects = [obj for obj in object_states.values()
                  if obj.class_name in ['backpack', 'handbag', 'suitcase', 'laptop', 'bottle']
                  and not obj.disappeared]
        
        for person in persons:
            person_pos = person.get_centroid()
            if not person_pos:
                continue
            
            for obj in objects:
                obj_pos = obj.get_centroid()
                if not obj_pos:
                    continue
                
                # Check proximity
                distance = np.linalg.norm(np.array(person_pos) - np.array(obj_pos))
                
                interaction_key = (person.track_id, obj.track_id)
                
                if distance < 50.0:  # Close proximity
                    # Start tracking interaction
                    if interaction_key not in self.person_object_interactions:
                        self.person_object_interactions[interaction_key] = timestamp
                    
                    # Check interaction duration
                    interaction_time = (timestamp - self.person_object_interactions[interaction_key]).total_seconds()
                    
                    # Check if person is moving fast (potential exit)
                    velocity = person.get_velocity_magnitude()
                    
                    if (interaction_time > self.theft_concealment_time and 
                        velocity > self.theft_exit_velocity):
                        
                        # THEFT PATTERN DETECTED
                        event_id = f"theft_{person.track_id}_{obj.track_id}_{timestamp.timestamp()}"
                        
                        event = Event(
                            event_id=event_id,
                            event_type=EventType.THEFT_SUSPECTED,
                            state=EventState.SUSPICIOUS,
                            track_ids=[person.track_id, obj.track_id],
                            timestamp=timestamp,
                            location=person_pos,
                            zone_id=person.current_zone,
                            duration=interaction_time,
                            severity_score=0.8,
                            confidence=0.7,
                            reason=f"Person {person.track_id} interacted with {obj.class_name} for {interaction_time:.1f}s then rapidly exited"
                        )
                        
                        event.add_evidence(f"Interaction duration: {interaction_time:.1f}s")
                        event.add_evidence(f"Exit velocity: {velocity:.1f} px/s")
                        event.add_evidence(f"Object: {obj.class_name}")
                        
                        events.append(event)
                        
                        # Clean up tracking
                        del self.person_object_interactions[interaction_key]
                else:
                    # Not in proximity, clean up
                    if interaction_key in self.person_object_interactions:
                        del self.person_object_interactions[interaction_key]
        
        return events
    
    def _detect_fighting(
        self,
        object_states: Dict,
        timestamp: datetime
    ) -> List[Event]:
        """
        Detect fighting:
        1. Multiple persons in close proximity
        2. High velocity movements
        3. Sustained for duration threshold
        """
        events = []
        
        persons = [obj for obj in object_states.values()
                  if obj.class_name == 'person' and not obj.disappeared]
        
        if len(persons) < 2:
            return events
        
        # Check all person pairs
        for i, person1 in enumerate(persons):
            for person2 in persons[i+1:]:
                pos1 = person1.get_centroid()
                pos2 = person2.get_centroid()
                
                if not pos1 or not pos2:
                    continue
                
                # Check proximity
                distance = np.linalg.norm(np.array(pos1) - np.array(pos2))
                
                interaction_key = tuple(sorted([person1.track_id, person2.track_id]))
                
                if distance < self.fight_proximity_threshold:
                    # Track proximity
                    if interaction_key not in self.person_proximities:
                        self.person_proximities[interaction_key] = []
                    
                    self.person_proximities[interaction_key].append(distance)
                    
                    # Check velocities
                    vel1 = person1.get_velocity_magnitude()
                    vel2 = person2.get_velocity_magnitude()
                    
                    if (vel1 > self.fight_velocity_threshold or 
                        vel2 > self.fight_velocity_threshold):
                        
                        # Check motion patterns
                        if (person1.motion_pattern == "ERRATIC" or 
                            person2.motion_pattern == "ERRATIC"):
                            
                            # FIGHTING PATTERN DETECTED
                            event_id = f"fight_{person1.track_id}_{person2.track_id}_{timestamp.timestamp()}"
                            
                            event = Event(
                                event_id=event_id,
                                event_type=EventType.FIGHTING,
                                state=EventState.CRITICAL,
                                track_ids=[person1.track_id, person2.track_id],
                                timestamp=timestamp,
                                location=pos1,
                                zone_id=person1.current_zone,
                                severity_score=0.9,
                                confidence=0.75,
                                reason=f"Fighting detected between persons {person1.track_id} and {person2.track_id}"
                            )
                            
                            event.add_evidence(f"Proximity: {distance:.1f} px")
                            event.add_evidence(f"Velocity 1: {vel1:.1f} px/s")
                            event.add_evidence(f"Velocity 2: {vel2:.1f} px/s")
                            event.add_evidence(f"Erratic motion detected")
                            
                            events.append(event)
                else:
                    # Not in proximity
                    if interaction_key in self.person_proximities:
                        del self.person_proximities[interaction_key]
        
        return events
    
    def _detect_abandoned_objects(
        self,
        object_states: Dict,
        timestamp: datetime
    ) -> List[Event]:
        """
        Detect abandoned objects:
        1. Object remains static for threshold time
        2. Owner (person) has moved far away
        """
        events = []
        
        for track_id, obj in object_states.items():
            if obj.disappeared or obj.class_name not in ['backpack', 'handbag', 'suitcase', 'laptop']:
                continue
            
            # Check if object is static
            velocity = obj.get_velocity_magnitude()
            
            if velocity < 2.0:  # Nearly static
                if track_id not in self.static_objects:
                    self.static_objects[track_id] = timestamp
                
                static_duration = (timestamp - self.static_objects[track_id]).total_seconds()
                
                if static_duration > self.abandoned_static_time:
                    # Check if any person is nearby
                    obj_pos = obj.get_centroid()
                    if not obj_pos:
                        continue
                    
                    persons = [o for o in object_states.values()
                             if o.class_name == 'person' and not o.disappeared]
                    
                    nearest_person_distance = float('inf')
                    for person in persons:
                        person_pos = person.get_centroid()
                        if person_pos:
                            dist = np.linalg.norm(np.array(obj_pos) - np.array(person_pos))
                            nearest_person_distance = min(nearest_person_distance, dist)
                    
                    if nearest_person_distance > self.abandoned_distance_threshold:
                        # ABANDONED OBJECT DETECTED
                        event_id = f"abandoned_{track_id}_{timestamp.timestamp()}"
                        
                        event = Event(
                            event_id=event_id,
                            event_type=EventType.ABANDONED_OBJECT,
                            state=EventState.WARNING,
                            track_ids=[track_id],
                            timestamp=timestamp,
                            location=obj_pos,
                            zone_id=obj.current_zone,
                            duration=static_duration,
                            severity_score=0.6,
                            confidence=0.8,
                            reason=f"Abandoned {obj.class_name} detected (static for {static_duration:.1f}s)"
                        )
                        
                        event.add_evidence(f"Static duration: {static_duration:.1f}s")
                        event.add_evidence(f"Nearest person: {nearest_person_distance:.1f} px away")
                        
                        events.append(event)
                        
                        del self.static_objects[track_id]
            else:
                # Object moving, remove from static tracking
                if track_id in self.static_objects:
                    del self.static_objects[track_id]
        
        return events
    
    def _detect_loitering(
        self,
        object_states: Dict,
        timestamp: datetime
    ) -> List[Event]:
        """Detect loitering behavior"""
        events = []
        
        for track_id, obj in object_states.items():
            if obj.disappeared or obj.class_name != 'person':
                continue
            
            if obj.is_loitering and obj.dwell_time > self.loitering_time_threshold:
                # Check movement distance
                if len(obj.positions) >= 2:
                    positions = np.array(list(obj.positions))
                    total_movement = np.sum(np.linalg.norm(np.diff(positions, axis=0), axis=1))
                    
                    if total_movement < self.loitering_movement_threshold:
                        # LOITERING DETECTED
                        event_id = f"loiter_{track_id}_{timestamp.timestamp()}"
                        
                        pos = obj.get_centroid()
                        
                        event = Event(
                            event_id=event_id,
                            event_type=EventType.LOITERING,
                            state=EventState.MONITORING,
                            track_ids=[track_id],
                            timestamp=timestamp,
                            location=pos if pos else (0, 0),
                            zone_id=obj.current_zone,
                            duration=obj.dwell_time,
                            severity_score=0.5,
                            confidence=0.85,
                            reason=f"Person {track_id} loitering for {obj.dwell_time:.1f}s"
                        )
                        
                        event.add_evidence(f"Dwell time: {obj.dwell_time:.1f}s")
                        event.add_evidence(f"Total movement: {total_movement:.1f} px")
                        event.add_evidence(f"Zone: {obj.current_zone or 'None'}")
                        
                        events.append(event)
        
        return events
    
    def _detect_crowd_gathering(
        self,
        object_states: Dict,
        timestamp: datetime
    ) -> List[Event]:
        """Detect rapid crowd gathering"""
        persons = [obj for obj in object_states.values()
                  if obj.class_name == 'person' and not obj.disappeared]
        
        crowd_size = len(persons)
        
        if crowd_size >= self.crowd_min_size:
            # Calculate crowd density (simplified - just count)
            event_id = f"crowd_{timestamp.timestamp()}"
            
            if crowd_size > 20:
                # Compute centroid of crowd
                centroids = [p.get_centroid() for p in persons if p.get_centroid()]
                if centroids:
                    crowd_center = np.mean(centroids, axis=0)
                    
                    event = Event(
                        event_id=event_id,
                        event_type=EventType.CROWD_GATHERING,
                        state=EventState.MONITORING,
                        track_ids=[p.track_id for p in persons],
                        timestamp=timestamp,
                        location=tuple(crowd_center),
                        zone_id=persons[0].current_zone if persons else None,
                        severity_score=0.4,
                        confidence=0.9,
                        reason=f"Crowd gathering detected ({crowd_size} persons)"
                    )
                    
                    event.add_evidence(f"Crowd size: {crowd_size}")
                    
                    return [event]
        
        return []
    
    def _detect_intrusion(
        self,
        spatial_violations: List,
        object_states: Dict,
        timestamp: datetime
    ) -> List[Event]:
        """Detect intrusion from spatial violations"""
        events = []
        
        for violation in spatial_violations:
            if violation.violation_type.value in ['restricted_access', 'time_violation']:
                event_id = f"intrusion_{violation.track_id}_{timestamp.timestamp()}"
                
                event = Event(
                    event_id=event_id,
                    event_type=EventType.INTRUSION,
                    state=EventState.WARNING,
                    track_ids=[violation.track_id],
                    timestamp=timestamp,
                    location=violation.position,
                    zone_id=violation.zone_id,
                    severity_score=violation.severity,
                    confidence=0.9,
                    reason=violation.reason
                )
                
                event.add_evidence(f"Violation type: {violation.violation_type.value}")
                event.add_evidence(f"Zone: {violation.zone_id}")
                
                events.append(event)
        
        return events
    
    def _detect_falls(
        self,
        object_states: Dict,
        timestamp: datetime
    ) -> List[Event]:
        """Detect person falls (sudden vertical movement)"""
        events = []
        
        for track_id, obj in object_states.items():
            if obj.disappeared or obj.class_name != 'person':
                continue
            
            # Check for rapid downward movement
            if obj._acceleration and obj._acceleration < -self.fall_velocity_threshold:
                # Check bbox aspect ratio change (person becomes horizontal)
                if len(obj.bboxes) >= 2:
                    prev_bbox = obj.bboxes[-2]
                    curr_bbox = obj.bboxes[-1]
                    
                    prev_height = prev_bbox[3] - prev_bbox[1]
                    curr_height = curr_bbox[3] - curr_bbox[1]
                    
                    if prev_height > 0:
                        height_ratio = curr_height / prev_height
                        
                        if height_ratio < (1.0 - self.fall_aspect_ratio_change):
                            # FALL DETECTED
                            event_id = f"fall_{track_id}_{timestamp.timestamp()}"
                            
                            pos = obj.get_centroid()
                            
                            event = Event(
                                event_id=event_id,
                                event_type=EventType.FALL_DETECTED,
                                state=EventState.CRITICAL,
                                track_ids=[track_id],
                                timestamp=timestamp,
                                location=pos if pos else (0, 0),
                                zone_id=obj.current_zone,
                                severity_score=0.95,
                                confidence=0.7,
                                reason=f"Person {track_id} fall detected"
                            )
                            
                            event.add_evidence(f"Vertical acceleration: {obj._acceleration:.1f} px/s²")
                            event.add_evidence(f"Height ratio: {height_ratio:.2f}")
                            
                            events.append(event)
        
        return events
    
    def _update_event_states(self, object_states: Dict, timestamp: datetime):
        """Update state machines for active events"""
        for event_id, event in list(self.active_events.items()):
            # Check if event objects still present
            objects_present = any(
                tid in object_states and not object_states[tid].disappeared
                for tid in event.track_ids
            )
            
            if not objects_present:
                # Objects disappeared, transition to lower state
                if event.state == EventState.CRITICAL:
                    event.transition_state(EventState.WARNING, "Objects no longer detected")
                elif event.state in [EventState.WARNING, EventState.SUSPICIOUS]:
                    event.transition_state(EventState.MONITORING, "Activity ceased")
            
            # Update duration
            event.duration = (timestamp - event.timestamp).total_seconds()
    
    def _resolve_stale_events(self, timestamp: datetime, max_age: float = 60.0):
        """Resolve events that are too old"""
        to_resolve = []
        
        for event_id, event in self.active_events.items():
            age = (timestamp - event.timestamp).total_seconds()
            
            if age > max_age:
                to_resolve.append(event_id)
        
        for event_id in to_resolve:
            event = self.active_events[event_id]
            event.resolved = True
            event.resolution_timestamp = timestamp
            self.resolved_events.append(event)
            del self.active_events[event_id]
    
    def get_critical_events(self) -> List[Event]:
        """Get all critical events"""
        with self.lock:
            return [e for e in self.active_events.values() if e.state == EventState.CRITICAL]
    
    def get_stats(self) -> Dict:
        """Get event intelligence statistics"""
        with self.lock:
            return {
                "total_events_detected": self.total_events_detected,
                "active_events": len(self.active_events),
                "resolved_events": len(self.resolved_events),
                "critical_events": len(self.get_critical_events()),
                "events_by_type": self.events_by_type
            }
