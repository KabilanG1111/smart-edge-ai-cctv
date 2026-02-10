"""
Real-Time Object Detection Test
Show objects to the camera and see what the AI detects!
"""

import cv2
import time
from core.stable_production_pipeline import stable_pipeline

print("=" * 80)
print("📹 LIVE OBJECT DETECTION TEST")
print("=" * 80)
print("\n🎯 System configured for 68 object classes")
print("🚫 Filtering: chair, couch, bed, table, refrigerator, oven, sink, vase, etc.")
print("\n✅ Ready to detect:")
print("   • Electronics: laptop, keyboard, mouse, cell phone, remote")
print("   • Kitchen: bottle, cup, fork, knife, spoon, bowl")
print("   • Office: book, clock, scissors")
print("   • Animals: cat, dog, bird")
print("   • And 50+ more objects!")
print("\n" + "=" * 80)

# Open camera
print("\n📹 Opening camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    print("💡 Make sure no other program is using the camera")
    exit()

print("✅ Camera opened successfully")
print("\n" + "=" * 80)
print("🔴 LIVE DETECTION - Press Ctrl+C to stop")
print("=" * 80)
print("\nShow objects to the camera!")
print("I'll tell you what I detect...\n")

frame_count = 0
last_detections = []

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️  Failed to read frame, retrying...")
            time.sleep(0.1)
            continue
        
        frame_count += 1
        
        # Process every 10 frames (to reduce spam)
        if frame_count % 10 == 0:
            start_time = time.time()
            
            # Run detection through stable pipeline
            annotated_frame, pipeline_data = stable_pipeline.process_frame(frame)
            
            # Get current detections
            tracked_objects = pipeline_data.get("tracked_objects", 0)
            fps = pipeline_data.get("fps", 0)
            active_tracks = pipeline_data.get("active_tracks", 0)
            
            # Extract detection details from detection_feed
            current_detections = []
            
            # Get recent detections from the feed
            recent_feed = list(stable_pipeline.detection_feed)[-10:]  # Last 10 detections
            
            # Group by class name to avoid duplicates
            detected_classes = {}
            for item in recent_feed:
                class_name = item.get('class', 'unknown')
                confidence = item.get('confidence', 0)
                if class_name not in detected_classes or confidence > detected_classes[class_name]:
                    detected_classes[class_name] = confidence
            
            # Convert to list
            current_detections = [
                {'class': name, 'confidence': conf}
                for name, conf in detected_classes.items()
            ]
            
            # Display if detections changed
            detection_key = str(sorted([d['class'] for d in current_detections]))
            last_key = str(sorted([d['class'] for d in last_detections]))
            
            if detection_key != last_key or frame_count % 50 == 0:  # Update every 50 frames minimum
                print(f"\n{'─' * 80}")
                print(f"Frame {frame_count} | FPS: {fps:.1f} | Active Tracks: {active_tracks}")
                print(f"{'─' * 80}")
                
                if len(current_detections) == 0:
                    print("   No objects detected")
                    print("   💡 Try showing: laptop, phone, book, bottle, cup, scissors...")
                else:
                    print("   Detected objects:")
                    for det in current_detections:
                        # Add emoji based on object type
                        emoji = {
                            'person': '👤',
                            'laptop': '💻',
                            'cell phone': '📱',
                            'book': '📚',
                            'bottle': '🍾',
                            'cup': '☕',
                            'scissors': '✂️',
                            'knife': '🔪',
                            'fork': '🍴',
                            'spoon': '🥄',
                            'cat': '🐱',
                            'dog': '🐶',
                            'bird': '🐦',
                            'clock': '⏰',
                            'keyboard': '⌨️',
                            'mouse': '🖱️',
                            'remote': '📺',
                            'backpack': '🎒',
                            'handbag': '👜',
                            'umbrella': '☂️'
                        }.get(det['class'], '📦')
                        
                        print(f"     {emoji} {det['class'].upper()}: {det['confidence']}%")
                
                last_detections = current_detections
        
        # Small delay
        time.sleep(0.033)  # ~30 FPS

except KeyboardInterrupt:
    print("\n\n" + "=" * 80)
    print("🛑 Detection stopped by user")
    print("=" * 80)
    print(f"\n📊 Session stats:")
    print(f"   Total frames processed: {frame_count}")
    print(f"   Detection changes: {len(set([str(d) for d in last_detections]))}")
    print("\n✅ Test complete!")

finally:
    cap.release()
    print("\n📹 Camera released")
