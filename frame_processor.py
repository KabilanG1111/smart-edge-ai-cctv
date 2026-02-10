import cv2

def process_frame(frame):
    # 1. Resize for speed
    frame = cv2.resize(frame, (640, 480))

    # 2. Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 3. Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    return frame, gray, blurred


def draw_status_text(frame, status):
    """No-op: status runs silently, no visual rendering"""
    return frame


def draw_alert_text(frame):
    """No-op: alerts run silently, no visual rendering"""
    return frame
