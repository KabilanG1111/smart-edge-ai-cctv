"""
🤖 AI REASONING AGENT CORE
==========================

Main orchestrator for the multi-layer reasoning system.

Architecture:
    Detection → Tracking → AI Agent → Event Intelligence → Alerts
    
    AI Agent Flow:
    1. Context Engine (object behavior analysis)
    2. Spatial Engine (zone/rule checking)
    3. Temporal Smoothing (flicker removal)
    4. Severity Scoring (risk assessment)
    5. Event Intelligence (pattern detection)

Performance:
- Target: <25ms per frame on CPU
- Thread-safe design
- Modular architecture
- Easy integration with existing pipeline

Usage:
    agent = AIReasoningAgent(frame_width=1920, frame_height=1080)
    
    # After ByteTrack
    events = agent.process_frame(
        detections=tracked_detections,
        frame_shape=(1080, 1920),
        timestamp=datetime.now()
    )
    
    # Check for alerts
    critical = agent.get_critical_alerts()
"""

import time
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import threading
import logging
import json
from pathlib import Path

from ai_agent.context_engine import BehavioralContextEngine
from ai_agent.spatial_engine import SpatialAwarenessEngine, Zone, ZoneType
from ai_agent.temporal_smoothing import TemporalConsistencyLayer
from ai_agent.severity_engine import SeverityScoreEngine, SeverityLevel
from ai_agent.event_patterns import EventIntelligenceLayer, Event, EventState

logger = logging.getLogger(__name__)


class AIReasoningAgent:
    """
    AI Reasoning Agent - Enterprise-grade intelligence layer.
    
    Orchestrates all reasoning layers and provides a unified interface.
    """
    
    def __init__(
        self,
        frame_width: int = 1920,
        frame_height: int = 1080,
        fps: int = 30,
        enable_context: bool = True,
        enable_spatial: bool = True,
        enable_temporal: bool = True,
        enable_severity: bool = True,
        enable_events: bool = True,
        log_dir: Optional[str] = None,
        verbose: bool = True
    ):
        """
        Initialize AI Reasoning Agent
        
        Args:
            frame_width: Video frame width
            frame_height: Video frame height
            fps: Video frame rate
            enable_context: Enable behavioral context engine
            enable_spatial: Enable spatial awareness engine
            enable_temporal: Enable temporal consistency layer
            enable_severity: Enable severity scoring engine
            enable_events: Enable event intelligence layer
            log_dir: Directory for event logs (None = no logging)
            verbose: Enable detailed logging
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.fps = fps
        self.verbose = verbose
        
        # Initialize all reasoning layers
        logger.info("=" * 80)
        logger.info("🤖 INITIALIZING AI REASONING AGENT")
        logger.info("=" * 80)
        
        # Layer 1: Behavioral Context
        self.context_engine = None
        if enable_context:
            logger.info("\n[Layer 1/5] Behavioral Context Engine")
            self.context_engine = BehavioralContextEngine(fps=fps)
        
        # Layer 2: Spatial Awareness
        self.spatial_engine = None
        if enable_spatial:
            logger.info("\n[Layer 2/5] Spatial Awareness Engine")
            self.spatial_engine = SpatialAwarenessEngine(
                frame_width=frame_width,
                frame_height=frame_height
            )
        
        # Layer 3: Temporal Consistency
        self.temporal_layer = None
        if enable_temporal:
            logger.info("\n[Layer 3/5] Temporal Consistency Layer")
            self.temporal_layer = TemporalConsistencyLayer()
        
        # Layer 4: Severity Scoring
        self.severity_engine = None
        if enable_severity:
            logger.info("\n[Layer 4/5] Severity Scoring Engine")
            self.severity_engine = SeverityScoreEngine()
        
        # Layer 5: Event Intelligence
        self.event_layer = None
        if enable_events:
            logger.info("\n[Layer 5/5] Event Intelligence Layer")
            self.event_layer = EventIntelligenceLayer()
        
        # Logging setup
        self.log_dir = Path(log_dir) if log_dir else None
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"\n📁 Event logs: {self.log_dir}")
        
        # Performance tracking
        self.frame_count = 0
        self.total_processing_time = 0.0
        self.lock = threading.RLock()
        
        # Alert thresholds
        self.critical_threshold = 0.7
        self.high_threshold = 0.5
        
        logger.info("=" * 80)
        logger.info("✅ AI REASONING AGENT READY")
        logger.info("=" * 80)
    
    def process_frame(
        self,
        detections: List[Dict],
        frame_shape: Tuple[int, int],
        timestamp: Optional[datetime] = None
    ) -> Dict:
        """
        Process a frame through all reasoning layers.
        
        Args:
            detections: List of tracked detections from ByteTrack
                [{
                    'track_id': int,
                    'bbox': [x1, y1, x2, y2],
                    'confidence': float,
                    'class_name': str
                }]
            frame_shape: (height, width) tuple
            timestamp: Frame timestamp (None = use current time)
        
        Returns:
            Dictionary with all reasoning outputs:
            {
                'smoothed_detections': List[Dict],
                'object_states': Dict[int, ObjectState],
                'spatial_violations': List[SpatialViolation],
                'severity_scores': Dict[int, Tuple[float, SeverityLevel]],
                'active_events': List[Event],
                'critical_alerts': List[Event],
                'processing_time_ms': float,
                'frame_count': int
            }
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        start_time = time.time()
        
        with self.lock:
            self.frame_count += 1
            
            # ============================================================
            # LAYER 3: TEMPORAL CONSISTENCY (Apply first to clean data)
            # ============================================================
            smoothed_detections = detections
            if self.temporal_layer:
                smoothed_detections = self.temporal_layer.update(detections)
            
            # ============================================================
            # LAYER 1: BEHAVIORAL CONTEXT
            # ============================================================
            object_states = {}
            if self.context_engine:
                object_states = self.context_engine.update(
                    frame_detections=smoothed_detections,
                    timestamp=timestamp,
                    frame_shape=frame_shape
                )
            
            # ============================================================
            # LAYER 2: SPATIAL AWARENESS
            # ============================================================
            spatial_violations = []
            if self.spatial_engine and object_states:
                spatial_violations = self.spatial_engine.update(
                    object_states=object_states,
                    timestamp=timestamp
                )
            
            # ============================================================
            # LAYER 4: SEVERITY SCORING
            # ============================================================
            severity_scores = {}
            if self.severity_engine and object_states:
                for track_id, obj_state in object_states.items():
                    if obj_state.disappeared:
                        continue
                    
                    # Get zone info
                    zone_info = None
                    if self.spatial_engine and obj_state.current_zone:
                        zone = self.spatial_engine.zones.get(obj_state.current_zone)
                        if zone:
                            zone_info = {
                                'type': zone.zone_type.value,
                                'severity_weight': zone.severity_weight
                            }
                    
                    # Get nearby crowd
                    crowd_count = len([o for o in object_states.values()
                                     if not o.disappeared and o.class_name == 'person'])
                    
                    # Compute severity
                    score, level, factors = self.severity_engine.compute_severity(
                        object_state=obj_state,
                        zone_info=zone_info,
                        crowd_count=crowd_count,
                        timestamp=timestamp
                    )
                    
                    severity_scores[track_id] = (score, level, factors)
            
            # ============================================================
            # LAYER 5: EVENT INTELLIGENCE
            # ============================================================
            active_events = []
            if self.event_layer and object_states:
                active_events = self.event_layer.update(
                    object_states=object_states,
                    spatial_violations=spatial_violations,
                    severity_scores=severity_scores,
                    timestamp=timestamp
                )
            
            # ============================================================
            # ALERT GENERATION
            # ============================================================
            critical_alerts = []
            if active_events:
                critical_alerts = [e for e in active_events 
                                 if e.state == EventState.CRITICAL or e.severity_score >= self.critical_threshold]
                
                # Log critical alerts
                if critical_alerts and self.log_dir:
                    self._log_alerts(critical_alerts, timestamp)
            
            # Performance measurement
            processing_time = (time.time() - start_time) * 1000  # ms
            self.total_processing_time += processing_time
            
            if self.verbose and self.frame_count % 30 == 0:
                avg_time = self.total_processing_time / self.frame_count
                logger.info(f"📊 Frame {self.frame_count} | Avg: {avg_time:.1f}ms | "
                          f"Objects: {len(object_states)} | Events: {len(active_events)} | "
                          f"Alerts: {len(critical_alerts)}")
            
            # Build response
            return {
                'smoothed_detections': smoothed_detections,
                'object_states': object_states,
                'spatial_violations': spatial_violations,
                'severity_scores': severity_scores,
                'active_events': active_events,
                'critical_alerts': critical_alerts,
                'processing_time_ms': processing_time,
                'frame_count': self.frame_count
            }
    
    def add_zone(
        self,
        zone_id: str,
        name: str,
        polygon: List[Tuple[float, float]],
        zone_type: str = "normal",
        **kwargs
    ):
        """
        Add a spatial zone to the agent.
        
        Args:
            zone_id: Unique zone identifier
            name: Human-readable zone name
            polygon: List of (x, y) coordinates defining zone boundary
            zone_type: Type of zone ("normal", "restricted", "entry_only", "exit_only", etc.)
            **kwargs: Additional zone parameters
        
        Example:
            agent.add_zone(
                zone_id="parking_lot",
                name="Parking Lot",
                polygon=[(100, 100), (500, 100), (500, 400), (100, 400)],
                zone_type="normal"
            )
            
            agent.add_zone(
                zone_id="restricted_area",
                name="Server Room",
                polygon=[(600, 200), (800, 200), (800, 500), (600, 500)],
                zone_type="restricted",
                severity_weight=2.0,
                allowed_classes={'person'}  # Only persons allowed
            )
        """
        if not self.spatial_engine:
            logger.warning("⚠️ Spatial engine not enabled, cannot add zones")
            return
        
        # Convert string to enum
        zone_type_enum = ZoneType.NORMAL
        for zt in ZoneType:
            if zt.value == zone_type:
                zone_type_enum = zt
                break
        
        self.spatial_engine.add_zone(
            zone_id=zone_id,
            name=name,
            polygon=polygon,
            zone_type=zone_type_enum,
            **kwargs
        )
        
        logger.info(f"➕ Zone added: {name} ({zone_type})")
    
    def get_critical_alerts(self) -> List[Event]:
        """Get all current critical alerts"""
        if self.event_layer:
            return self.event_layer.get_critical_events()
        return []
    
    def get_comprehensive_stats(self) -> Dict:
        """Get statistics from all layers"""
        stats = {
            'agent': {
                'frames_processed': self.frame_count,
                'avg_processing_time_ms': self.total_processing_time / max(1, self.frame_count),
                'frame_width': self.frame_width,
                'frame_height': self.frame_height,
                'fps': self.fps
            }
        }
        
        if self.context_engine:
            stats['context'] = self.context_engine.get_stats()
        
        if self.spatial_engine:
            stats['spatial'] = self.spatial_engine.get_stats()
        
        if self.temporal_layer:
            stats['temporal'] = self.temporal_layer.get_stats()
        
        if self.severity_engine:
            stats['severity'] = self.severity_engine.get_stats()
        
        if self.event_layer:
            stats['events'] = self.event_layer.get_stats()
        
        return stats
    
    def _log_alerts(self, alerts: List[Event], timestamp: datetime):
        """Log alerts to JSON file"""
        if not self.log_dir:
            return
        
        log_file = self.log_dir / f"alerts_{timestamp.strftime('%Y%m%d')}.jsonl"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                for alert in alerts:
                    log_entry = {
                        'timestamp': timestamp.isoformat(),
                        'event_id': alert.event_id,
                        'event_type': alert.event_type.value,
                        'state': alert.state.value,
                        'severity_score': alert.severity_score,
                        'track_ids': alert.track_ids,
                        'location': alert.location,
                        'zone_id': alert.zone_id,
                        'reason': alert.reason,
                        'evidence': alert.evidence,
                        'duration': alert.duration,
                        'confidence': alert.confidence
                    }
                    f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"❌ Failed to log alerts: {e}")
    
    def export_event_report(self, filepath: str):
        """
        Export comprehensive event report for auditing.
        
        Generates a JSON report with all detected events and statistics.
        """
        if not self.event_layer:
            logger.warning("⚠️ Event layer not enabled")
            return
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'statistics': self.get_comprehensive_stats(),
            'active_events': [],
            'resolved_events': []
        }
        
        # Active events
        for event in self.event_layer.active_events.values():
            report['active_events'].append({
                'event_id': event.event_id,
                'type': event.event_type.value,
                'state': event.state.value,
                'severity': event.severity_score,
                'timestamp': event.timestamp.isoformat(),
                'duration': event.duration,
                'reason': event.reason,
                'evidence': event.evidence
            })
        
        # Resolved events
        for event in self.event_layer.resolved_events:
            report['resolved_events'].append({
                'event_id': event.event_id,
                'type': event.event_type.value,
                'final_state': event.state.value,
                'severity': event.severity_score,
                'timestamp': event.timestamp.isoformat(),
                'resolution_time': event.resolution_timestamp.isoformat() if event.resolution_timestamp else None,
                'total_duration': event.duration,
                'reason': event.reason
            })
        
        # Write to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            logger.info(f"📄 Event report exported: {filepath}")
        except Exception as e:
            logger.error(f"❌ Failed to export report: {e}")
    
    def cleanup(self, max_age_seconds: float = 300.0):
        """
        Cleanup old objects and events to prevent memory bloat.
        
        Should be called periodically in long-running systems.
        """
        if self.context_engine:
            self.context_engine.cleanup_old_objects(max_age_seconds)
        
        logger.info(f"🧹 Cleanup complete (objects older than {max_age_seconds}s removed)")
