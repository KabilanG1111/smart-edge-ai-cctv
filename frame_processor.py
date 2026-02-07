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
    if status == "IDLE":
        color = (0, 255, 0)
        text = "STATUS: IDLE"
    elif status == "MOTION":
        color = (0, 255, 255)
        text = "STATUS: MOTION"
    elif status == "ALERT":
        color = (0, 0, 255)
        text = "⚠ STATUS: ALERT"
    else:
        return frame

    cv2.putText(
        frame,
        text,
        (10, frame.shape[0] - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )
    return frame


def draw_alert_text(frame):
    cv2.putText(
        frame,
        "⚠ ALERT",
        (frame.shape[1] // 2 - 60, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )
    return frame
