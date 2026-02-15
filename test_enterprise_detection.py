"""
Quick test for enterprise detection system
Shows which objects are detectable and tests accuracy
"""

import cv2
import time
from core.enterprise_pipeline import EnterprisePipeline

print("=" * 60)
print("  🏢 ENTERPRISE DETECTION TEST")
print("=" * 60)
print()

# Initialize pipeline
print("📥 Initializing enterprise pipeline...")
try:
    pipeline = EnterprisePipeline(
        yolo_model_path="models/openvino/yolov8s_fp16.xml",  # Will fallback to PyTorch if not found
        use_openvino=True,
        confidence_threshold=0.20,
        enable_stage2=False  # Start with Stage 1 only for speed
    )
    print("✅ Pipeline initialized")
except Exception as e:
    print(f"❌ Initialization failed: {e}")
    exit(1)

print()
print("📊 DETECTABLE OBJECTS (Stage 1 - YOLOv8):")
print("-" * 60)

# Dynamic classes that work with Stage 1
stage1_classes = {
    0: 'person',
    1: 'bicycle',
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck',
    26: 'handbag',
    27: 'tie',
    28: 'suitcase',
    32: 'sports ball',
    39: 'bottle',
    40: 'wine glass',
    41: 'cup',
    42: 'fork',
    43: 'knife',
    44: 'spoon',
    45: 'bowl',
    63: 'laptop',
    64: 'mouse',
    65: 'remote',
    66: 'keyboard',
    67: 'cell phone',
    73: 'book',
    77: 'scissors',
    84: 'toothbrush',
}

print("\n✅ WILL DETECT (25 dynamic objects):")
for class_id, name in sorted(stage1_classes.items(), key=lambda x: x[1]):
    print(f"   • {name}")

print("\n❌ WON'T DETECT (static objects filtered out):")
print("   • chair, couch, bed, table, tv, refrigerator")
print("   • potted plant, vase, sink, oven, toaster")
print("   • toilet, dining table")

print()
print("-" * 60)
print("🎥 Opening camera for live test...")
print()

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not accessible")
    exit(1)

print("✅ Camera opened")
print()
print("📹 LIVE DETECTION TEST:")
print("   Show these objects to camera:")
print("   ✓ Person (you)")
print("   ✓ Cell phone")
print("   ✓ Cup/Bottle")
print("   ✓ Book")
print("   ✓ Laptop")
print("   ✓ Keyboard/Mouse")
print()
print("   Press 'q' to quit")
print()

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break
    
    # Process frame
    try:
        annotated, detections, metrics = pipeline.process_frame(frame)
        
        # Show metrics every 30 frames
        frame_count += 1
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            avg_fps = frame_count / elapsed
            print(f"Frame {frame_count:4d} | FPS: {metrics.get('fps', 0):5.1f} | "
                  f"Detections: {len(detections):2d} | "
                  f"Tracks: {metrics.get('active_tracks', 0):2d}")
            
            # Show detected objects
            if detections:
                detected_classes = set()
                for det in detections:
                    detected_classes.add(det.class_name)
                    # Show high confidence detections
                    if det.confidence > 0.4:
                        locked = "🔒" if hasattr(det, 'track_id') and det.track_id in pipeline.track_memory and pipeline.track_memory[det.track_id].locked_class else ""
                        print(f"         {locked} {det.class_name}: {det.confidence:.2f}")
        
        # Display
        cv2.imshow('Enterprise Detection Test', annotated)
        
    except Exception as e:
        print(f"⚠️ Processing error: {e}")
        cv2.imshow('Enterprise Detection Test', frame)
    
    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print()
print("=" * 60)
print(f"✅ Test complete - {frame_count} frames processed")
print("=" * 60)
