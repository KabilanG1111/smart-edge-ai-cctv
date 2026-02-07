import cv2

def draw_roi(frame):
    """Draw thin neon ROI outline - 2050 surveillance style"""
    h, w = frame.shape[:2]
    # Thin cyan border with subtle glow
    cv2.rectangle(frame, (2, 2), (w - 3, h - 3), (150, 100, 50), 2, cv2.LINE_AA)  # Glow layer
    cv2.rectangle(frame, (2, 2), (w - 3, h - 3), (255, 150, 0), 1, cv2.LINE_AA)   # Main cyan line

def inside_roi(x, y, w, h):
    # Option 1: Entire frame is ROI
    return True
