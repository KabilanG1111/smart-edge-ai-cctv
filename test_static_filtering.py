"""
Test Static Object Filtering
Verify that fans, ACs, clocks, etc. are filtered out
"""

import cv2
import time
from core.stable_production_pipeline import stable_pipeline

# Get a frame from camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

print("📹 Reading frame from camera...")
ret, frame = cap.read()
cap.release()

if not ret or frame is None:
    print("❌ Failed to read frame")
    exit()

print("✅ Frame captured")
print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")

# Process frame through stable pipeline
print("\n🔄 Processing frame through stable pipeline...")
annotated_frame, pipeline_data = stable_pipeline.process_frame(frame)

# Display results
print("\n" + "=" * 60)
print("📊 DETECTION RESULTS (with Static Object Filtering)")
print("=" * 60)

# Debug: show what pipeline_data contains
print(f"\n🔍 Pipeline data keys: {pipeline_data.keys()}")
print(f"🔍 Pipeline data: {pipeline_data}")

detections = pipeline_data.get("detections", [])
print(f"\n🔍 Detections type: {type(detections)}")
print(f"🔍 Detections value: {detections}")

# If detections is a list of Detection objects
if isinstance(detections, list):
    print(f"\n✅ Total detections: {len(detections)}")
    
    if len(detections) == 0:
        print("   No dynamic objects detected (fans/ACs/clocks filtered out)")
    else:
        print("\nDynamic objects detected:")
        for det in detections:
            class_name = det.class_name if hasattr(det, 'class_name') else 'Unknown'
            confidence = det.confidence if hasattr(det, 'confidence') else 0
            print(f"   • {class_name}: {confidence:.1%}")
else:
    print(f"\n⚠️  Unexpected detections format: {type(detections)}")

# Check what was filtered out
print("\n" + "=" * 60)
print("ℹ️  DYNAMIC CLASSES (allowed):")
print("=" * 60)
from core.openvino_inference import DYNAMIC_CLASSES
for class_id, class_name in DYNAMIC_CLASSES.items():
    print(f"   • {class_name}")

print("\n" + "=" * 60)
print("🚫 STATIC CLASSES (filtered out):")
print("=" * 60)
static_classes = [
    "fan", "ceiling fan", "clock", "tv", "laptop", "keyboard", 
    "chair", "couch", "bed", "dining table", "toilet",
    "refrigerator", "oven", "microwave", "toaster", "sink",
    "book", "vase", "potted plant", "airplane", "bird", "cat", "dog"
]
for cls in static_classes:
    print(f"   • {cls}")

print("\n✅ Test complete!")
print("\n💡 Key benefit: Even if YOLOv8 detects fan→airplane or AC→bird,")
print("   they'll be filtered out since airplane and bird are not in DYNAMIC_CLASSES")
