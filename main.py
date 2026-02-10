import cv2
import time

MIN_MOTION_SECONDS = 0.5
COOLDOWN_SECONDS = 5
BANNER_DURATION = 3
BANNER_HEIGHT = 50

last_alert_time = 0

from core.video_stream import get_camera
from core.motion_detector import MotionDetector
from core.roi import inside_roi
from core.snapshot import save_snapshot
from core.alerts import alert_console, motion_beep, alert_siren
from utils.timer import get_time_string
from frame_processor import draw_status_text, draw_alert_text

cap = get_camera()
detector = MotionDetector()

motion_start = None
status = "IDLE"
snapshot_taken = False

motion_sound_played = False
alert_sound_played = False

banner_text = None
banner_color = None
banner_start_time = None

# ✅ CREATE RESIZABLE WINDOW
WINDOW_NAME = "AI CCTV System"
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

while True:
    # 🔴 EXIT IF WINDOW IS CLOSED (X button)
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    display = frame.copy()

    boxes, _ = detector.detect(frame)

    motion_detected = False
    roi_triggered = False

    for (x, y, w, h) in boxes:
        motion_detected = True
        # No bounding box rendering — silent detection

        if inside_roi(x, y, w, h):
            roi_triggered = True

    # ================= MOTION STATE =================

    if motion_detected:
        if motion_start is None:
            motion_start = current_time
            snapshot_taken = False
            status = "MOTION"

            if not motion_sound_played:
                motion_beep()
                motion_sound_played = True

            banner_text = "MOTION DETECTED"
            banner_color = (0, 255, 255)
            banner_start_time = current_time

        if not snapshot_taken and (current_time - motion_start) >= MIN_MOTION_SECONDS:
            save_snapshot(frame)
            snapshot_taken = True

    else:
        if motion_start is not None:
            duration = current_time - motion_start

            if roi_triggered and (current_time - last_alert_time) > COOLDOWN_SECONDS:
                last_alert_time = current_time
                status = "ALERT"

                if not alert_sound_played:
                    alert_siren()
                    alert_sound_played = True

                banner_text = "SUSPICIOUS ACTIVITY DETECTED"
                banner_color = (0, 0, 255)
                banner_start_time = current_time

                alert_console(duration)
            else:
                status = "IDLE"

        motion_start = None
        snapshot_taken = False
        motion_sound_played = False
        alert_sound_played = False

    # All visual overlays removed — clean raw feed
    # Timer, status text, alert text, and banners run silently

    cv2.imshow(WINDOW_NAME, display)

    # 🔴 EXIT IF 'q' or 'Q' PRESSED
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()
