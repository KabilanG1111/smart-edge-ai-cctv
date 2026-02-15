"""
⏱️ TEMPORAL CONSISTENCY LAYER
==============================

Smooths predictions over time to remove flicker and noise.

Capabilities:
- Class flicker removal (majority voting)
- Confidence smoothing (exponential moving average)
- Bounding box stabilization
- Multi-frame consensus
- Temporal confidence memory
- State persistence

CPU Optimizations:
- Circular buffers for O(1) operations
- Vectorized NumPy operations
- Lazy computation
- Memory-efficient deques
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Deque
from collections import deque, Counter
from dataclasses import dataclass
import threading
import logging

logger = logging.getLogger(__name__)


@dataclass
class TemporalState:
    """Temporal state for a tracked object"""
    track_id: int
    
    # History buffers (circular)
    class_history: Deque[str] = None
    confidence_history: Deque[float] = None
    bbox_history: Deque[List[float]] = None
    
    # Smoothed outputs
    stable_class: Optional[str] = None
    stable_confidence: float = 0.0
    stable_bbox: Optional[List[float]] = None
    
    # Consensus tracking
    frames_with_current_class: int = 0
    total_frames: int = 0
    class_locked: bool = False
    
    def __post_init__(self):
        if self.class_history is None:
            self.class_history = deque(maxlen=30)
        if self.confidence_history is None:
            self.confidence_history = deque(maxlen=30)
        if self.bbox_history is None:
            self.bbox_history = deque(maxlen=10)


class TemporalConsistencyLayer:
    """
    Temporal Consistency Layer - Smooths predictions over time.
    
    Removes class flicker, stabilizes bounding boxes, maintains confidence memory.
    Thread-safe, CPU-optimized.
    """
    
    def __init__(
        self,
        history_size: int = 15,          # Frames to consider for majority vote
        bbox_smooth_frames: int = 5,      # Frames for bbox smoothing
        class_lock_threshold: int = 8,    # Consecutive frames to lock class
        class_unlock_threshold: float = 0.7,  # Ratio of contradictions to unlock
        confidence_alpha: float = 0.3,    # EMA smoothing factor (lower = more smooth)
        min_confidence_threshold: float = 0.2  # Minimum confidence to maintain
    ):
        """
        Initialize Temporal Consistency Layer
        
        Args:
            history_size: Number of frames to keep for majority voting
            bbox_smooth_frames: Number of frames for bounding box smoothing
            class_lock_threshold: Consecutive frames with same class to lock
            class_unlock_threshold: Fraction of history contradicting to unlock
            confidence_alpha: Exponential moving average alpha (0-1)
            min_confidence_threshold: Minimum confidence to keep prediction
        """
        self.history_size = history_size
        self.bbox_smooth_frames = bbox_smooth_frames
        self.class_lock_threshold = class_lock_threshold
        self.class_unlock_threshold = class_unlock_threshold
        self.confidence_alpha = confidence_alpha
        self.min_confidence_threshold = min_confidence_threshold
        
        # Thread-safe temporal state tracking
        self.temporal_states: Dict[int, TemporalState] = {}
        self.lock = threading.RLock()
        
        # Performance metrics
        self.total_flickers_prevented = 0
        self.total_frames_processed = 0
        
        logger.info("✅ Temporal Consistency Layer initialized")
    
    def update(
        self,
        frame_detections: List[Dict]
    ) -> List[Dict]:
        """
        Apply temporal smoothing to detections.
        
        Args:
            frame_detections: List of raw detections from tracker
                [{
                    'track_id': int,
                    'bbox': [x1, y1, x2, y2],
                    'confidence': float,
                    'class_name': str
                }]
        
        Returns:
            Smoothed detections with stable classes and bboxes
        """
        with self.lock:
            self.total_frames_processed += 1
            smoothed_detections = []
            
            current_ids = set()
            
            for det in frame_detections:
                track_id = det['track_id']
                current_ids.add(track_id)
                
                # Get or create temporal state
                if track_id not in self.temporal_states:
                    self.temporal_states[track_id] = TemporalState(track_id=track_id)
                
                state = self.temporal_states[track_id]
                
                # Update histories
                self._update_history(state, det)
                
                # Apply smoothing
                smooth_det = self._apply_smoothing(state, det)
                
                if smooth_det:
                    smoothed_detections.append(smooth_det)
            
            # Cleanup old states (not seen in current frame)
            # Keep them for a few frames in case object reappears
            to_remove = []
            for track_id in self.temporal_states:
                if track_id not in current_ids:
                    # Mark for removal after N frames
                    # For now, keep all (cleanup handled by context engine)
                    pass
            
            return smoothed_detections
    
    def _update_history(self, state: TemporalState, detection: Dict):
        """Update history buffers with new detection"""
        state.class_history.append(detection['class_name'])
        state.confidence_history.append(detection['confidence'])
        state.bbox_history.append(detection['bbox'])
        state.total_frames += 1
    
    def _apply_smoothing(self, state: TemporalState, detection: Dict) -> Optional[Dict]:
        """
        Apply temporal smoothing algorithms.
        
        Returns smoothed detection or None if confidence too low.
        """
        # 1. Class majority voting
        stable_class = self._get_majority_class(state)
        
        # 2. Class locking logic
        if state.stable_class == stable_class:
            state.frames_with_current_class += 1
        else:
            # Class changed
            if state.class_locked:
                # Check if we should unlock
                if self._should_unlock_class(state, stable_class):
                    state.stable_class = stable_class
                    state.frames_with_current_class = 1
                    state.class_locked = False
                    self.total_flickers_prevented += 1
                else:
                    # Keep locked class (ignore flicker)
                    stable_class = state.stable_class
                    self.total_flickers_prevented += 1
            else:
                # Not locked, accept new class
                state.stable_class = stable_class
                state.frames_with_current_class = 1
        
        # Lock class if consecutive threshold reached
        if state.frames_with_current_class >= self.class_lock_threshold:
            state.class_locked = True
        
        # 3. Confidence smoothing (Exponential Moving Average)
        raw_confidence = detection['confidence']
        if state.stable_confidence == 0.0:
            # First frame
            state.stable_confidence = raw_confidence
        else:
            # EMA: new_value = alpha * raw + (1-alpha) * prev
            state.stable_confidence = (
                self.confidence_alpha * raw_confidence +
                (1 - self.confidence_alpha) * state.stable_confidence
            )
        
        # Check minimum confidence threshold
        if state.stable_confidence < self.min_confidence_threshold:
            return None  # Filter out low confidence
        
        # 4. Bounding box smoothing (moving average)
        stable_bbox = self._smooth_bbox(state)
        
        # Build smoothed detection
        smoothed = {
            'track_id': state.track_id,
            'bbox': stable_bbox,
            'confidence': state.stable_confidence,
            'class_name': stable_class,
            'raw_class': detection['class_name'],  # Keep original for debugging
            'raw_confidence': raw_confidence,
            'class_locked': state.class_locked,
            'lock_strength': state.frames_with_current_class
        }
        
        state.stable_class = stable_class
        state.stable_bbox = stable_bbox
        
        return smoothed
    
    def _get_majority_class(self, state: TemporalState) -> str:
        """
        Get majority class from history using voting.
        CPU-optimized with Counter.
        """
        if not state.class_history:
            return "unknown"
        
        # Use only recent history for voting
        recent_history = list(state.class_history)[-self.history_size:]
        
        # Count occurrences
        class_counts = Counter(recent_history)
        
        # Return most common
        majority_class, count = class_counts.most_common(1)[0]
        
        return majority_class
    
    def _should_unlock_class(self, state: TemporalState, new_class: str) -> bool:
        """
        Determine if locked class should be unlocked.
        
        Unlocks if majority of recent history contradicts locked class.
        """
        if not state.class_history:
            return False
        
        recent_history = list(state.class_history)[-self.history_size:]
        
        # Count how many frames contradict current locked class
        contradictions = sum(1 for c in recent_history if c != state.stable_class)
        
        # Unlock if contradiction ratio exceeds threshold
        contradiction_ratio = contradictions / len(recent_history)
        
        return contradiction_ratio >= self.class_unlock_threshold
    
    def _smooth_bbox(self, state: TemporalState) -> List[float]:
        """
        Smooth bounding box using moving average.
        CPU-optimized with NumPy vectorization.
        """
        if not state.bbox_history:
            return [0, 0, 0, 0]
        
        # Convert to numpy array
        recent_bboxes = list(state.bbox_history)[-self.bbox_smooth_frames:]
        bbox_array = np.array(recent_bboxes)
        
        # Compute moving average
        smoothed = np.mean(bbox_array, axis=0)
        
        return smoothed.tolist()
    
    def get_flicker_prevention_rate(self) -> float:
        """Get percentage of flickers prevented"""
        if self.total_frames_processed == 0:
            return 0.0
        return (self.total_flickers_prevented / self.total_frames_processed) * 100
    
    def get_locked_objects(self) -> List[int]:
        """Get track IDs with locked classes"""
        with self.lock:
            return [tid for tid, state in self.temporal_states.items() if state.class_locked]
    
    def get_stats(self) -> Dict:
        """Get temporal layer statistics"""
        with self.lock:
            return {
                "tracked_objects": len(self.temporal_states),
                "locked_objects": len(self.get_locked_objects()),
                "frames_processed": self.total_frames_processed,
                "flickers_prevented": self.total_flickers_prevented,
                "prevention_rate": f"{self.get_flicker_prevention_rate():.1f}%"
            }
