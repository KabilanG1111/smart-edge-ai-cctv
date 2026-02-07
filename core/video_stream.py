import cv2
from config.settings import CAMERA_INDEX

_cap = None  # 🔒 shared camera instance

def get_camera():
    global _cap
    if _cap is None:
        _cap = cv2.VideoCapture(CAMERA_INDEX)
        if not _cap.isOpened():
            raise RuntimeError("Camera not accessible")
    return _cap
