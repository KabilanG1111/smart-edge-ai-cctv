"""
AI Agent for Security Event Reasoning and Escalation
Rule-based + Stateful (NO LLM calls required)

Responsibilities:
- Consume low-level events from EventDetector
- Apply temporal reasoning (context + duration + frequency)
- Escalate severity dynamically
- Decide when to raise alerts
- Decide when to start/stop recording evidence
- Track event patterns over time

This is NOT a tool - this is LOGIC
"""

import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
from collections import deque, defaultdict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class AlertAction(Enum):
    """Actions the agent can trigger"""
    IGNORE = "IGNORE"                # No action needed
    MONITOR = "MONITOR"              # Watch but don't alert
    ALERT = "ALERT"                  # Raise UI alert
    RECORD = "RECORD"                # Start evidence recording
    STOP_RECORDING = "STOP_RECORDING"  # Stop evidence recording
    ESCALATE = "ESCALATE"            # Upgrade severity


@dataclass
class AgentDecision:
    """AI Agent's reasoning and decision"""
    action: AlertAction
    confidence: float
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    reasoning: List[str]
    should_record: bool
    recording_duration: int  # seconds
    alert_message: str
    metadata: Dict


class SecurityAgent:
    """
    AI Agent for intelligent event reasoning and decision-making
    
    Uses rule-based logic with stateful context tracking:
    - Temporal patterns (frequency, duration, recency)
    - Spatial patterns (location clustering)
    - Behavioral patterns (escalation paths)
    - Risk scoring (multi-factor)
    """
    
    def __init__(
        self,
        alert_cooldown: float = 30.0,  # seconds between repeat alerts
        escalation_window: float = 60.0,  # Time window for escalation
        recording_buffer: int = 5,  # Pre-event buffer seconds
        max_recording_duration: int = 120  # Max clip length
    ):
        """
        Initialize the AI security agent
        
        Args:
            alert_cooldown: Minimum time between alerts for same event type
            escalation_window: Time window to consider for escalation
            recording_buffer: Seconds of pre-event buffer for recordings
            max_recording_duration: Maximum recording length in seconds
        """
        self.alert_cooldown = alert_cooldown
        self.escalation_window = escalation_window
        self.recording_buffer = recording_buffer
        self.max_recording_duration = max_recording_duration
        
        # State tracking
        self.event_window = deque(maxlen=100)  # Recent events
        self.last_alert_time: Dict[str, float] = {}  # event_type -> timestamp
        self.active_recordings: Dict[str, Dict] = {}  # event_id -> metadata
        self.severity_escalations: Dict[str, int] = defaultdict(int)  # track_id -> count
        
        # Pattern tracking
        self.location_clusters: Dict[str, List] = defaultdict(list)
        self.frequency_counters: Dict[str, deque] = {
            "MOTION": deque(maxlen=20),
            "LOITERING": deque(maxlen=10),
            "ROI_BREACH": deque(maxlen=5),
            "INTRUSION": deque(maxlen=3),
            "CROWD": deque(maxlen=10)
        }
        
        # Risk scoring weights
        self.risk_weights = {
            "frequency": 0.3,
            "duration": 0.25,
            "severity": 0.25,
            "pattern": 0.2
        }
        
        logger.info("🤖 SecurityAgent initialized")
    
    def analyze_event(self, event: Dict) -> AgentDecision:
        """
        Analyze security event and make intelligent decision
        
        Args:
            event: SecurityEvent dict from EventDetector
            
        Returns:
            AgentDecision with action, reasoning, and recording directive
        """
        current_time = time.time()
        event_type = event["event_type"]
        severity = event["severity"]
        
        # Add to event window
        self.event_window.append(event)
        
        # Update frequency counter
        if event_type in self.frequency_counters:
            self.frequency_counters[event_type].append(current_time)
        
        # === RULE 1: INTRUSION = IMMEDIATE ALERT + RECORD ===
        if event_type == "INTRUSION":
            return self._handle_intrusion(event, current_time)
        
        # === RULE 2: ROI BREACH = IMMEDIATE ALERT + RECORD ===
        if event_type == "ROI_BREACH":
            return self._handle_roi_breach(event, current_time)
        
        # === RULE 3: LOITERING ESCALATION ===
        if event_type == "LOITERING":
            return self._handle_loitering(event, current_time)
        
        # === RULE 4: CROWD ANALYSIS ===
        if event_type == "CROWD":
            return self._handle_crowd(event, current_time)
        
        # === RULE 5: RAPID MOVEMENT ===
        if event_type == "RAPID_MOVEMENT":
            return self._handle_rapid_movement(event, current_time)
        
        # === RULE 6: MOTION (BASELINE) ===
        if event_type == "MOTION":
            return self._handle_motion(event, current_time)
        
        # Default: Monitor only
        return AgentDecision(
            action=AlertAction.MONITOR,
            confidence=0.5,
            severity="LOW",
            reasoning=["Event under observation"],
            should_record=False,
            recording_duration=0,
            alert_message="",
            metadata={}
        )
    
    def _handle_intrusion(self, event: Dict, current_time: float) -> AgentDecision:
        """CRITICAL: Unauthorized activity during restricted hours"""
        # Check alert cooldown
        if self._is_alert_on_cooldown("INTRUSION", current_time):
            return self._create_monitor_decision(event, "Alert on cooldown")
        
        # ALWAYS RECORD INTRUSIONS
        recording_duration = min(60, self.max_recording_duration)
        
        reasoning = [
            "🚨 CRITICAL: Unauthorized activity during restricted hours",
            f"Detected {event['metadata'].get('person_count', 1)} person(s)",
            f"Time: {event['metadata'].get('hour')}:00",
            "Recording initiated for forensic evidence"
        ]
        
        self.last_alert_time["INTRUSION"] = current_time
        self._start_recording(event["event_id"], recording_duration)
        
        return AgentDecision(
            action=AlertAction.ALERT,
            confidence=0.98,
            severity="CRITICAL",
            reasoning=reasoning,
            should_record=True,
            recording_duration=recording_duration,
            alert_message="INTRUSION DETECTED - After Hours Activity",
            metadata={
                "priority": "CRITICAL",
                "requires_review": True,
                "auto_notify": True
            }
        )
    
    def _handle_roi_breach(self, event: Dict, current_time: float) -> AgentDecision:
        """HIGH: Unauthorized zone entry"""
        zone_name = event["location"].get("zone", "Unknown")
        
        # Check frequency
        recent_breaches = [
            e for e in self.event_window 
            if e["event_type"] == "ROI_BREACH" and 
            current_time - e.get("timestamp_unix", 0) < 30
        ]
        
        # Escalate if repeated breaches
        confidence = min(0.95, 0.85 + len(recent_breaches) * 0.05)
        recording_duration = 30 if len(recent_breaches) < 2 else 60
        
        reasoning = [
            f"⚠️ HIGH: Unauthorized entry into {zone_name}",
            f"Object type: {event['metadata'].get('class', 'unknown')}",
            f"Confidence: {event['confidence'] * 100:.0f}%"
        ]
        
        if len(recent_breaches) > 1:
            reasoning.append(f"Pattern: {len(recent_breaches)} breaches in 30s - ESCALATING")
        
        self._start_recording(event["event_id"], recording_duration)
        
        return AgentDecision(
            action=AlertAction.ALERT,
            confidence=confidence,
            severity="HIGH",
            reasoning=reasoning,
            should_record=True,
            recording_duration=recording_duration,
            alert_message=f"Zone Breach: {zone_name}",
            metadata={"zone": zone_name, "breach_count": len(recent_breaches)}
        )
    
    def _handle_loitering(self, event: Dict, current_time: float) -> AgentDecision:
        """MEDIUM/HIGH: Person stationary too long"""
        duration = event["metadata"].get("duration", 0)
        track_id = event["track_ids"][0] if event["track_ids"] else 0
        
        # Escalate based on duration
        if duration < 10:
            severity = "MEDIUM"
            should_record = False
            recording_duration = 0
            action = AlertAction.MONITOR
            message = ""
        elif duration < 30:
            severity = "MEDIUM"
            should_record = True
            recording_duration = 20
            action = AlertAction.ALERT if not self._is_alert_on_cooldown("LOITERING", current_time) else AlertAction.RECORD
            message = "Loitering Detected"
        else:
            severity = "HIGH"
            should_record = True
            recording_duration = 45
            action = AlertAction.ALERT
            message = "Extended Loitering - Potential Threat"
            self.severity_escalations[f"loiter_{track_id}"] += 1
        
        reasoning = [
            f"Person stationary for {duration:.1f} seconds",
            f"Threshold: {self.escalation_window}s",
        ]
        
        if should_record:
            self._start_recording(event["event_id"], recording_duration)
            self.last_alert_time["LOITERING"] = current_time
            reasoning.append("Recording evidence for review")
        
        return AgentDecision(
            action=action,
            confidence=min(0.9, 0.7 + (duration / 60.0)),
            severity=severity,
            reasoning=reasoning,
            should_record=should_record,
            recording_duration=recording_duration,
            alert_message=message,
            metadata={"duration": duration, "track_id": track_id}
        )
    
    def _handle_crowd(self, event: Dict, current_time: float) -> AgentDecision:
        """MEDIUM/HIGH: Multiple people detected"""
        person_count = event["metadata"].get("person_count", 0)
        
        # Check frequency
        recent_crowds = len([
            e for e in self.event_window 
            if e["event_type"] == "CROWD" and 
            current_time - e.get("timestamp_unix", 0) < 60
        ])
        
        if person_count < 5:
            severity = "MEDIUM"
            should_record = False
            recording_duration = 0
        else:
            severity = "HIGH"
            should_record = True
            recording_duration = 30
        
        reasoning = [
            f"{person_count} people detected simultaneously",
            "Crowd density above threshold"
        ]
        
        if recent_crowds > 2:
            reasoning.append(f"Sustained crowd activity ({recent_crowds} detections/min)")
            should_record = True
        
        if should_record:
            self._start_recording(event["event_id"], recording_duration)
        
        return AgentDecision(
            action=AlertAction.MONITOR if person_count < 5 else AlertAction.ALERT,
            confidence=0.85,
            severity=severity,
            reasoning=reasoning,
            should_record=should_record,
            recording_duration=recording_duration,
            alert_message=f"Crowd Detected: {person_count} people" if person_count >= 5 else "",
            metadata={"person_count": person_count}
        )
    
    def _handle_rapid_movement(self, event: Dict, current_time: float) -> AgentDecision:
        """MEDIUM: Fast-moving object (running, vehicle)"""
        velocity = event["metadata"].get("velocity", 0)
        
        # Very fast = potential chase or danger
        if velocity > 200:
            severity = "HIGH"
            should_record = True
            recording_duration = 20
        else:
            severity = "MEDIUM"
            should_record = False
            recording_duration = 0
        
        reasoning = [
            f"Rapid movement detected: {velocity:.0f} px/frame",
            f"Object: {event['metadata'].get('class', 'unknown')}"
        ]
        
        if should_record:
            self._start_recording(event["event_id"], recording_duration)
        
        return AgentDecision(
            action=AlertAction.MONITOR,
            confidence=0.80,
            severity=severity,
            reasoning=reasoning,
            should_record=should_record,
            recording_duration=recording_duration,
            alert_message="",
            metadata={"velocity": velocity}
        )
    
    def _handle_motion(self, event: Dict, current_time: float) -> AgentDecision:
        """LOW: Basic motion detection"""
        # Motion is baseline - only monitor
        return AgentDecision(
            action=AlertAction.MONITOR,
            confidence=0.95,
            severity="LOW",
            reasoning=["General motion detected", "Monitoring activity"],
            should_record=False,
            recording_duration=0,
            alert_message="",
            metadata={}
        )
    
    def _is_alert_on_cooldown(self, event_type: str, current_time: float) -> bool:
        """Check if alert for this event type is on cooldown"""
        if event_type not in self.last_alert_time:
            return False
        
        elapsed = current_time - self.last_alert_time[event_type]
        return elapsed < self.alert_cooldown
    
    def _start_recording(self, event_id: str, duration: int):
        """Mark event as requiring recording"""
        self.active_recordings[event_id] = {
            "start_time": time.time(),
            "duration": duration,
            "status": "recording"
        }
        logger.info(f"🎥 Recording started for event {event_id[:8]} - {duration}s")
    
    def _create_monitor_decision(self, event: Dict, reason: str) -> AgentDecision:
        """Helper to create monitor-only decision"""
        return AgentDecision(
            action=AlertAction.MONITOR,
            confidence=0.6,
            severity=event["severity"],
            reasoning=[reason],
            should_record=False,
            recording_duration=0,
            alert_message="",
            metadata={}
        )
    
    def should_stop_recording(self, event_id: str) -> bool:
        """Check if recording should be stopped for this event"""
        if event_id not in self.active_recordings:
            return False
        
        recording = self.active_recordings[event_id]
        elapsed = time.time() - recording["start_time"]
        
        if elapsed >= recording["duration"]:
            del self.active_recordings[event_id]
            logger.info(f"🎥 Recording stopped for event {event_id[:8]}")
            return True
        
        return False
    
    def get_active_recordings(self) -> List[str]:
        """Get list of events currently being recorded"""
        return list(self.active_recordings.keys())
    
    def get_stats(self) -> Dict:
        """Get agent statistics"""
        return {
            "events_analyzed": len(self.event_window),
            "active_recordings": len(self.active_recordings),
            "escalation_count": sum(self.severity_escalations.values()),
            "alert_types": dict(self.last_alert_time)
        }
    
    def reset(self):
        """Reset agent state"""
        logger.info("🔄 Resetting SecurityAgent")
        self.event_window.clear()
        self.last_alert_time.clear()
        self.active_recordings.clear()
        self.severity_escalations.clear()
        for key in self.frequency_counters:
            self.frequency_counters[key].clear()


# Global singleton
security_agent = SecurityAgent(
    alert_cooldown=30.0,
    escalation_window=60.0,
    recording_buffer=5,
    max_recording_duration=120
)
