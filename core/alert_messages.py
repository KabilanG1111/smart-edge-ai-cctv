# core/alert_messages.py

class AlertMessage:
    MOTION = {
        "text": "⚠ Motion detected",
        "color": (0, 255, 255)  # Yellow (BGR)
    }

    SUSPICIOUS = {
        "text": "⚠ Suspicious activity detected",
        "color": (0, 0, 255)    # Red (BGR)
    }
