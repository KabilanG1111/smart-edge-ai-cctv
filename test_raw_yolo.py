"""Quick diagnostic: what does YOLO actually see in the camera right now?"""
import cv2
from ultralytics import YOLO

model = YOLO("yolov8s.pt")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Grab a few frames to flush buffer
for _ in range(10):
    cap.grab()

ret, frame = cap.read()
cap.release()

if not ret:
    print("ERROR: Could not read camera")
    exit(1)

print(f"Frame: {frame.shape}")

# Raw YOLO predict (no tracking, no filtering)
results = model.predict(frame, conf=0.10, imgsz=640, verbose=False)

if results and len(results) > 0:
    boxes = results[0].boxes
    if boxes is not None and len(boxes) > 0:
        print(f"\n=== YOLO found {len(boxes)} objects ===")
        for box in boxes:
            cls_id = int(box.cls[0])
            cls_name = model.names[cls_id]
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].cpu().numpy()
            w = xyxy[2] - xyxy[0]
            h = xyxy[3] - xyxy[1]
            print(f"  {cls_name:15s}  conf={conf:.2f}  size={int(w)}x{int(h)}px")
    else:
        print("No detections at all!")
else:
    print("No results!")
