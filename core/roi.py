import cv2

def draw_roi(frame):
    """No-op: ROI analysis runs silently, no visual rendering"""
    pass

def inside_roi(x, y, w, h):
    # Option 1: Entire frame is ROI
    return True
