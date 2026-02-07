"""
Unified Camera Access Layer
Supports both OpenCV VideoCapture and GStreamer pipelines
"""

import cv2
from config.settings import CAMERA_INDEX, USE_GSTREAMER, GSTREAMER_SOURCE, GSTREAMER_TYPE

_cap = None  # 🔒 shared camera instance


def get_camera():
    """
    Get camera instance (singleton pattern).
    
    Returns either OpenCV VideoCapture or GStreamer camera
    based on USE_GSTREAMER configuration.
    
    Both interfaces provide the same API:
    - read() -> (bool, numpy.ndarray)
    - isOpened() -> bool
    - release() -> None
    
    Returns:
        Camera instance compatible with cv2.VideoCapture API
    """
    global _cap
    
    if _cap is None:
        if USE_GSTREAMER:
            # Use GStreamer pipeline
            from core.camera_gstreamer import GStreamerCamera
            _cap = GStreamerCamera(source=GSTREAMER_SOURCE, pipeline_type=GSTREAMER_TYPE)
        else:
            # Use standard OpenCV VideoCapture
            _cap = cv2.VideoCapture(CAMERA_INDEX)
        
        if not _cap.isOpened():
            raise RuntimeError("Camera not accessible")
    
    return _cap


def release_camera():
    """Release camera resources."""
    global _cap
    if _cap is not None:
        _cap.release()
        _cap = None
