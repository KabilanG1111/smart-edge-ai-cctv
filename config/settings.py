import numpy as np

# ============================================================================
# CAMERA CONFIGURATION
# ============================================================================

# Choose camera backend: False = OpenCV VideoCapture, True = GStreamer
USE_GSTREAMER = False

# OpenCV VideoCapture settings (when USE_GSTREAMER = False)
CAMERA_INDEX = 0  # USB camera index: 0, 1, 2, etc.

# GStreamer settings (when USE_GSTREAMER = True)
GSTREAMER_TYPE = 'usb'  # Options: 'usb' or 'rtsp'

# GStreamer source (depends on GSTREAMER_TYPE)
# For USB: camera index as integer (0, 1, 2, etc.)
# For RTSP: full RTSP URL as string
# Examples:
#   USB: GSTREAMER_SOURCE = 0
#   RTSP: GSTREAMER_SOURCE = "rtsp://admin:password@192.168.1.100:554/stream1"
GSTREAMER_SOURCE = 0

# ============================================================================
# MOTION DETECTION
# ============================================================================

# Motion
MIN_CONTOUR_AREA = 1500

# ROI (bottom-right quadrant, relative coords)
ROI_TOP_LEFT = (50, 50)
ROI_BOTTOM_RIGHT = (300, 300)

# Snapshot folder
SNAPSHOT_DIR = "snapshots"
