"""
Cognitive State Model - System Self-Awareness Layer
Tracks internal AI confidence, operational readiness, and cognitive mode
"""

from enum import Enum
from datetime import datetime, timedelta


class CognitiveState(Enum):
    """System cognitive states"""
    IDLE = "IDLE"  # No activity, standby
    LEARNING = "LEARNING"  # Building baseline, low confidence
    ACTIVE = "ACTIVE"  # Normal monitoring, baseline established
    ALERT = "ALERT"  # Anomaly detected, elevated attention
    ESCALATION = "ESCALATION"  # Critical threat, maximum priority


class CognitiveStateManager:
    """
    Manages system cognitive state based on:
    - Baseline establishment status
    - Anomaly severity history
    - System confidence levels
    - Temporal context
    """
    
    def __init__(self):
        self.current_state = CognitiveState.IDLE
        self.state_history = []
        self.state_entry_time = datetime.now()
        self.confidence_level = 0.0
        
        # State transition thresholds
        self.alert_cooldown_seconds = 30
        self.escalation_threshold = 0.85
        
        # Metrics
        self.alerts_in_window = []
        self.last_anomaly_time = None
    
    def update(self, analysis_result, baseline_summary):
        """
        Update cognitive state based on current analysis
        
        Args:
            analysis_result: Output from AgentFusionSystem
            baseline_summary: Output from BehaviorBaseline
        """
        baseline_established = baseline_summary.get('established', False)
        severity = analysis_result.get('severity', 'NONE')
        confidence = analysis_result.get('confidence', 0.0)
        
        previous_state = self.current_state
        new_state = self._determine_state(
            baseline_established,
            severity,
            confidence
        )
        
        # State transition
        if new_state != self.current_state:
            self._transition_to(new_state, severity, confidence)
        
        # Update confidence
        self.confidence_level = self._compute_confidence(
            baseline_established,
            confidence,
            severity
        )
        
        # Track anomaly history
        if severity in ['MEDIUM', 'HIGH', 'CRITICAL']:
            self.last_anomaly_time = datetime.now()
            self.alerts_in_window.append({
                'time': datetime.now(),
                'severity': severity,
                'confidence': confidence
            })
            
            # Cleanup old alerts (keep last 5 minutes)
            cutoff = datetime.now() - timedelta(minutes=5)
            self.alerts_in_window = [
                a for a in self.alerts_in_window
                if a['time'] > cutoff
            ]
    
    def _determine_state(self, baseline_established, severity, confidence):
        """Determine appropriate cognitive state"""
        
        # LEARNING: Baseline not yet established
        if not baseline_established:
            return CognitiveState.LEARNING
        
        # ESCALATION: Critical threat detected
        if severity == 'CRITICAL' and confidence >= self.escalation_threshold:
            return CognitiveState.ESCALATION
        
        # ALERT: Significant anomaly detected
        if severity in ['HIGH', 'CRITICAL']:
            return CognitiveState.ALERT
        
        if severity == 'MEDIUM' and confidence >= 0.7:
            return CognitiveState.ALERT
        
        # ACTIVE: Normal monitoring
        if severity in ['NONE', 'LOW']:
            # Check if we should stay in ALERT (cooldown)
            if self.current_state == CognitiveState.ALERT:
                time_since_entry = (datetime.now() - self.state_entry_time).total_seconds()
                if time_since_entry < self.alert_cooldown_seconds:
                    return CognitiveState.ALERT
            
            # Check recent alert history
            if len(self.alerts_in_window) >= 3:
                return CognitiveState.ALERT
            
            return CognitiveState.ACTIVE
        
        return CognitiveState.ACTIVE
    
    def _transition_to(self, new_state, severity, confidence):
        """Handle state transition"""
        self.state_history.append({
            'from': self.current_state.value,
            'to': new_state.value,
            'time': datetime.now(),
            'trigger': {
                'severity': severity,
                'confidence': confidence
            }
        })
        
        # Keep only recent history
        if len(self.state_history) > 100:
            self.state_history.pop(0)
        
        self.current_state = new_state
        self.state_entry_time = datetime.now()
    
    def _compute_confidence(self, baseline_established, agent_confidence, severity):
        """
        Compute system-level confidence score
        
        Factors:
        - Baseline establishment (0-40%)
        - Agent confidence (0-40%)
        - State stability (0-20%)
        """
        confidence = 0.0
        
        # Baseline contribution
        if baseline_established:
            confidence += 0.4
        
        # Agent confidence contribution
        confidence += agent_confidence * 0.4
        
        # State stability contribution
        time_in_state = (datetime.now() - self.state_entry_time).total_seconds()
        stability_factor = min(1.0, time_in_state / 30.0)  # Stable after 30s
        confidence += stability_factor * 0.2
        
        return min(1.0, confidence)
    
    def get_state_summary(self):
        """Get current cognitive state for telemetry"""
        time_in_state = (datetime.now() - self.state_entry_time).total_seconds()
        
        return {
            'state': self.current_state.value,
            'confidence': self.confidence_level,
            'time_in_state': time_in_state,
            'recent_alerts': len(self.alerts_in_window),
            'last_anomaly_time': self.last_anomaly_time.isoformat() if self.last_anomaly_time else None,
            'state_description': self._get_state_description()
        }
    
    def _get_state_description(self):
        """Human-readable state description"""
        descriptions = {
            CognitiveState.IDLE: "System standby - awaiting activation",
            CognitiveState.LEARNING: "Establishing behavioral baseline - learning mode",
            CognitiveState.ACTIVE: "Normal surveillance mode - monitoring active",
            CognitiveState.ALERT: "Anomaly detected - heightened attention",
            CognitiveState.ESCALATION: "Critical threat detected - maximum priority"
        }
        return descriptions.get(self.current_state, "Unknown state")
    
    def reset(self):
        """Reset cognitive state"""
        self.current_state = CognitiveState.IDLE
        self.state_entry_time = datetime.now()
        self.confidence_level = 0.0
        self.alerts_in_window = []
        self.last_anomaly_time = None
