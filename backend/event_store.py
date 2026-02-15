"""
🎯 PRODUCTION-GRADE REASONING EVENT STORE
==========================================

Thread-safe event management for Intel Intelligence Core dashboard.
Provides structured behavioral reasoning events with human-readable explanations.

Architecture:
- Circular buffer (last 50 events)
- Thread-safe operations
- Natural language generation
- Event deduplication
- REST API integration

Usage:
    from backend.event_store import publish_event, get_events, EventType, EventSeverity
    
    # Publish an event
    event = publish_event(
        event_type=EventType.LOITERING,
        severity=EventSeverity.HIGH,
        track_id=14,
        severity_score=0.72,
        duration=42.3,
        reasoning_text="Subject ID 14 remained stationary for 42 seconds..."
    )
    
    # Retrieve events
    events = get_events(limit=50)
"""

import threading
from collections import deque
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Dict, Optional


# ============================================================
# EVENT TYPE DEFINITIONS
# ============================================================

class EventType(str, Enum):
    """Event types for behavioral analysis"""
    LOITERING = "LOITERING"
    THEFT = "THEFT_SUSPECTED"
    FIGHT = "FIGHTING"
    INTRUSION = "INTRUSION"
    ABANDONED_OBJECT = "ABANDONED_OBJECT"
    CROWD_FORMING = "CROWD_FORMING"
    ZONE_VIOLATION = "ZONE_VIOLATION"
    NORMAL = "NORMAL"


class EventSeverity(str, Enum):
    """Severity levels for events"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ============================================================
# EVENT DATA MODEL
# ============================================================

@dataclass
class ReasoningEvent:
    """Structured reasoning event with human-readable explanation"""
    event_id: int
    event_type: EventType
    severity: EventSeverity
    track_id: int
    reasoning_text: str
    timestamp: str
    severity_score: float
    duration: float  # seconds
    additional_context: dict


# ============================================================
# GLOBAL EVENT STORE (Thread-Safe Circular Buffer)
# ============================================================

event_store: deque = deque(maxlen=50)  # Last 50 events
event_store_lock = threading.Lock()
event_counter = 0


# ============================================================
# EVENT PUBLISHING
# ============================================================

def publish_event(
    event_type: EventType,
    severity: EventSeverity,
    track_id: int,
    severity_score: float,
    duration: float,
    reasoning_text: str,
    additional_context: dict = None
) -> ReasoningEvent:
    """
    Publish a structured reasoning event to the event store.
    
    Generates human-readable reasoning text with context.
    Thread-safe operation.
    
    Args:
        event_type: Type of event detected
        severity: Severity level
        track_id: Subject track ID
        severity_score: Numerical severity (0.0-1.0)
        duration: Event duration in seconds
        reasoning_text: Human-readable explanation
        additional_context: Additional metadata
    
    Returns:
        ReasoningEvent: Published event object
    """
    global event_counter
    
    with event_store_lock:
        event_counter += 1
        
        event = ReasoningEvent(
            event_id=event_counter,
            event_type=event_type,
            severity=severity,
            track_id=track_id,
            reasoning_text=reasoning_text,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            severity_score=severity_score,
            duration=duration,
            additional_context=additional_context or {}
        )
        
        event_store.append(event)
        
        return event


def get_events(limit: int = 50) -> List[Dict]:
    """
    Retrieve events from the store (newest first).
    
    Args:
        limit: Maximum number of events to return
    
    Returns:
        List[Dict]: Event data as dictionaries
    """
    with event_store_lock:
        all_events = list(event_store)
        all_events.reverse()  # Newest first
        limited_events = all_events[:limit]
        return [asdict(event) for event in limited_events]


def clear_events():
    """Clear all events from the store"""
    with event_store_lock:
        event_store.clear()


def get_event_count() -> int:
    """Get total number of events in store"""
    with event_store_lock:
        return len(event_store)


# ============================================================
# NATURAL LANGUAGE GENERATION
# ============================================================

def generate_reasoning_text(
    event_type: EventType,
    track_id: int,
    duration: float,
    obj_state: dict,
    zone_name: str = None
) -> str:
    """
    Generate human-readable reasoning text for events.
    
    Production-grade natural language generation based on:
    - Event type
    - Duration
    - Object behavior
    - Spatial context
    """
    if event_type == EventType.LOITERING:
        if zone_name:
            return f"Subject ID {track_id} remained stationary for {duration:.0f} seconds near {zone_name}. Sustained presence detected with minimal movement pattern."
        else:
            velocity = obj_state.get('velocity_avg', 0)
            return f"Subject ID {track_id} exhibited loitering behavior for {duration:.0f} seconds. Low velocity ({velocity:.1f} px/s) with extended dwell time."
    
    elif event_type == EventType.FIGHT:
        return f"Rapid oscillating motion detected involving Subject ID {track_id} and nearby tracks. High-velocity physical interaction pattern observed for {duration:.1f} seconds."
    
    elif event_type == EventType.THEFT:
        velocity = obj_state.get('velocity_avg', 0)
        return f"Subject ID {track_id} exhibited suspicious object interaction followed by rapid departure ({velocity:.1f} px/s). Concealment behavior detected."
    
    elif event_type == EventType.INTRUSION:
        if zone_name:
            return f"Unauthorized access detected: Subject ID {track_id} entered {zone_name} for {duration:.1f} seconds. Zone breach confirmed."
        else:
            return f"Subject ID {track_id} entered restricted area. Perimeter violation active for {duration:.1f} seconds."
    
    elif event_type == EventType.ZONE_VIOLATION:
        return f"Subject ID {track_id} violated zone rules in {zone_name or 'monitored area'}. Active violation duration: {duration:.1f}s."
    
    elif event_type == EventType.CROWD_FORMING:
        return f"Crowd formation detected around Subject ID {track_id}. Multiple tracks converging with {duration:.1f}s sustained proximity."
    
    elif event_type == EventType.ABANDONED_OBJECT:
        return f"Potential abandoned object detected by Subject ID {track_id}. Object left unattended for {duration:.1f} seconds."
    
    else:
        return f"Subject ID {track_id} under observation. Duration: {duration:.1f}s, Behavior: {event_type.value}."


def get_severity_level(score: float) -> EventSeverity:
    """Convert numerical severity score to categorical level"""
    if score >= 0.75:
        return EventSeverity.CRITICAL
    elif score >= 0.50:
        return EventSeverity.HIGH
    elif score >= 0.25:
        return EventSeverity.MEDIUM
    else:
        return EventSeverity.LOW
