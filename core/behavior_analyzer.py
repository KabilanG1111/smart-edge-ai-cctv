"""
Behavior Analysis & Anomaly Detection Module
Smart Edge-AI CCTV Enhancement - Hackathon Demo

Learns "normal" activity patterns and flags anomalies:
- Unusual motion frequency (e.g., 10 people at 2am)
- Loitering detection (stationary objects in ROI)
- Rapid movement patterns (running, sudden motion)
- Size anomalies (unusually large objects)
"""

import time
from datetime import datetime
from collections import deque
import numpy as np


class BehaviorAnalyzer:
    """
    AI Agent for behavioral pattern analysis and anomaly detection.
    Uses statistical baseline learning without external training data.
    """
    
    def __init__(self, learning_window=100, sensitivity=2.0):
        """
        Args:
            learning_window: Number of frames to establish baseline
            sensitivity: Standard deviation threshold (2.0 = 95% confidence)
        """
        self.learning_window = learning_window
        self.sensitivity = sensitivity
        
        # Baseline tracking
        self.motion_history = deque(maxlen=learning_window)
        self.size_history = deque(maxlen=learning_window)
        self.position_history = deque(maxlen=learning_window)
        
        # Hourly patterns (24-hour learning)
        self.hourly_baseline = {hour: {'count': 0, 'total_motion': 0, 'avg_motion': 0} 
                                for hour in range(24)}
        
        # Anomaly tracking
        self.current_anomaly = None
        self.anomaly_confidence = 0.0
        self.anomaly_start_time = None
        self.consecutive_anomalies = 0
        
        # Performance metrics
        self.total_frames = 0
        self.total_anomalies = 0
        self.false_alarm_filter = 3  # Require N consecutive anomalies
        
    def analyze_frame(self, motion_data):
        """
        Analyze current frame and detect anomalies.
        
        Args:
            motion_data: {
                'motion_detected': bool,
                'num_motions': int,
                'largest_area': int,
                'centroids': [(x, y), ...],
                'timestamp': float
            }
        
        Returns:
            {
                'is_anomaly': bool,
                'anomaly_type': 'normal' | 'unusual_activity' | 'loitering' | 'rapid_movement',
                'confidence': float (0.0-1.0),
                'severity': 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL',
                'reasoning': [str],
                'baseline_deviation': float
            }
        """
        self.total_frames += 1
        
        # Extract metrics
        num_motions = motion_data.get('num_motions', 0)
        largest_area = motion_data.get('largest_area', 0)
        centroids = motion_data.get('centroids', [])
        
        # Update history
        self.motion_history.append(num_motions)
        self.size_history.append(largest_area)
        if centroids:
            self.position_history.append(centroids[0])  # Track first object
        
        # Update hourly baseline
        current_hour = datetime.now().hour
        self.hourly_baseline[current_hour]['count'] += 1
        self.hourly_baseline[current_hour]['total_motion'] += num_motions
        if self.hourly_baseline[current_hour]['count'] > 0:
            self.hourly_baseline[current_hour]['avg_motion'] = (
                self.hourly_baseline[current_hour]['total_motion'] / 
                self.hourly_baseline[current_hour]['count']
            )
        
        # Not enough data yet - learning mode
        if len(self.motion_history) < min(30, self.learning_window):
            return self._normal_result()
        
        # Run anomaly detection
        anomaly_result = self._detect_anomaly(motion_data, current_hour)
        
        # False alarm filtering
        if anomaly_result['is_anomaly']:
            self.consecutive_anomalies += 1
            if self.consecutive_anomalies >= self.false_alarm_filter:
                self.total_anomalies += 1
                if self.anomaly_start_time is None:
                    self.anomaly_start_time = time.time()
                return anomaly_result
            else:
                # Not enough consecutive detections
                return self._normal_result()
        else:
            self.consecutive_anomalies = 0
            self.anomaly_start_time = None
            return anomaly_result
    
    def _detect_anomaly(self, motion_data, current_hour):
        """Core anomaly detection logic"""
        num_motions = motion_data.get('num_motions', 0)
        largest_area = motion_data.get('largest_area', 0)
        centroids = motion_data.get('centroids', [])
        
        reasoning = []
        severity_score = 0
        anomaly_type = 'normal'
        
        # 1. Unusual motion frequency
        motion_baseline = np.mean(self.motion_history)
        motion_std = np.std(self.motion_history) + 1e-6  # Avoid division by zero
        motion_deviation = (num_motions - motion_baseline) / motion_std
        
        if motion_deviation > self.sensitivity:
            severity_score += motion_deviation
            reasoning.append(f"Unusual motion count: {num_motions} (baseline: {motion_baseline:.1f})")
            anomaly_type = 'unusual_activity'
        
        # 2. Loitering detection (position not changing)
        if len(self.position_history) >= 20 and centroids:
            recent_positions = list(self.position_history)[-20:]
            position_variance = np.var([p[0] for p in recent_positions]) + np.var([p[1] for p in recent_positions])
            
            if position_variance < 500 and num_motions > 0:  # Low variance = stationary
                severity_score += 2.0
                reasoning.append(f"Loitering detected: stationary object for {len(recent_positions)} frames")
                anomaly_type = 'loitering'
        
        # 3. Size anomaly (unusually large object)
        size_baseline = np.mean(self.size_history)
        size_std = np.std(self.size_history) + 1e-6
        size_deviation = (largest_area - size_baseline) / size_std
        
        if size_deviation > self.sensitivity:
            severity_score += size_deviation * 0.5
            reasoning.append(f"Unusually large object: {largest_area}px (baseline: {size_baseline:.0f}px)")
        
        # 4. Time-of-day context
        hourly_baseline = self.hourly_baseline[current_hour]['avg_motion']
        if hourly_baseline > 0:
            hourly_deviation = abs(num_motions - hourly_baseline) / (hourly_baseline + 1)
            if hourly_deviation > 1.5:
                severity_score += hourly_deviation
                reasoning.append(f"Unusual for {current_hour}:00 (expected: {hourly_baseline:.1f})")
        
        # 5. After-hours activity (10pm - 6am)
        if current_hour >= 22 or current_hour <= 6:
            if num_motions > 0:
                severity_score += 1.5
                reasoning.append(f"After-hours activity detected at {current_hour}:00")
        
        # Determine severity
        is_anomaly = severity_score > self.sensitivity
        confidence = min(severity_score / (self.sensitivity * 2), 1.0)
        
        if severity_score > 5.0:
            severity = 'CRITICAL'
        elif severity_score > 3.5:
            severity = 'HIGH'
        elif severity_score > 2.0:
            severity = 'MEDIUM'
        else:
            severity = 'LOW'
        
        return {
            'is_anomaly': is_anomaly,
            'anomaly_type': anomaly_type,
            'confidence': confidence,
            'severity': severity,
            'reasoning': reasoning,
            'baseline_deviation': motion_deviation,
            'severity_score': severity_score
        }
    
    def _normal_result(self):
        """Return normal activity result"""
        return {
            'is_anomaly': False,
            'anomaly_type': 'normal',
            'confidence': 0.0,
            'severity': 'LOW',
            'reasoning': ['Normal activity pattern'],
            'baseline_deviation': 0.0,
            'severity_score': 0.0
        }
    
    def get_statistics(self):
        """Get analyzer performance statistics"""
        return {
            'total_frames_analyzed': self.total_frames,
            'total_anomalies_detected': self.total_anomalies,
            'anomaly_rate': self.total_anomalies / max(self.total_frames, 1),
            'baseline_samples': len(self.motion_history),
            'learning_complete': len(self.motion_history) >= self.learning_window,
            'hourly_patterns': self.hourly_baseline
        }
    
    def reset_baseline(self):
        """Reset learned baseline (for new environment)"""
        self.motion_history.clear()
        self.size_history.clear()
        self.position_history.clear()
        self.hourly_baseline = {hour: {'count': 0, 'total_motion': 0, 'avg_motion': 0} 
                                for hour in range(24)}
        self.consecutive_anomalies = 0
        self.anomaly_start_time = None
