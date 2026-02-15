"""
Test what objects YOUR CURRENT SYSTEM can detect
Uses the working stable_production_pipeline.py
"""

import cv2
import time
from core.stable_production_pipeline import stable_pipeline

print("=" * 70)
print("  🎥 YOUR CURRENT SYSTEM - DETECTION TEST")
print("=" * 70)
print()

# Show what's filtered OUT (won't detect)
print("❌ FILTERED OUT (Static objects - WON'T DETECT):")
print("-" * 70)
BLOCKED = {
    56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed',
    60: 'dining table', 61: 'toilet', 62: 'tv', 69: 'oven',
    70: 'toaster', 71: 'sink', 72: 'refrigerator', 75: 'vase'
}
for class_id, name in sorted(BLOCKED.items(), key=lambda x: x[1]):
    print(f"   • {name.upper()}")

print()
print("✅ WILL DETECT (68 other objects including):")
print("-" * 70)
COMMON_DETECTABLE = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
    'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
    'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'book', 'clock', 'scissors', 'teddy bear', 'hair drier'
]

for i, name in enumerate(COMMON_DETECTABLE, 1):
    print(f"   • {name}", end="")
    if i % 4 == 0:
        print()
    else:
        print("\t", end="")
print("\n")

print("=" * 70)
print("🎯 TESTING WITH YOUR CAMERA:")
print("=" * 70)
print()
print("   Show these HIGH-CONFIDENCE objects:")
print("   ✓ PERSON (yourself)")
print("   ✓ CELL PHONE")
print("   ✓ BOOK")
print("   ✓ CUP or BOTTLE")
print("   ✓ LAPTOP")
print("   ✓ BACKPACK or HANDBAG")
print()
print("   DON'T show these (they're filtered):")
print("   ✗ Chair, Table, TV, Refrigerator")
print("   ✗ Couch, Bed, Vase, Plant")
print()
print("   Press 'q' to quit")
print()

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not accessible")
    exit(1)

print("✅ Camera opened - processing frames...")
print()

frame_count = 0
start_time = time.time()
last_detections = []

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process with working pipeline
        result = stable_pipeline.process_frame(frame)
        
        if result:
            annotated = result['annotated_frame']
            detections = result.get('detections', [])
            
            frame_count += 1
            
            # Show status every 30 frames
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                fps = frame_count / elapsed
                print(f"Frame {frame_count:4d} | FPS: {fps:5.1f} | Detections: {len(detections):2d}")
                
                # Show what's detected
                if detections:
                    detected = {}
                    for det in detections:
                        class_name = det.get('class', 'unknown')
                        conf = det.get('confidence', 0)
                        if conf > 0.35:  # High confidence only
                            if class_name not in detected or conf > detected[class_name]:
                                detected[class_name] = conf
                    
                    if detected:
                        print("   Currently seeing:")
                        for name, conf in sorted(detected.items(), key=lambda x: -x[1]):
                            print(f"      • {name}: {conf:.1%}")
                        print()
                else:
                    if last_detections:
                        print("   (No current detections)")
                        print()
                
                last_detections = detections
            
            cv2.imshow('Your Current System Test', annotated)
        else:
            cv2.imshow('Your Current System Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nStopped by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    print()
    print("=" * 70)
    print(f"✅ Test complete - {frame_count} frames processed")
    print("=" * 70)
