import cv2
from config.settings import MIN_CONTOUR_AREA

class MotionDetector:
    def __init__(self):
        self.prev_gray = None
        self.prev_shape = None

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # 🔴 FIX: reset background if frame size changes
        if self.prev_gray is None or gray.shape != self.prev_shape:
            self.prev_gray = gray
            self.prev_shape = gray.shape
            return [], None

        delta = cv2.absdiff(self.prev_gray, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        boxes = []
        for c in contours:
            if cv2.contourArea(c) < MIN_CONTOUR_AREA:
                continue
            boxes.append(cv2.boundingRect(c))

        self.prev_gray = gray
        self.prev_shape = gray.shape
        return boxes, thresh
