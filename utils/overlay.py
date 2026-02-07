# ui/overlay.py

import cv2

def draw_alert_message(frame, message, position=(10, 30)):
    """
    Draw alert message on frame.
    message: dict with 'text' and 'color'
    """
    cv2.putText(
        frame,
        message["text"],
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        message["color"],
        2
    )
