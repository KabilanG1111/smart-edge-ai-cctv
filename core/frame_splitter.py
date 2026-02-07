import cv2
import numpy as np


def split_four(original, gray, roi_view, motion_mask):
    h, w = original.shape[:2]

    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    motion_bgr = cv2.cvtColor(motion_mask, cv2.COLOR_GRAY2BGR)

    top = np.hstack((original, gray_bgr))
    bottom = np.hstack((roi_view, motion_bgr))

    return np.vstack((top, bottom))


def frame_splitter(frame):
    """Split `frame` into four quadrants and return a dict with keys:
    'top_left', 'top_right', 'bottom_left', 'bottom_right'.

    This matches the structure expected by `main.py`.
    """
    h, w = frame.shape[:2]
    h2 = h // 2
    w2 = w // 2

    top_left = frame[0:h2, 0:w2]
    top_right = frame[0:h2, w2:w]
    bottom_left = frame[h2:h, 0:w2]
    bottom_right = frame[h2:h, w2:w]

    return {
        "top_left": top_left,
        "top_right": top_right,
        "bottom_left": bottom_left,
        "bottom_right": bottom_right
    }
