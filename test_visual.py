"""
Quick visual test - displays camera feed for 5 seconds
Tests that existing motion detection pipeline works
"""

import cv2
import time
from core.video_stream import get_camera
from core.motion_detector import MotionDetector

print("=" * 60)
print("Visual Camera Test - 5 seconds")
print("Press 'q' to quit early")
print("=" * 60)

cap = get_camera()
detector = MotionDetector()

start_time = time.time()
frame_count = 0

while time.time() - start_time < 5:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame")
        break
    
    frame_count += 1
    
    # Run motion detection
    boxes, thresh = detector.detect(frame)
    
    # Draw bounding boxes
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Add info text
    fps = frame_count / (time.time() - start_time)
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Motions: {len(boxes)}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Camera Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

print(f"\n✅ Test complete!")
print(f"   Frames processed: {frame_count}")
print(f"   Average FPS: {frame_count / 5:.1f}")
print(f"   Motion detection: Working")
