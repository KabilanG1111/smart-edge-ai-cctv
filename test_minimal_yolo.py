"""
STEP 8: Minimal Isolation Test - YOLO Detection Verification
This script tests YOLO detection in complete isolation (no FastAPI, no ByteTrack)
"""
import cv2
import numpy as np
from ultralytics import YOLO
import time

print("=" * 70)
print("MINIMAL YOLO DETECTION TEST")
print("=" * 70)

# STEP 1: Load Model
print("\n[STEP 1] Loading YOLO model...")
try:
    model = YOLO('yolov8n.pt')  # Using nano model for CPU
    print(f"✅ Model loaded: {model.model_name if hasattr(model, 'model_name') else 'yolov8n'}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    exit(1)

# STEP 3: Verify Classes
print("\n[STEP 3] Loaded classes:")
print(f"  Total classes: {len(model.names)}")
print(f"  Sample classes: {list(model.names.values())[:10]}")

# STEP 2: Open Camera
print("\n[STEP 2] Opening camera...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera failed to open")
    exit(1)
print("✅ Camera opened")

# Test Configuration​
CONF_THRESHOLD = 0.25  # STEP 6: Lower threshold for CPU
TEST_FRAMES = 50
detection_count = 0

print(f"\n[TEST] Processing {TEST_FRAMES} frames with conf={CONF_THRESHOLD}...")
print("Press 'q' to quit early\n")

for frame_num in range(TEST_FRAMES):
    ret, frame = cap.read()
    if not ret:
        print(f"❌ Failed to read frame {frame_num}")
        continue
    
    # STEP 2: Convert BGR → RGB (Critical for YOLO accuracy)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # STEP 1: Run Inference with Debug Logs
    start_time = time.time()
    results = model(frame_rgb, conf=CONF_THRESHOLD, verbose=False)
    inference_time = (time.time() - start_time) * 1000
    
    # Extract detections
    boxes = results[0].boxes
    num_detections = len(boxes)
    
    if num_detections > 0:
        detection_count += 1
        print(f"Frame {frame_num:3d}: {num_detections} detections | Inference: {inference_time:.1f}ms")
        
        # STEP 4: Draw Bounding Boxes
        for box in boxes:
            # Extract coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]
            
            # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            label_text = f"{label} {conf:.2f}"
            cv2.putText(
                frame, 
                label_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        # STEP 5: Display annotated frame
        cv2.imshow('YOLO Detection Test', frame)
    else:
        # Show frame even without detections
        cv2.putText(
            frame,
            "No detections",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )
        cv2.imshow('YOLO Detection Test', frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n⏹️ Test stopped by user")
        break

cap.release()
cv2.destroyAllWindows()

# Results
print("\n" + "=" * 70)
print("TEST RESULTS")
print("=" * 70)
print(f"Frames with detections: {detection_count}/{frame_num + 1}")
print(f"Detection rate: {(detection_count / (frame_num + 1)) * 100:.1f}%")

if detection_count == 0:
    print("\n❌ DIAGNOSIS: No detections found")
    print("Possible causes:")
    print("  1. Poor lighting conditions")
    print("  2. No objects in frame (try moving in front of camera)")
    print("  3. Confidence threshold too high (try 0.15)")
    print("  4. Camera returning corrupted frames")
    print("  5. Model incompatible with CPU")
elif detection_count < frame_num * 0.5:
    print("\n⚠️ DIAGNOSIS: Sporadic detections")
    print("Possible causes:")
    print("  1. Objects moving in/out of frame")
    print("  2. Lighting variations")
    print("  3. CPU inference too slow (frame drops)")
else:
    print("\n✅ DIAGNOSIS: Detection working correctly!")
    print("If bounding boxes still don't appear in your app:")
    print("  → The issue is in the integration layer (FastAPI/pipeline)")
    print("  → Check that annotated frames are being streamed (not raw frames)")

print("\n💡 Next steps:")
print("  1. If this test shows boxes → Integration issue")
print("  2. If this test shows NO boxes → Environment/model issue")
print("  3. Compare this code with your pipeline's drawing logic")
