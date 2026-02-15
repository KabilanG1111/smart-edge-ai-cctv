"""
🎯 TRACKER MODULE - ByteTrack Integration for Object Tracking
============================================================

Provides:
- Unique ID assignment for detected objects
- IoU-based track association across frames
- Track lifecycle management (active, lost, removed)
- Integration with ByteTrack algorithm

ByteTrack is chosen for CPU efficiency and robustness.

Author: Production AI Team
License: Enterprise
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
import logging

logger = logging.getLogger(__name__)

try:
    from yolox.tracker.byte_tracker import BYTETracker, STrack
    from yolox.tracker.basetrack import BaseTrack, TrackState
    BYTETRACK_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ ByteTrack not available, using fallback tracker")
    BYTETRACK_AVAILABLE = False


class SimpleTrack:
    """
    Fallback simple tracker using IoU matching
    
    Used when ByteTrack is not installed.
    Provides basic tracking functionality.
    """
    _count = 0
    
    def __init__(self, tlwh: np.ndarray, score: float, class_id: int):
        """
        Initialize track
        
        Args:
            tlwh: [top, left, width, height]
            score: Confidence score
            class_id: Object class ID
        """
        SimpleTrack._count += 1
        self.track_id = SimpleTrack._count
        self.tlwh = np.array(tlwh)
        self.score = score
        self.class_id = class_id
        self.age = 0
        self.hits = 1
        self.time_since_update = 0
    
    @property
    def tlbr(self) -> np.ndarray:
        """Convert tlwh to tlbr (top-left, bottom-right)"""
        ret = self.tlwh.copy()
        ret[2:] += ret[:2]  # width, height -> x2, y2
        return ret
    
    def update(self, tlwh: np.ndarray, score: float, class_id: int):
        """Update track with new detection"""
        self.tlwh = np.array(tlwh)
        self.score = score
        self.class_id = class_id
        self.hits += 1
        self.time_since_update = 0
        self.age += 1
    
    def predict(self):
        """Predict next state (simple: no motion prediction)"""
        self.age += 1
        self.time_since_update += 1


class SimpleTracker:
    """
    Simple IoU-based tracker (fallback when ByteTrack unavailable)
    
    Algorithm:
    1. Match detections to existing tracks via IoU
    2. Update matched tracks
    3. Create new tracks for unmatched detections
    4. Remove stale tracks
    """
    
    def __init__(
        self,
        match_threshold: float = 0.3,
        max_age: int = 30,
        min_hits: int = 3
    ):
        """
        Initialize tracker
        
        Args:
            match_threshold: IoU threshold for matching (default: 0.3)
            max_age: Max frames to keep lost track (default: 30)
            min_hits: Min hits before track is confirmed (default: 3)
        """
        self.match_threshold = match_threshold
        self.max_age = max_age
        self.min_hits = min_hits
        self.tracks: List[SimpleTrack] = []
        
        logger.info("✅ Simple fallback tracker initialized")
    
    def update(
        self,
        detections: np.ndarray,
        scores: np.ndarray,
        class_ids: np.ndarray
    ) -> List[Tuple[int, np.ndarray, float, int]]:
        """
        Update tracks with new detections
        
        Args:
            detections: Nx4 array of boxes [x1, y1, x2, y2]
            scores: N confidence scores
            class_ids: N class IDs
        
        Returns:
            List of (track_id, box, score, class_id)
        """
        # Convert to tlwh format
        tlwh_detections = []
        for box in detections:
            x1, y1, x2, y2 = box
            w, h = x2 - x1, y2 - y1
            tlwh_detections.append([x1, y1, w, h])
        tlwh_detections = np.array(tlwh_detections) if tlwh_detections else np.empty((0, 4))
        
        # Predict existing tracks
        for track in self.tracks:
            track.predict()
        
        # Match detections to tracks
        matched, unmatched_dets, unmatched_tracks = self._match(
            tlwh_detections, scores, class_ids
        )
        
        # Update matched tracks
        for det_idx, track_idx in matched:
            self.tracks[track_idx].update(
                tlwh_detections[det_idx],
                scores[det_idx],
                class_ids[det_idx]
            )
        
        # Create new tracks for unmatched detections
        for det_idx in unmatched_dets:
            new_track = SimpleTrack(
                tlwh_detections[det_idx],
                scores[det_idx],
                class_ids[det_idx]
            )
            self.tracks.append(new_track)
        
        # Remove stale tracks
        self.tracks = [
            t for t in self.tracks 
            if t.time_since_update < self.max_age
        ]
        
        # Return confirmed tracks
        results = []
        for track in self.tracks:
            if track.hits >= self.min_hits:
                results.append((
                    track.track_id,
                    track.tlbr,
                    track.score,
                    track.class_id
                ))
        
        return results
    
    def _match(
        self,
        detections: np.ndarray,
        scores: np.ndarray,
        class_ids: np.ndarray
    ) -> Tuple[List[Tuple[int, int]], List[int], List[int]]:
        """
        Match detections to tracks via IoU
        
        Returns:
            (matched_pairs, unmatched_detection_indices, unmatched_track_indices)
        """
        if len(self.tracks) == 0:
            return [], list(range(len(detections))), []
        
        if len(detections) == 0:
            return [], [], list(range(len(self.tracks)))
        
        # Compute IoU matrix
        iou_matrix = np.zeros((len(detections), len(self.tracks)))
        for d, det in enumerate(detections):
            det_tlbr = np.array([det[0], det[1], det[0] + det[2], det[1] + det[3]])
            for t, track in enumerate(self.tracks):
                iou_matrix[d, t] = self._iou(det_tlbr, track.tlbr)
        
        # Greedy matching
        matched = []
        unmatched_dets = list(range(len(detections)))
        unmatched_tracks = list(range(len(self.tracks)))
        
        while iou_matrix.size > 0:
            # Find best match
            max_iou = iou_matrix.max()
            if max_iou < self.match_threshold:
                break
            
            det_idx, track_idx = np.unravel_index(iou_matrix.argmax(), iou_matrix.shape)
            matched.append((det_idx, track_idx))
            unmatched_dets.remove(det_idx)
            unmatched_tracks.remove(track_idx)
            
            # Remove matched row and column
            iou_matrix[det_idx, :] = 0
            iou_matrix[:, track_idx] = 0
        
        return matched, unmatched_dets, unmatched_tracks
    
    @staticmethod
    def _iou(box1: np.ndarray, box2: np.ndarray) -> float:
        """Compute IoU between two boxes [x1, y1, x2, y2]"""
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        
        inter_area = max(0, x2 - x1) * max(0, y2 - y1)
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0


class ByteTrackWrapper:
    """
    Wrapper for ByteTrack algorithm
    
    Provides consistent API regardless of ByteTrack availability.
    """
    
    def __init__(
        self,
        track_thresh: float = 0.5,
        track_buffer: int = 30,
        match_thresh: float = 0.8,
        frame_rate: int = 30
    ):
        """
        Initialize ByteTrack
        
        Args:
            track_thresh: High threshold for first association (default: 0.5)
            track_buffer: Frames to keep lost tracks (default: 30)
            match_thresh: Match threshold for IoU (default: 0.8)
            frame_rate: Video frame rate (default: 30)
        """
        if not BYTETRACK_AVAILABLE:
            logger.warning("ByteTrack not available, falling back to simple tracker")
            self.tracker = SimpleTracker(
                match_threshold=0.3,
                max_age=track_buffer,
                min_hits=3
            )
            self.use_bytetrack = False
        else:
            # ByteTrack config
            class Args:
                track_thresh = track_thresh
                track_buffer = track_buffer
                match_thresh = match_thresh
                mot20 = False  # Not MOT20 dataset
            
            self.tracker = BYTETracker(Args(), frame_rate=frame_rate)
            self.use_bytetrack = True
            logger.info("✅ ByteTrack initialized")
    
    def update(
        self,
        detections: np.ndarray,
        scores: np.ndarray,
        class_ids: np.ndarray
    ) -> List[Tuple[int, np.ndarray, float, int]]:
        """
        Update tracker with new frame detections
        
        Args:
            detections: Nx4 array of boxes [x1, y1, x2, y2]
            scores: N confidence scores
            class_ids: N class IDs
        
        Returns:
            List of (track_id, box, score, class_id) for active tracks
        """
        if len(detections) == 0:
            # No detections, just update tracker
            if self.use_bytetrack:
                return []
            else:
                return self.tracker.update(
                    np.empty((0, 4)),
                    np.empty(0),
                    np.empty(0, dtype=int)
                )
        
        if self.use_bytetrack:
            # ByteTrack expects [x1, y1, x2, y2, confidence]
            dets_with_scores = np.column_stack([detections, scores])
            
            # Update tracker
            online_targets = self.tracker.update(
                dets_with_scores,
                img_info=(640, 640),  # Default input size
                img_size=(640, 640)
            )
            
            # Extract results
            results = []
            for track in online_targets:
                tlbr = track.tlbr
                track_id = track.track_id
                score = track.score
                
                # Find matching class_id (closest detection)
                best_iou = 0
                best_class_id = 0
                for det, cid in zip(detections, class_ids):
                    iou = self._iou(tlbr, det)
                    if iou > best_iou:
                        best_iou = iou
                        best_class_id = cid
                
                results.append((track_id, tlbr, score, best_class_id))
            
            return results
        else:
            # Use simple tracker
            return self.tracker.update(detections, scores, class_ids)
    
    @staticmethod
    def _iou(box1: np.ndarray, box2: np.ndarray) -> float:
        """Compute IoU between two boxes [x1, y1, x2, y2]"""
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        
        inter_area = max(0, x2 - x1) * max(0, y2 - y1)
        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0


# Main tracker class for external use
class ObjectTracker:
    """
    High-level object tracker interface
    
    Provides simple API:
    - update(detections) -> tracked_objects
    - reset()
    - get_stats()
    
    Automatically selects best available tracker (ByteTrack or Simple)
    """
    
    def __init__(
        self,
        track_thresh: float = 0.5,
        track_buffer: int = 30,
        match_thresh: float = 0.8,
        frame_rate: int = 30
    ):
        """
        Initialize tracker
        
        Args:
            track_thresh: Confidence threshold for tracking (default: 0.5)
            track_buffer: Frames to keep lost tracks (default: 30)
            match_thresh: IoU match threshold (default: 0.8)
            frame_rate: Video FPS (default: 30)
        """
        self.tracker = ByteTrackWrapper(
            track_thresh=track_thresh,
            track_buffer=track_buffer,
            match_thresh=match_thresh,
            frame_rate=frame_rate
        )
        
        self.frame_count = 0
        self.total_tracks_created = 0
        
        logger.info("✅ Object Tracker initialized")
    
    def update(
        self,
        detections: List[Dict]
    ) -> List[Dict]:
        """
        Update tracker with new frame detections
        
        Args:
            detections: List of detection dicts with keys:
                - 'box': [x1, y1, x2, y2]
                - 'confidence': float
                - 'class_id': int
                - 'class_name': str
        
        Returns:
            List of tracked object dicts with additional 'track_id' key
        """
        self.frame_count += 1
        
        if not detections:
            return []
        
        # Extract numpy arrays
        boxes = np.array([d['box'] for d in detections])
        scores = np.array([d['confidence'] for d in detections])
        class_ids = np.array([d['class_id'] for d in detections])
        
        # Update tracker
        tracked = self.tracker.update(boxes, scores, class_ids)
        
        # Convert back to dict format
        results = []
        for track_id, box, score, class_id in tracked:
            # Find matching detection for class_name
            class_name = detections[0]['class_name']  # Fallback
            for det in detections:
                if det['class_id'] == class_id:
                    class_name = det['class_name']
                    break
            
            results.append({
                'track_id': int(track_id),
                'box': box.tolist(),
                'confidence': float(score),
                'class_id': int(class_id),
                'class_name': class_name
            })
        
        # Update stats
        new_ids = {r['track_id'] for r in results}
        self.total_tracks_created = max(self.total_tracks_created, max(new_ids) if new_ids else 0)
        
        return results
    
    def reset(self):
        """Reset tracker state"""
        self.tracker = ByteTrackWrapper()
        self.frame_count = 0
        logger.info("Tracker reset")
    
    def get_stats(self) -> Dict:
        """Get tracker statistics"""
        return {
            "frame_count": self.frame_count,
            "total_tracks_created": self.total_tracks_created,
            "tracker_type": "ByteTrack" if self.tracker.use_bytetrack else "Simple"
        }


if __name__ == "__main__":
    # Test tracker
    tracker = ObjectTracker()
    
    # Mock detections
    detections = [
        {'box': [100, 100, 200, 200], 'confidence': 0.9, 'class_id': 0, 'class_name': 'person'},
        {'box': [300, 150, 350, 250], 'confidence': 0.8, 'class_id': 39, 'class_name': 'bottle'}
    ]
    
    # Update tracker
    tracked = tracker.update(detections)
    print(f"Frame 1: {len(tracked)} tracked objects")
    for obj in tracked:
        print(f"  Track {obj['track_id']}: {obj['class_name']} ({obj['confidence']:.2f})")
    
    print("\nTracker stats:", tracker.get_stats())
