import cv2
import os
import time

from config.settings import SNAPSHOT_DIR

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def save_snapshot(frame):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"motion_{timestamp}.jpg"
    path = os.path.join(SNAPSHOT_DIR, filename)
    cv2.imwrite(path, frame)
