"""
Multi-Agent Decision System - Specialized Intelligence Agents
Each agent analyzes specific behavioral dimensions and contributes to final decision
"""

import numpy as np
from enum import Enum
from datetime import datetime


class SeverityLevel(Enum):
    """Anomaly severity classification"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class BaseAgent:
    """Base class for all intelligence agents"""
    
    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.confidence = 0.0
        self.reasoning = []
    
    def analyze(self, context):
        """
        Analyze context and return decision
        
        Returns:
            {
                'severity': SeverityLevel,
                'confidence': float (0-1),
                'reasoning': [str],
                'contributing_factors': dict
            }
        """
        raise NotImplementedError
    
    def reset(self):
        """Reset agent state"""
        self.confidence = 0.0
        self.reasoning = []


class MotionAgent(BaseAgent):
    """Analyzes motion patterns and intensity"""
    
    def __init__(self):
        super().__init__("MotionAgent", weight=1.0)
    
    def analyze(self, context):
        self.reset()
        
        motion_data = context.get('motion_data', {})
        baseline_dev = context.get('baseline_deviations', {})
        
        motion_count = motion_data.get('num_motions', 0)
        largest_area = motion_data.get('largest_area', 0)
        
        # Check motion intensity deviation
        motion_dev = baseline_dev.get('motion_rate', {})
        speed_dev = baseline_dev.get('avg_speed', {})
        
        severity = SeverityLevel.NONE
        factors = {}
        
        # Excessive motion detection
        if motion_count > 5:
            severity = SeverityLevel.MEDIUM
            self.confidence = min(1.0, motion_count / 10.0)
            self.reasoning.append(f"Multiple simultaneous objects detected ({motion_count})")
            factors['motion_count'] = motion_count
        
        # Motion pattern deviation
        if motion_dev.get('is_anomalous'):
            sigma = motion_dev.get('sigma_distance', 0)
            if abs(sigma) > 3.0:
                severity = SeverityLevel.HIGH
                self.confidence = min(1.0, abs(sigma) / 4.0)
                self.reasoning.append(f"Motion frequency {sigma:.1f}σ from baseline")
                factors['motion_sigma'] = sigma
        
        # Speed anomaly
        if speed_dev.get('is_anomalous'):
            sigma = speed_dev.get('sigma_distance', 0)
            if sigma > 2.5:
                severity = max(severity, SeverityLevel.MEDIUM)
                self.confidence = max(self.confidence, min(1.0, sigma / 3.5))
                self.reasoning.append(f"Unusual motion speed detected ({sigma:.1f}σ)")
                factors['speed_sigma'] = sigma
        
        return {
            'severity': severity,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'contributing_factors': factors
        }


class ROIAgent(BaseAgent):
    """Analyzes region-of-interest violations"""
    
    def __init__(self):
        super().__init__("ROIAgent", weight=2.0)  # Higher weight for security
    
    def analyze(self, context):
        self.reset()
        
        motion_data = context.get('motion_data', {})
        baseline_dev = context.get('baseline_deviations', {})
        
        roi_triggered = motion_data.get('roi_triggered', False)
        roi_dev = baseline_dev.get('roi_interaction_rate', {})
        
        severity = SeverityLevel.NONE
        factors = {}
        
        if roi_triggered:
            severity = SeverityLevel.HIGH
            self.confidence = 0.9
            self.reasoning.append("Object entered restricted ROI zone")
            factors['roi_breach'] = True
            
            # Check if ROI breach is unexpected
            if roi_dev.get('is_anomalous'):
                severity = SeverityLevel.CRITICAL
                self.confidence = 0.95
                self.reasoning.append("Unexpected ROI breach - baseline deviation")
                factors['unexpected_breach'] = True
        
        return {
            'severity': severity,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'contributing_factors': factors
        }


class TemporalAgent(BaseAgent):
    """Analyzes temporal context and time-of-day patterns"""
    
    def __init__(self):
        super().__init__("TemporalAgent", weight=1.2)
    
    def analyze(self, context):
        self.reset()
        
        motion_data = context.get('motion_data', {})
        baseline_summary = context.get('baseline_summary', {})
        
        current_hour = datetime.now().hour
        motion_detected = motion_data.get('motion_detected', False)
        
        severity = SeverityLevel.NONE
        factors = {}
        
        # Low-activity hours (11 PM - 5 AM)
        if current_hour >= 23 or current_hour <= 5:
            if motion_detected:
                severity = SeverityLevel.MEDIUM
                self.confidence = 0.7
                self.reasoning.append(f"Motion during low-activity hours ({current_hour}:00)")
                factors['off_hours_activity'] = True
                factors['hour'] = current_hour
        
        # Check temporal variance
        temporal_var = baseline_summary.get('baseline_metrics', {}).get('temporal_variance', 0)
        if motion_detected and temporal_var > 0.3:
            severity = max(severity, SeverityLevel.LOW)
            self.confidence = max(self.confidence, 0.5)
            self.reasoning.append("Activity pattern deviates from temporal baseline")
            factors['temporal_deviation'] = temporal_var
        
        return {
            'severity': severity,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'contributing_factors': factors
        }


class ContextAgent(BaseAgent):
    """Analyzes broader behavioral context and object persistence"""
    
    def __init__(self):
        super().__init__("ContextAgent", weight=1.0)
    
    def analyze(self, context):
        self.reset()
        
        motion_data = context.get('motion_data', {})
        baseline_dev = context.get('baseline_deviations', {})
        
        dwell_dev = baseline_dev.get('dwell_time', {})
        num_motions = motion_data.get('num_motions', 0)
        
        severity = SeverityLevel.NONE
        factors = {}
        
        # Loitering detection (high dwell time)
        if dwell_dev.get('is_anomalous'):
            sigma = dwell_dev.get('sigma_distance', 0)
            if sigma > 2.0:
                severity = SeverityLevel.MEDIUM
                self.confidence = min(1.0, sigma / 3.0)
                self.reasoning.append(f"Prolonged presence detected ({sigma:.1f}σ dwell time)")
                factors['loitering_detected'] = True
                factors['dwell_sigma'] = sigma
        
        # Unusual object clustering
        if num_motions >= 3:
            severity = max(severity, SeverityLevel.LOW)
            self.confidence = max(self.confidence, 0.6)
            self.reasoning.append(f"Multiple objects clustered ({num_motions})")
            factors['clustering'] = num_motions
        
        return {
            'severity': severity,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'contributing_factors': factors
        }


class AgentFusionSystem:
    """
    Fuses decisions from multiple agents into final verdict
    Transparent, explainable, and debuggable
    """
    
    def __init__(self):
        self.agents = [
            MotionAgent(),
            ROIAgent(),
            TemporalAgent(),
            ContextAgent()
        ]
    
    def process(self, context):
        """
        Process context through all agents and fuse decisions
        
        Returns:
            {
                'severity': str,
                'confidence': float,
                'reasoning': [str],
                'agent_contributions': dict,
                'contributing_factors': dict
            }
        """
        agent_results = []
        all_reasoning = []
        all_factors = {}
        
        # Query each agent
        for agent in self.agents:
            result = agent.analyze(context)
            agent_results.append({
                'agent': agent.name,
                'weight': agent.weight,
                'result': result
            })
            
            if result['reasoning']:
                all_reasoning.extend(result['reasoning'])
            
            all_factors[agent.name] = result['contributing_factors']
        
        # Weighted fusion
        final_severity = self._fuse_severity(agent_results)
        final_confidence = self._fuse_confidence(agent_results)
        
        return {
            'severity': final_severity.name,
            'confidence': final_confidence,
            'reasoning': all_reasoning,
            'agent_contributions': [
                {
                    'agent': r['agent'],
                    'severity': r['result']['severity'].name,
                    'confidence': r['result']['confidence'],
                    'weight': r['weight']
                }
                for r in agent_results
            ],
            'contributing_factors': all_factors
        }
    
    def _fuse_severity(self, agent_results):
        """Fuse severity levels using weighted maximum"""
        max_severity = SeverityLevel.NONE
        max_weighted_score = 0.0
        
        for result in agent_results:
            severity = result['result']['severity']
            confidence = result['result']['confidence']
            weight = result['weight']
            
            weighted_score = severity.value * confidence * weight
            
            if weighted_score > max_weighted_score:
                max_weighted_score = weighted_score
                max_severity = severity
        
        return max_severity
    
    def _fuse_confidence(self, agent_results):
        """Fuse confidence scores using weighted average"""
        total_weight = sum(r['weight'] for r in agent_results)
        
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(
            r['result']['confidence'] * r['weight']
            for r in agent_results
        )
        
        return weighted_sum / total_weight
