"""
Production-Grade Evidence Recorder with Pre-Event Buffer
Records video clips when security events occur

Features:
- Circular buffer for pre-event recording (last N seconds)
- Automatic clip creation on security events
- Thread-safe frame queuing
- Metadata tagging (event_id, severity, confidence)
- MP4 encoding with H.264 codec
- Disk space management
"""

import cv2
import os
import time
import json
import threading
from datetime import datetime
from collections import deque
from typing import Optional, Dict, List
from pathlib import Path
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EvidenceRecorder:
    """
    Thread-safe video recorder with circular pre-buffer
    
    Maintains a rolling buffer of recent frames so when an event occurs,
    we can include the preceding N seconds in the recording.
    """
    
    def __init__(
        self,
        evidence_dir: str = "evidence",
        buffer_seconds: int = 5,
        fps: int = 30,
        resolution: tuple = (640, 480),
        codec: str = "mp4v",  # or "avc1" for H.264
        max_storage_mb: int = 5000  # 5GB max
    ):
        """
        Initialize evidence recorder
        
        Args:
            evidence_dir: Directory to save evidence clips
            buffer_seconds: Seconds of pre-event buffer
            fps: Frames per second
            resolution: Video resolution (width, height)
            codec: Video codec fourcc
            max_storage_mb: Maximum storage in megabytes
        """
        self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        
        self.buffer_seconds = buffer_seconds
        self.fps = fps
        self.resolution = resolution
        self.codec = cv2.VideoWriter_fourcc(*codec)
        self.max_storage_bytes = max_storage_mb * 1024 * 1024
        
        # Pre-event circular buffer
        buffer_size = fps * buffer_seconds
        self.frame_buffer = deque(maxlen=buffer_size)
        self.buffer_lock = threading.Lock()
        
        # Active recordings
        self.active_recordings: Dict[str, Dict] = {}
        self.recording_lock = threading.Lock()
        
        # Metadata storage
        self.metadata_file = self.evidence_dir / "evidence_index.json"
        self.evidence_index = self._load_index()
        
        logger.info(f"🎥 EvidenceRecorder initialized: buffer={buffer_seconds}s, fps={fps}")
    
    def add_frame(self, frame: np.ndarray):
        """
        Add frame to circular buffer
        
        Called continuously by the video pipeline to maintain pre-event buffer
        
        Args:
            frame: BGR image frame
        """
        with self.buffer_lock:
            # Store frame with timestamp
            self.frame_buffer.append({
                "frame": frame.copy(),
                "timestamp": time.time()
            })
    
    def start_recording(
        self,
        event_id: str,
        event_data: Dict,
        duration: int
    ) -> bool:
        """
        Start recording evidence clip for security event
        
        Includes pre-event buffer + duration
        
        Args:
            event_id: Unique event identifier
            event_data: Event metadata (type, severity, confidence, etc.)
            duration: Recording duration in seconds (excluding buffer)
            
        Returns:
            True if recording started successfully
        """
        with self.recording_lock:
            if event_id in self.active_recordings:
                logger.warning(f"Recording already active for event {event_id[:8]}")
                return False
            
            # Check storage space
            if not self._check_storage_space():
                logger.error("Insufficient storage space for recording")
                return False
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            event_type = event_data.get("event_type", "UNKNOWN")
            filename = f"{timestamp}_{event_type}_{event_id[:8]}.mp4"
            filepath = self.evidence_dir / filename
            
            # Initialize video writer
            writer = cv2.VideoWriter(
                str(filepath),
                self.codec,
                self.fps,
                self.resolution
            )
            
            if not writer.isOpened():
                logger.error(f"Failed to open video writer for {filepath}")
                return False
            
            # Copy pre-event buffer
            with self.buffer_lock:
                pre_event_frames = list(self.frame_buffer)
            
            # Write pre-event frames
            written_frames = 0
            for frame_data in pre_event_frames:
                frame = frame_data["frame"]
                # Resize if needed
                if frame.shape[1] != self.resolution[0] or frame.shape[0] != self.resolution[1]:
                    frame = cv2.resize(frame, self.resolution)
                writer.write(frame)
                written_frames += 1
            
            # Store recording metadata
            recording_data = {
                "event_id": event_id,
                "event_data": event_data,
                "filepath": str(filepath),
                "filename": filename,
                "start_time": time.time(),
                "duration": duration,
                "target_frames": duration * self.fps,
                "written_frames": written_frames,
                "writer": writer,
                "status": "recording"
            }
            
            self.active_recordings[event_id] = recording_data
            
            logger.info(
                f"🎬 Recording started: {filename} | "
                f"Pre-buffer: {written_frames} frames | "
                f"Target: {duration}s"
            )
            
            return True
    
    def update_recordings(self, frame: np.ndarray):
        """
        Update all active recordings with new frame
        
        Call this for every frame during streaming
        
        Args:
            frame: Current BGR frame
        """
        with self.recording_lock:
            completed = []
            
            for event_id, recording in self.active_recordings.items():
                writer = recording["writer"]
                target_frames = recording["target_frames"]
                written = recording["written_frames"]
                
                # Write frame
                frame_resized = frame
                if frame.shape[1] != self.resolution[0] or frame.shape[0] != self.resolution[1]:
                    frame_resized = cv2.resize(frame, self.resolution)
                
                writer.write(frame_resized)
                recording["written_frames"] += 1
                
                # Check if completed
                if recording["written_frames"] >= target_frames:
                    completed.append(event_id)
            
            # Finalize completed recordings
            for event_id in completed:
                self._finalize_recording(event_id)
    
    def stop_recording(self, event_id: str) -> Optional[str]:
        """
        Manually stop a recording
        
        Args:
            event_id: Event ID to stop recording
            
        Returns:
            Filepath of saved video, or None if not found
        """
        with self.recording_lock:
            if event_id not in self.active_recordings:
                return None
            
            return self._finalize_recording(event_id)
    
    def _finalize_recording(self, event_id: str) -> Optional[str]:
        """
        Finalize and save recording (must be called with recording_lock held)
        
        Args:
            event_id: Event ID
            
        Returns:
            Filepath of saved video
        """
        if event_id not in self.active_recordings:
            return None
        
        recording = self.active_recordings[event_id]
        writer = recording["writer"]
        filepath = recording["filepath"]
        
        # Release writer
        writer.release()
        
        # Get file size
        file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        
        # Update evidence index
        evidence_entry = {
            "event_id": event_id,
            "filename": recording["filename"],
            "filepath": str(filepath),
            "timestamp": datetime.now().isoformat(),
            "event_type": recording["event_data"].get("event_type", "UNKNOWN"),
            "severity": recording["event_data"].get("severity", "LOW"),
            "confidence": recording["event_data"].get("confidence", 0.0),
            "duration": recording["duration"],
            "frames": recording["written_frames"],
            "file_size": file_size,
            "metadata": recording["event_data"]
        }
        
        self.evidence_index[event_id] = evidence_entry
        self._save_index()
        
        # Remove from active
        del self.active_recordings[event_id]
        
        logger.info(
            f"✅ Recording finished: {recording['filename']} | "
            f"Frames: {recording['written_frames']} | "
            f"Size: {file_size / 1024:.1f}KB"
        )
        
        return str(filepath)
    
    def get_evidence_list(
        self,
        limit: int = 50,
        severity_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Get list of recorded evidence clips
        
        Args:
            limit: Maximum number of results
            severity_filter: Filter by severity (CRITICAL, HIGH, MEDIUM, LOW)
            
        Returns:
            List of evidence metadata dicts
        """
        evidence = list(self.evidence_index.values())
        
        # Filter by severity
        if severity_filter:
            evidence = [e for e in evidence if e["severity"] == severity_filter]
        
        # Sort by timestamp (newest first)
        evidence.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return evidence[:limit]
    
    def get_evidence_by_id(self, event_id: str) -> Optional[Dict]:
        """Get evidence metadata by event ID"""
        return self.evidence_index.get(event_id)
    
    def delete_evidence(self, event_id: str) -> bool:
        """
        Delete evidence clip and metadata
        
        Args:
            event_id: Event ID to delete
            
        Returns:
            True if deleted successfully
        """
        if event_id not in self.evidence_index:
            return False
        
        evidence = self.evidence_index[event_id]
        filepath = Path(evidence["filepath"])
        
        # Delete file
        try:
            if filepath.exists():
                filepath.unlink()
            
            # Remove from index
            del self.evidence_index[event_id]
            self._save_index()
            
            logger.info(f"🗑️ Evidence deleted: {event_id[:8]}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete evidence {event_id}: {e}")
            return False
    
    def _check_storage_space(self) -> bool:
        """Check if there's enough storage space"""
        total_size = sum(
            os.path.getsize(self.evidence_dir / e["filename"])
            for e in self.evidence_index.values()
            if os.path.exists(self.evidence_dir / e["filename"])
        )
        
        return total_size < self.max_storage_bytes
    
    def _load_index(self) -> Dict:
        """Load evidence index from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load evidence index: {e}")
        return {}
    
    def _save_index(self):
        """Save evidence index to disk"""
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.evidence_index, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save evidence index: {e}")
    
    def get_stats(self) -> Dict:
        """Get recorder statistics"""
        total_size = sum(
            e.get("file_size", 0) for e in self.evidence_index.values()
        )
        
        return {
            "total_clips": len(self.evidence_index),
            "active_recordings": len(self.active_recordings),
            "total_size_mb": total_size / (1024 * 1024),
            "buffer_frames": len(self.frame_buffer),
            "storage_usage_percent": (total_size / self.max_storage_bytes) * 100
        }
    
    def cleanup_old_evidence(self, days: int = 30) -> int:
        """
        Delete evidence older than specified days
        
        Args:
            days: Age threshold in days
            
        Returns:
            Number of clips deleted
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        deleted = 0
        
        for event_id, evidence in list(self.evidence_index.items()):
            try:
                ts = datetime.fromisoformat(evidence["timestamp"]).timestamp()
                if ts < cutoff:
                    if self.delete_evidence(event_id):
                        deleted += 1
            except Exception as e:
                logger.error(f"Error checking evidence age: {e}")
        
        logger.info(f"🧹 Cleaned up {deleted} old evidence clips")
        return deleted
    
    def reset(self):
        """Reset recorder state (but keep saved clips)"""
        with self.buffer_lock:
            self.frame_buffer.clear()
        
        with self.recording_lock:
            # Finalize any active recordings
            for event_id in list(self.active_recordings.keys()):
                self._finalize_recording(event_id)


# Global singleton
evidence_recorder = EvidenceRecorder(
    evidence_dir="evidence",
    buffer_seconds=5,
    fps=30,
    resolution=(640, 480)
)
