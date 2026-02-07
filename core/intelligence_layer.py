"""
Intelligence Layer Orchestrator - Main Entry Point
Coordinates all AI subsystems and provides unified interface
"""

from core.behavioral_baseline import BehaviorBaseline
from core.agent_system import AgentFusionSystem
from core.cognitive_state import CognitiveStateManager


class IntelligenceLayer:
    """
    Main Intelligence Layer - Autonomous Surveillance AI
    
    Integrates:
    - Behavioral Baseline Learning
    - Multi-Agent Decision System
    - Cognitive State Management
    - Explainable Anomaly Detection
    
    Architecture:
    CPU-only, on-device, privacy-preserving, future-proof
    """
    
    def __init__(self, learning_window=500, adaptation_rate=0.01):
        """
        Initialize Intelligence Layer
        
        Args:
            learning_window: Frames for initial baseline learning
            adaptation_rate: Baseline adaptation speed (0.001-0.05)
        """
        # Core subsystems
        self.baseline = BehaviorBaseline(learning_window, adaptation_rate)
        self.agent_system = AgentFusionSystem()
        self.cognitive_state = CognitiveStateManager()
        
        # Telemetry
        self.frames_analyzed = 0
        self.anomalies_detected = 0
        self.false_positives_suppressed = 0
        
    def process_frame(self, motion_data):
        """
        Main processing pipeline for each frame
        
        Args:
            motion_data: dict {
                'motion_detected': bool,
                'num_motions': int,
                'largest_area': float,
                'centroids': [(x, y)],
                'roi_triggered': bool,
                'timestamp': float
            }
        
        Returns:
            intelligence_result: dict {
                'is_anomaly': bool,
                'severity': str,
                'confidence': float,
                'reasoning': [str],
                'explainability': dict,
                'cognitive_state': dict,
                'telemetry': dict
            }
        """
        self.frames_analyzed += 1
        
        # Step 1: Update behavioral baseline
        self.baseline.update(motion_data)
        
        # Step 2: Get baseline deviations
        baseline_deviations = self._compute_deviations(motion_data)
        
        # Step 3: Build agent context
        agent_context = {
            'motion_data': motion_data,
            'baseline_deviations': baseline_deviations,
            'baseline_summary': self.baseline.get_baseline_summary()
        }
        
        # Step 4: Multi-agent analysis
        agent_result = self.agent_system.process(agent_context)
        
        # Step 5: Update cognitive state
        self.cognitive_state.update(agent_result, agent_context['baseline_summary'])
        
        # Step 6: Determine anomaly status
        is_anomaly = agent_result['severity'] not in ['NONE', 'LOW']
        
        if is_anomaly:
            self.anomalies_detected += 1
        
        # Step 7: Build explainability payload
        explainability = self._build_explainability(
            agent_result,
            baseline_deviations,
            motion_data
        )
        
        # Step 8: Compile intelligence result
        return {
            'is_anomaly': is_anomaly,
            'severity': agent_result['severity'],
            'confidence': agent_result['confidence'],
            'reasoning': agent_result['reasoning'],
            'explainability': explainability,
            'cognitive_state': self.cognitive_state.get_state_summary(),
            'telemetry': self._get_telemetry()
        }
    
    def _compute_deviations(self, motion_data):
        """Compute baseline deviations for all metrics"""
        deviations = {}
        
        # Motion rate deviation
        motion_rate = 1.0 if motion_data['motion_detected'] else 0.0
        dev_score, is_anom, sigma = self.baseline.get_deviation(motion_rate, 'motion_rate')
        deviations['motion_rate'] = {
            'deviation_score': dev_score,
            'is_anomalous': is_anom,
            'sigma_distance': sigma
        }
        
        # Speed deviation (proxy from area)
        speed = self.baseline._estimate_speed(
            motion_data['centroids'],
            motion_data['largest_area']
        )
        dev_score, is_anom, sigma = self.baseline.get_deviation(speed, 'avg_speed')
        deviations['avg_speed'] = {
            'deviation_score': dev_score,
            'is_anomalous': is_anom,
            'sigma_distance': sigma
        }
        
        # ROI interaction deviation
        roi_rate = 1.0 if motion_data['roi_triggered'] else 0.0
        dev_score, is_anom, sigma = self.baseline.get_deviation(roi_rate, 'roi_interaction_rate')
        deviations['roi_interaction_rate'] = {
            'deviation_score': dev_score,
            'is_anomalous': is_anom,
            'sigma_distance': sigma
        }
        
        # Dwell time deviation
        dwell = float(motion_data['num_motions'])
        dev_score, is_anom, sigma = self.baseline.get_deviation(dwell, 'dwell_time')
        deviations['dwell_time'] = {
            'deviation_score': dev_score,
            'is_anomalous': is_anom,
            'sigma_distance': sigma
        }
        
        return deviations
    
    def _build_explainability(self, agent_result, deviations, motion_data):
        """
        Build structured explainability payload
        Human-readable and UI-renderable
        """
        return {
            'summary': self._generate_summary(agent_result),
            'agent_breakdown': agent_result['agent_contributions'],
            'baseline_deviations': deviations,
            'contributing_factors': agent_result['contributing_factors'],
            'confidence_factors': {
                'agent_confidence': agent_result['confidence'],
                'baseline_established': self.baseline.is_baseline_established,
                'frames_analyzed': self.frames_analyzed
            },
            'recommendations': self._generate_recommendations(agent_result['severity'])
        }
    
    def _generate_summary(self, agent_result):
        """Generate human-readable summary"""
        severity = agent_result['severity']
        confidence = agent_result['confidence']
        reasoning = agent_result['reasoning']
        
        if severity == 'NONE':
            return "No anomalous behavior detected. System monitoring normal activity."
        
        summary_parts = [
            f"{severity} severity anomaly detected (confidence: {confidence:.0%}).",
        ]
        
        if reasoning:
            summary_parts.append("Factors: " + "; ".join(reasoning[:3]))  # Top 3 reasons
        
        return " ".join(summary_parts)
    
    def _generate_recommendations(self, severity):
        """Generate actionable recommendations"""
        recommendations = {
            'NONE': ["Continue normal monitoring"],
            'LOW': ["Monitor closely for pattern development"],
            'MEDIUM': ["Review footage manually", "Consider alert notification"],
            'HIGH': ["Immediate manual review recommended", "Alert security personnel"],
            'CRITICAL': ["URGENT: Immediate response required", "Escalate to security team", "Preserve evidence"]
        }
        return recommendations.get(severity, [])
    
    def _get_telemetry(self):
        """Get system telemetry metrics"""
        return {
            'frames_analyzed': self.frames_analyzed,
            'anomalies_detected': self.anomalies_detected,
            'baseline_established': self.baseline.is_baseline_established,
            'baseline_frames': self.baseline.frames_processed,
            'detection_rate': self.anomalies_detected / max(1, self.frames_analyzed),
            'false_positives_suppressed': self.false_positives_suppressed
        }
    
    def get_system_status(self):
        """Get comprehensive system status for API/UI"""
        baseline_summary = self.baseline.get_baseline_summary()
        cognitive_summary = self.cognitive_state.get_state_summary()
        
        return {
            'intelligence_layer': {
                'status': 'OPERATIONAL',
                'cognitive_state': cognitive_summary['state'],
                'system_confidence': cognitive_summary['confidence'],
                'state_description': cognitive_summary['state_description']
            },
            'baseline': {
                'established': baseline_summary['established'],
                'progress': min(100, int((baseline_summary['frames_processed'] / self.baseline.learning_window) * 100)),
                'metrics': baseline_summary['baseline_metrics']
            },
            'telemetry': self._get_telemetry(),
            'agents': {
                'active_count': len(self.agent_system.agents),
                'agent_names': [a.name for a in self.agent_system.agents]
            }
        }
    
    def reset(self):
        """Reset intelligence layer (e.g., when stopping/restarting)"""
        self.baseline = BehaviorBaseline(self.baseline.learning_window, self.baseline.adaptation_rate)
        self.cognitive_state.reset()
        self.frames_analyzed = 0
        self.anomalies_detected = 0
        self.false_positives_suppressed = 0
