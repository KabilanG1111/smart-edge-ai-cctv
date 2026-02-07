"""
GStreamer-based Camera Module for CCTV System
Drop-in replacement for cv2.VideoCapture with optimized low-latency pipelines
Supports: USB webcams, RTSP streams
CPU-only, no GPU dependencies
"""

import cv2
import numpy as np


class GStreamerCamera:
    """
    GStreamer camera interface compatible with OpenCV VideoCapture API.
    
    Provides the same methods as cv2.VideoCapture:
    - read() -> (bool, numpy.ndarray)
    - isOpened() -> bool
    - release() -> None
    
    Optimized for low-latency CPU processing on Intel i5.
    """
    
    def __init__(self, source, pipeline_type='usb'):
        """
        Initialize GStreamer camera.
        
        Args:
            source: Camera source
                    - USB: 0, 1, 2 (camera index)
                    - RTSP: "rtsp://username:password@ip:port/stream"
            pipeline_type: 'usb' or 'rtsp'
        """
        self.source = source
        self.pipeline_type = pipeline_type
        self.cap = None
        self._init_pipeline()
    
    def _init_pipeline(self):
        """Initialize GStreamer pipeline based on source type."""
        
        if self.pipeline_type == 'usb':
            # USB webcam pipeline - optimized for low latency
            pipeline = self._build_usb_pipeline(self.source)
        elif self.pipeline_type == 'rtsp':
            # RTSP stream pipeline - optimized for network cameras
            pipeline = self._build_rtsp_pipeline(self.source)
        else:
            raise ValueError(f"Unknown pipeline type: {self.pipeline_type}")
        
        # Open with GStreamer backend
        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open GStreamer pipeline: {pipeline}")
    
    def _build_usb_pipeline(self, camera_index):
        """
        Build GStreamer pipeline for USB webcam.
        
        Optimized for:
        - Low latency (minimal buffering)
        - CPU-only processing
        - Direct conversion to BGR for OpenCV
        
        Args:
            camera_index: USB camera index (0, 1, 2, etc.)
        
        Returns:
            GStreamer pipeline string
        """
        # Windows: ksvideosrc (Kernel Streaming Video Source)
        # Linux alternative: v4l2src device=/dev/video{camera_index}
        
        pipeline = (
            f"ksvideosrc device-index={camera_index} ! "
            "image/jpeg,width=640,height=480,framerate=30/1 ! "
            "jpegdec ! "
            "videoconvert ! "
            "video/x-raw,format=BGR ! "
            "appsink drop=1 sync=0 max-buffers=2"
        )
        
        return pipeline
    
    def _build_rtsp_pipeline(self, rtsp_url):
        """
        Build GStreamer pipeline for RTSP stream.
        
        Optimized for:
        - Low latency (minimal buffering)
        - Network jitter handling
        - CPU-only decoding (no NVDEC/hardware acceleration)
        - Automatic reconnection on stream loss
        
        Args:
            rtsp_url: RTSP stream URL
                     Example: "rtsp://admin:password@192.168.1.100:554/stream1"
        
        Returns:
            GStreamer pipeline string
        """
        pipeline = (
            f"rtspsrc location={rtsp_url} latency=0 buffer-mode=0 ! "
            "rtph264depay ! "
            "h264parse ! "
            "avdec_h264 ! "  # Software H.264 decoder (CPU-only)
            "videoconvert ! "
            "video/x-raw,format=BGR ! "
            "appsink drop=1 sync=0 max-buffers=2"
        )
        
        return pipeline
    
    def read(self):
        """
        Read frame from camera (compatible with cv2.VideoCapture.read()).
        
        Returns:
            tuple: (success: bool, frame: numpy.ndarray or None)
                   - success: True if frame was successfully read
                   - frame: BGR image as numpy array (H, W, 3) or None
        """
        if self.cap is None or not self.cap.isOpened():
            return False, None
        
        return self.cap.read()
    
    def isOpened(self):
        """
        Check if camera is opened (compatible with cv2.VideoCapture.isOpened()).
        
        Returns:
            bool: True if camera is opened and ready
        """
        if self.cap is None:
            return False
        return self.cap.isOpened()
    
    def release(self):
        """
        Release camera resources (compatible with cv2.VideoCapture.release()).
        """
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.release()
        return False


# ============================================================================
# EXAMPLE GSTREAMER PIPELINE STRINGS
# ============================================================================

"""
USB WEBCAM EXAMPLES:
--------------------

1. Basic USB camera (640x480 @ 30fps):
   ksvideosrc device-index=0 ! 
   image/jpeg,width=640,height=480,framerate=30/1 ! 
   jpegdec ! 
   videoconvert ! 
   video/x-raw,format=BGR ! 
   appsink drop=1 sync=0 max-buffers=2

2. High resolution USB camera (1920x1080 @ 30fps):
   ksvideosrc device-index=0 ! 
   image/jpeg,width=1920,height=1080,framerate=30/1 ! 
   jpegdec ! 
   videoconvert ! 
   video/x-raw,format=BGR ! 
   appsink drop=1 sync=0 max-buffers=2

3. Lower FPS for CPU savings (640x480 @ 15fps):
   ksvideosrc device-index=0 ! 
   image/jpeg,width=640,height=480,framerate=15/1 ! 
   jpegdec ! 
   videoconvert ! 
   video/x-raw,format=BGR ! 
   appsink drop=1 sync=0 max-buffers=2


RTSP STREAM EXAMPLES:
---------------------

1. Basic RTSP stream (H.264, low latency):
   rtspsrc location=rtsp://admin:password@192.168.1.100:554/stream1 latency=0 buffer-mode=0 ! 
   rtph264depay ! 
   h264parse ! 
   avdec_h264 ! 
   videoconvert ! 
   video/x-raw,format=BGR ! 
   appsink drop=1 sync=0 max-buffers=2

2. RTSP with authentication:
   rtspsrc location=rtsp://username:password@192.168.1.100:554/live/stream1 latency=0 buffer-mode=0 ! 
   rtph264depay ! 
   h264parse ! 
   avdec_h264 ! 
   videoconvert ! 
   video/x-raw,format=BGR ! 
   appsink drop=1 sync=0 max-buffers=2

3. RTSP without authentication:
   rtspsrc location=rtsp://192.168.1.100:554/stream latency=0 buffer-mode=0 ! 
   rtph264depay ! 
   h264parse ! 
   avdec_h264 ! 
   videoconvert ! 
   video/x-raw,format=BGR ! 
   appsink drop=1 sync=0 max-buffers=2


PIPELINE COMPONENTS EXPLAINED:
-------------------------------

USB Pipeline:
- ksvideosrc: Windows Kernel Streaming video source (use v4l2src on Linux)
- device-index=N: USB camera index (0 = first camera)
- image/jpeg: Request JPEG-compressed frames from camera
- jpegdec: Decode JPEG to raw video
- videoconvert: Convert color space
- video/x-raw,format=BGR: Output in OpenCV-compatible BGR format
- appsink: Output sink for application (OpenCV)
  - drop=1: Drop old frames if processing is slow (prevent buffering)
  - sync=0: Don't sync to clock (lower latency)
  - max-buffers=2: Keep only 2 frames in buffer (minimal latency)

RTSP Pipeline:
- rtspsrc: RTSP network stream source
  - location: RTSP URL with credentials
  - latency=0: Minimal latency mode
  - buffer-mode=0: No buffering
- rtph264depay: Extract H.264 from RTP packets
- h264parse: Parse H.264 stream
- avdec_h264: Software H.264 decoder (CPU-only, no GPU)
- videoconvert: Convert to BGR
- appsink: Same as USB pipeline


PERFORMANCE TUNING:
-------------------

For LOWER CPU usage:
- Reduce resolution: width=320,height=240
- Reduce framerate: framerate=15/1 or framerate=10/1
- Increase max-buffers (but adds latency): max-buffers=5

For LOWER latency:
- Keep max-buffers=1 or max-buffers=2
- Use drop=1 on appsink
- Set latency=0 on rtspsrc
- Ensure sync=0 on appsink

For BETTER quality:
- Increase resolution: width=1920,height=1080
- Increase framerate: framerate=60/1 (if camera supports)
- Use drop=0 to keep all frames


TROUBLESHOOTING:
----------------

Issue: "Failed to open GStreamer pipeline"
Fix: Install GStreamer runtime for Windows
     Download from: https://gstreamer.freedesktop.org/download/

Issue: USB camera not detected
Fix: Try different device-index values (0, 1, 2)
     Or use: gst-device-monitor-1.0 Video to list cameras

Issue: RTSP connection failed
Fix: Verify RTSP URL, credentials, and network connectivity
     Test with: gst-launch-1.0 playbin uri=rtsp://...

Issue: High CPU usage
Fix: Reduce resolution and framerate in pipeline
     Example: width=320,height=240,framerate=15/1

Issue: Frame lag/buffering
Fix: Ensure drop=1 and max-buffers=2 in appsink
     Reduce network latency for RTSP streams
"""


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usb_camera():
    """Example: Use USB camera with GStreamer."""
    
    # Create camera instance
    camera = GStreamerCamera(source=0, pipeline_type='usb')
    
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            
            # Process frame with existing OpenCV code
            # (motion detection, AI pipeline, etc.)
            cv2.imshow("GStreamer USB Camera", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


def example_rtsp_stream():
    """Example: Use RTSP stream with GStreamer."""
    
    rtsp_url = "rtsp://admin:password@192.168.1.100:554/stream1"
    camera = GStreamerCamera(source=rtsp_url, pipeline_type='rtsp')
    
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            
            # Process frame with existing OpenCV code
            cv2.imshow("GStreamer RTSP Stream", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


def example_context_manager():
    """Example: Use with context manager (automatic cleanup)."""
    
    with GStreamerCamera(source=0, pipeline_type='usb') as camera:
        while camera.isOpened():
            ret, frame = camera.read()
            if not ret:
                break
            
            # Process frame
            cv2.imshow("Camera", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    # Test USB camera
    print("Testing GStreamer USB camera...")
    example_usb_camera()
