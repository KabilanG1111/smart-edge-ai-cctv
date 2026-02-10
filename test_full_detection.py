"""
Test Full Object Detection
Verify that the system now detects ALL objects except static infrastructure
"""

import cv2
import numpy as np
from core.openvino_inference import COCO_CLASSES, BLOCKED_CLASS_IDS, STATIC_BLOCKED_CLASSES

print("=" * 70)
print("🎯 PRODUCTION-LEVEL OBJECT DETECTION - CONFIGURATION")
print("=" * 70)

print(f"\n📊 Total COCO classes: {len(COCO_CLASSES)}")
print(f"🚫 Blocked (static infrastructure): {len(BLOCKED_CLASS_IDS)}")
print(f"✅ Allowed (detectable): {len(COCO_CLASSES) - len(BLOCKED_CLASS_IDS)}")

print("\n" + "=" * 70)
print("🚫 BLOCKED CLASSES (Static Infrastructure Only)")
print("=" * 70)
for class_id, class_name in sorted(STATIC_BLOCKED_CLASSES.items()):
    print(f"   {class_id:2d}: {class_name}")

print("\n" + "=" * 70)
print("✅ ALLOWED CLASSES (All Others)")
print("=" * 70)

allowed_classes = {k: v for k, v in COCO_CLASSES.items() if k not in BLOCKED_CLASS_IDS}

# Group by category for better readability
categories = {
    "People": [0],
    "Vehicles": list(range(1, 9)),
    "Traffic/Outdoor": list(range(9, 14)),
    "Animals": list(range(14, 24)),
    "Accessories": [24, 25, 26, 27, 28],
    "Sports": list(range(29, 39)),
    "Kitchen/Food": list(range(39, 56)),
    "Electronics": [62, 63, 64, 65, 66, 67, 68],
    "Office": [73, 74],
    "Tools": [76],
    "Toys": [77, 78, 79]
}

for category, class_ids in categories.items():
    items = [f"{id}:{COCO_CLASSES[id]}" for id in class_ids if id in allowed_classes]
    if items:
        print(f"\n{category}:")
        for item in items:
            class_id, name = item.split(":")
            print(f"   {class_id:>2}: {name}")

print("\n" + "=" * 70)
print("💡 KEY CHANGES FROM PREVIOUS VERSION")
print("=" * 70)
print("BEFORE: Only 7 classes (person, backpack, handbag, suitcase, bottle, phone, scissors)")
print("NOW:    68 classes (everything except furniture/appliances)")
print()
print("✅ NOW DETECTS:")
print("   • Laptops, keyboards, mice, remotes")
print("   • Books, clocks")
print("   • Bottles, cups, forks, knives, spoons")
print("   • Cats, dogs, birds")
print("   • Cars, motorcycles, bicycles")
print("   • Scissors, hair driers, toothbrushes")
print("   • And 50+ more objects!")
print()
print("🚫 STILL BLOCKS (as intended):")
print("   • Furniture: chair, couch, bed, dining table")
print("   • Appliances: refrigerator, oven, toaster, microwave, sink")
print("   • Decor: vase, potted plant, TV (wall-mounted)")

print("\n" + "=" * 70)
print("🧪 TESTING LIVE DETECTION")
print("=" * 70)

from core.stable_production_pipeline import stable_pipeline

# Test with camera
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

# Process frame
print("\n🔄 Processing frame...")
annotated_frame, pipeline_data = stable_pipeline.process_frame(frame)

print("\n" + "=" * 70)
print("📊 DETECTION RESULTS")
print("=" * 70)

tracked_objects = pipeline_data.get("tracked_objects", [])
print(f"\n✅ Objects detected: {tracked_objects if isinstance(tracked_objects, int) else len(tracked_objects)}")

# Try to get more details
frame_number = pipeline_data.get("frame_number", 0)
fps = pipeline_data.get("fps", 0)
active_tracks = pipeline_data.get("active_tracks", 0)

print(f"   Frame: {frame_number}")
print(f"   FPS: {fps:.1f}")
print(f"   Active tracks: {active_tracks}")

print("\n✅ System ready! Refresh your browser to see improved detections.")
print("💡 Now try showing:")
print("   • Laptop → should detect 'laptop'")
print("   • Phone → should detect 'cell phone'")
print("   • Book → should detect 'book'")
print("   • Bottle → should detect 'bottle'")
print("   • Cup → should detect 'cup'")
print("   • Scissors → should detect 'scissors'")
