"""
Behavioral Intelligence Core - Temporal Baseline Learning System
Continuously learns "normal behavior" patterns using adaptive statistics
CPU-only, on-device, privacy-preserving
"""

import numpy as np
from collections import deque
from datetime import datetime
import json


class BehaviorBaseline:
    """
    Learns and maintains a baseline of normal behavior using:
    - Motion frequency and intensity
    - Object trajectory patterns
    - Temporal patterns (hour-of-day, day-of-week)
    - ROI interaction statistics
    - Speed and dwell time distributions
    """
    
    def __init__(self, learning_window=500, adaptation_rate=0.01):
        """
        Args:
            learning_window: Number of frames for initial baseline learning
            adaptation_rate: How fast baseline adapts (0.001-0.05 recommended)
        """
        self.learning_window = learning_window
        self.adaptation_rate = adaptation_rate
        
        # Behavioral metrics storage
        self.motion_history = deque(maxlen=learning_window)
        self.speed_history = deque(maxlen=learning_window)
        self.dwell_history = deque(maxlen=learning_window)
        self.roi_interaction_history = deque(maxlen=learning_window)
        self.temporal_patterns = {}  # hour -> {motion_rate, avg_speed}
        
        # Learned baseline statistics
        self.baseline = {
            'motion_rate': {'mean': 0.0, 'std': 0.1},
            'avg_speed': {'mean': 0.0, 'std': 0.1},
            'roi_interaction_rate': {'mean': 0.0, 'std': 0.1},
            'dwell_time': {'mean': 0.0, 'std': 0.1},
            'temporal_variance': 0.0
        }
        
        # Learning state
        self.frames_processed = 0
        self.is_baseline_established = False
        self.last_adaptation_time = datetime.now()
        
    def update(self, frame_data):
        """
        Update baseline with new frame observation
        
        Args:
            frame_data: dict with keys:
                - motion_detected: bool
                - num_motions: int
                - largest_area: float
                - centroids: list of (x, y)
                - roi_triggered: bool
                - timestamp: float
        """
        self.frames_processed += 1
        
        # Extract behavioral signals
        motion_rate = 1.0 if frame_data['motion_detected'] else 0.0
        speed = self._estimate_speed(frame_data['centroids'], frame_data['largest_area'])
        dwell = self._estimate_dwell(frame_data['num_motions'])
        roi_interaction = 1.0 if frame_data['roi_triggered'] else 0.0
        
        # Store in history
        self.motion_history.append(motion_rate)
        self.speed_history.append(speed)
        self.dwell_history.append(dwell)
        self.roi_interaction_history.append(roi_interaction)
        
        # Update temporal patterns
        hour = datetime.now().hour
        self._update_temporal_pattern(hour, motion_rate, speed)
        
        # Compute baseline after learning window
        if self.frames_processed >= self.learning_window and not self.is_baseline_established:
            self._compute_initial_baseline()
            self.is_baseline_established = True
        
        # Adaptive baseline update (slow drift)
        elif self.is_baseline_established:
            self._adapt_baseline(motion_rate, speed, dwell, roi_interaction)
    
    def _estimate_speed(self, centroids, largest_area):
        """Estimate motion speed from object area (proxy for velocity)"""
        if largest_area == 0:
            return 0.0
        # Normalize area to speed estimate (0-100 scale)
        return min(100.0, np.sqrt(largest_area) / 10.0)
    
    def _estimate_dwell(self, num_motions):
        """Estimate dwell time from object persistence"""
        return float(num_motions)
    
    def _update_temporal_pattern(self, hour, motion_rate, speed):
        """Track hour-specific behavioral patterns"""
        if hour not in self.temporal_patterns:
            self.temporal_patterns[hour] = {
                'motion_samples': [],
                'speed_samples': []
            }
        
        patterns = self.temporal_patterns[hour]
        patterns['motion_samples'].append(motion_rate)
        patterns['speed_samples'].append(speed)
        
        # Keep only recent samples (last 100 per hour)
        if len(patterns['motion_samples']) > 100:
            patterns['motion_samples'].pop(0)
            patterns['speed_samples'].pop(0)
    
    def _compute_initial_baseline(self):
        """Compute initial baseline statistics from learning window"""
        if len(self.motion_history) == 0:
            return
        
        self.baseline['motion_rate'] = {
            'mean': np.mean(self.motion_history),
            'std': max(0.1, np.std(self.motion_history))
        }
        
        self.baseline['avg_speed'] = {
            'mean': np.mean(self.speed_history),
            'std': max(0.1, np.std(self.speed_history))
        }
        
        self.baseline['roi_interaction_rate'] = {
            'mean': np.mean(self.roi_interaction_history),
            'std': max(0.1, np.std(self.roi_interaction_history))
        }
        
        self.baseline['dwell_time'] = {
            'mean': np.mean(self.dwell_history),
            'std': max(0.1, np.std(self.dwell_history))
        }
        
        # Compute temporal variance
        hourly_means = []
        for hour_data in self.temporal_patterns.values():
            if len(hour_data['motion_samples']) > 0:
                hourly_means.append(np.mean(hour_data['motion_samples']))
        
        if len(hourly_means) > 1:
            self.baseline['temporal_variance'] = np.std(hourly_means)
        else:
            self.baseline['temporal_variance'] = 0.1
    
    def _adapt_baseline(self, motion_rate, speed, dwell, roi_interaction):
        """Slowly adapt baseline to prevent drift while maintaining sensitivity"""
        alpha = self.adaptation_rate
        
        # Exponential moving average
        self.baseline['motion_rate']['mean'] = (
            alpha * motion_rate + (1 - alpha) * self.baseline['motion_rate']['mean']
        )
        
        self.baseline['avg_speed']['mean'] = (
            alpha * speed + (1 - alpha) * self.baseline['avg_speed']['mean']
        )
        
        self.baseline['roi_interaction_rate']['mean'] = (
            alpha * roi_interaction + (1 - alpha) * self.baseline['roi_interaction_rate']['mean']
        )
        
        self.baseline['dwell_time']['mean'] = (
            alpha * dwell + (1 - alpha) * self.baseline['dwell_time']['mean']
        )
    
    def get_deviation(self, current_value, metric_name):
        """
        Calculate z-score deviation from baseline
        
        Returns:
            (deviation_score, is_anomalous, sigma_distance)
        """
        if not self.is_baseline_established:
            return 0.0, False, 0.0
        
        baseline = self.baseline.get(metric_name)
        if not baseline:
            return 0.0, False, 0.0
        
        mean = baseline['mean']
        std = baseline['std']
        
        # Z-score
        sigma_distance = (current_value - mean) / std if std > 0 else 0.0
        
        # Anomaly threshold: 2+ standard deviations
        is_anomalous = abs(sigma_distance) > 2.0
        
        # Normalized deviation score (0-1)
        deviation_score = min(1.0, abs(sigma_distance) / 3.0)
        
        return deviation_score, is_anomalous, sigma_distance
    
    def get_baseline_summary(self):
        """Get current baseline state for telemetry"""
        return {
            'established': self.is_baseline_established,
            'frames_processed': self.frames_processed,
            'baseline_metrics': self.baseline,
            'temporal_patterns_tracked': len(self.temporal_patterns),
            'adaptation_rate': self.adaptation_rate
        }
