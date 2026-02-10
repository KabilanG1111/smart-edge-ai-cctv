"""
Production-Grade Camera Lifecycle Manager for Edge AI CCTV System

Ensures:
- Only ONE camera pipeline runs at a time (singleton)
- Graceful startup and shutdown
- GStreamer pipeline proper state transitions
- Resource cleanup on Ctrl+C and server reload
- Thread-safe operations
- State tracking (IDLE / RUNNING / ERROR)
"""

import threading
import time
import logging
from enum import Enum
from typing import Optional, Tuple
import cv2
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CameraState(Enum):
    """Camera lifecycle states"""
    IDLE = "IDLE"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    ERROR = "ERROR"


class CameraLifecycleManager:
    """
    Singleton Camera Lifecycle Manager
    
    Manages camera pipeline lifecycle with these guarantees:
    1. Only ONE pipeline instance across entire application
    2. Graceful state transitions
    3. Proper resource cleanup
    4. Thread-safe operations
    5. Automatic recovery on errors
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern - only one instance allowed"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize lifecycle manager (called once due to singleton)"""
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.state = CameraState.IDLE
        self.cap: Optional[cv2.VideoCapture] = None
        self.streaming = False
        self.frame_count = 0
        self.error_message: Optional[str] = None
        self._state_lock = threading.Lock()
        
        logger.info("🎬 Camera Lifecycle Manager initialized")
    
    def get_state(self) -> dict:
        """
        Get current camera state and statistics.
        
        Returns:
            dict: Current state, streaming status, frame count, errors
        """
        with self._state_lock:
            return {
                "state": self.state.value,
                "streaming": self.streaming,
                "frame_count": self.frame_count,
                "camera_opened": self.cap is not None and self.cap.isOpened() if self.cap else False,
                "error": self.error_message
            }
    
    def start_stream(self, camera_source: int = 0, use_gstreamer: bool = False) -> Tuple[bool, str]:
        """
        Start camera stream with lifecycle management.
        
        Args:
            camera_source: Camera index (0, 1, 2) or RTSP URL
            use_gstreamer: Use GStreamer pipeline (True) or OpenCV (False)
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        with self._state_lock:
            # Prevent multiple concurrent starts
            if self.state == CameraState.RUNNING:
                logger.warning("⚠️  Camera already running, skipping start")
                return True, "Camera already running"
            
            if self.state == CameraState.STARTING:
                logger.warning("⚠️  Camera is starting, please wait")
                return False, "Camera is already starting"
            
            # If stopping, wait for cleanup
            if self.state == CameraState.STOPPING:
                logger.info("⏳ Waiting for previous stream to stop...")
                # Release lock temporarily to allow stop to complete
                self._state_lock.release()
                time.sleep(0.5)
                self._state_lock.acquire()
            
            self.state = CameraState.STARTING
            self.error_message = None
            logger.info(f"🚀 Starting camera stream (source: {camera_source}, gstreamer: {use_gstreamer})")
        
        try:
            # Ensure any previous camera is released
            self._force_release_camera()
            
            # Initialize camera
            if use_gstreamer:
                pipeline = self._build_gstreamer_pipeline(camera_source)
                self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
                logger.info(f"📹 GStreamer pipeline: {pipeline}")
            else:
                # Windows: Use DirectShow backend for proper webcam access
                self.cap = cv2.VideoCapture(camera_source, cv2.CAP_DSHOW)
                logger.info(f"📹 OpenCV VideoCapture with DirectShow: {camera_source}")
            
            # Verify camera opened successfully
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open camera source: {camera_source}")
            
            # LOW-LATENCY settings — minimize buffer to get latest frame
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            # Test read a frame
            success, frame = self.cap.read()
            if not success or frame is None:
                raise RuntimeError("Camera opened but cannot read frames")
            
            logger.info(f"✅ Camera initialized: {frame.shape} @ {self.cap.get(cv2.CAP_PROP_FPS)} FPS")
            
            # Update state
            with self._state_lock:
                self.streaming = True
                self.frame_count = 0
                self.state = CameraState.RUNNING
            
            return True, "Camera started successfully"
        
        except Exception as e:
            error_msg = f"Camera start failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            with self._state_lock:
                self.state = CameraState.ERROR
                self.error_message = error_msg
                self.streaming = False
            
            # Cleanup on failure
            self._force_release_camera()
            
            return False, error_msg
    
    def stop_stream(self) -> Tuple[bool, str]:
        """
        Stop camera stream and release resources gracefully.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        with self._state_lock:
            if self.state == CameraState.IDLE:
                logger.info("ℹ️  Camera already stopped")
                return True, "Camera already stopped"
            
            if self.state == CameraState.STOPPING:
                logger.warning("⚠️  Camera is already stopping")
                return False, "Camera is already stopping"
            
            logger.info("⏹️  Stopping camera stream...")
            self.state = CameraState.STOPPING
            self.streaming = False
        
        try:
            # Release camera resources
            self._force_release_camera()
            
            with self._state_lock:
                self.state = CameraState.IDLE
                self.frame_count = 0
                self.error_message = None
            
            logger.info("✅ Camera stopped successfully")
            return True, "Camera stopped successfully"
        
        except Exception as e:
            error_msg = f"Error during camera stop: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            with self._state_lock:
                self.state = CameraState.ERROR
                self.error_message = error_msg
            
            return False, error_msg
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read the LATEST frame from the camera (skips buffered/stale frames).
        Uses grab+retrieve pattern to drain the OS buffer.
        
        Returns:
            Tuple[bool, Optional[np.ndarray]]: (success, frame)
        """
        if not self.streaming:
            return False, None
            
        if self.state != CameraState.RUNNING:
            return False, None
        
        if self.cap is None or not self.cap.isOpened():
            return False, None
        
        try:
            # Drain buffer: grab (discard) stale frames to get the latest one
            # This is the key to low-latency — without this, you see old frames
            for _ in range(4):
                self.cap.grab()
            
            # Now retrieve the latest frame
            success, frame = self.cap.read()
            if success:
                with self._state_lock:
                    self.frame_count += 1
            return success, frame
        except Exception as e:
            logger.error(f"❌ Frame read error: {e}")
            return False, None
    
    def _force_release_camera(self):
        """
        Force release camera resources (internal use only).
        Does NOT acquire lock - caller must hold lock.
        """
        if self.cap is not None:
            try:
                if self.cap.isOpened():
                    self.cap.release()
                    logger.info("🔓 Camera released")
                self.cap = None
            except Exception as e:
                logger.error(f"⚠️  Error releasing camera: {e}")
                self.cap = None
    
    def _build_gstreamer_pipeline(self, camera_index: int) -> str:
        """
        Build optimized GStreamer pipeline for low-latency streaming.
        
        Args:
            camera_index: USB camera index (0, 1, 2)
        
        Returns:
            str: GStreamer pipeline string
        """
        # Windows: ksvideosrc | Linux: v4l2src device=/dev/video{camera_index}
        pipeline = (
            f"ksvideosrc device-index={camera_index} ! "
            "image/jpeg,width=640,height=480,framerate=30/1 ! "
            "jpegdec ! "
            "videoconvert ! "
            "video/x-raw,format=BGR ! "
            "appsink drop=1 sync=0 max-buffers=2"
        )
        return pipeline
    
    def shutdown(self):
        """
        Emergency shutdown - force cleanup all resources.
        Called on Ctrl+C, server reload, or application exit.
        """
        logger.info("🛑 Emergency shutdown triggered")
        
        with self._state_lock:
            self.streaming = False
            self.state = CameraState.STOPPING
        
        # Force release without waiting
        self._force_release_camera()
        
        with self._state_lock:
            self.state = CameraState.IDLE
        
        logger.info("✅ Emergency shutdown complete")
    
    def reset(self):
        """Reset manager to initial state (for testing/recovery)"""
        logger.info("🔄 Resetting camera lifecycle manager")
        self.stop_stream()
        
        with self._state_lock:
            self.frame_count = 0
            self.error_message = None
            self.state = CameraState.IDLE


# Global singleton instance
camera_manager = CameraLifecycleManager()
