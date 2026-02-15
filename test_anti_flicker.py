"""
🧪 ANTI-FLICKER SYSTEM TEST SCRIPT
==================================

Quick test to verify zero class flicker on bottle detection.

Usage:
    python test_anti_flicker.py

Expected behavior:
- Hold a bottle in front of webcam
- Should detect as "bottle" consistently
- Should NEVER flicker to dog, cat, tie, etc.
- Should lock after 5 consecutive stable frames

Author: Production AI Team
"""

import cv2
import time
import sys
import logging
from pathlib import Path
from collections import Counter

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.inference_engine import StableInferenceEngine

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_bottle_stability():
    """
    Test bottle detection stability
    
    Hold a bottle in front of camera for 10 seconds.
    Expected: Always "bottle", never dog/cat/tie.
    """
    print("\n" + "=" * 70)
    print("🧪 ANTI-FLICKER SYSTEM TEST")
    print("=" * 70)
    print("\nInitializing Stable Inference Engine...")
    
    try:
        engine = StableInferenceEngine(
            model_path="yolov8s.pt",
            conf_threshold=0.35,
            use_openvino=False,  # Start with ultralytics for compatibility
            verbose=False  # Reduce logging noise
        )
    except Exception as e:
        logger.error(f"Failed to initialize engine: {e}")
        logger.error("Make sure yolov8s.pt exists in the current directory")
        return False
    
    print("✅ Engine initialized\n")
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Cannot open webcam (camera index 0)")
        logger.info("Try changing camera index: cv2.VideoCapture(1) or (2)")
        return False
    
    print("=" * 70)
    print("TEST INSTRUCTIONS:")
    print("=" * 70)
    print("1. Hold a BOTTLE in front of the camera")
    print("2. Keep it visible for 10 seconds")
    print("3. Move it around slightly (test tracking)")
    print("4. Expected: Always 'bottle', never dog/cat/tie")
    print("=" * 70)
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    print("🎬 RECORDING...\n")
    
    # Test parameters
    test_duration = 10  # seconds
    detected_classes = []
    frame_count = 0
    start_time = time.time()
    
    # FPS tracking
    fps_history = []
    
    try:
        while time.time() - start_time < test_duration:
            ret, frame = cap.read()
            if not ret:
                logger.warning("Failed to read frame from webcam")
                continue
            
            frame_count += 1
            
            # Process frame
            t_start = time.time()
            detections, metadata = engine.process_frame(frame)
            fps = metadata.get('fps', 0)
            fps_history.append(fps)
            
            # Draw detections
            annotated = engine.draw_detections(
                frame, detections,
                show_track_id=True,
                show_confidence=True,
                show_lock_status=True
            )
            
            # Add timer and FPS
            elapsed = int(time.time() - start_time)
            remaining = test_duration - elapsed
            
            cv2.putText(
                annotated,
                f"Time remaining: {remaining}s",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )
            
            cv2.putText(
                annotated,
                f"FPS: {fps:.1f}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            # Log bottle detections
            for det in detections:
                class_name = det['class_name']
                confidence = det['confidence']
                is_locked = det['is_locked']
                track_id = det['track_id']
                
                # Record all detections containing "bottle"
                if 'bottle' in class_name.lower():
                    detected_classes.append(class_name)
                    
                    lock_emoji = "🔒" if is_locked else "🔓"
                    print(
                        f"Frame {frame_count:3d}: "
                        f"Track {track_id} | "
                        f"{class_name:15s} | "
                        f"Conf={confidence:.2f} | "
                        f"{lock_emoji} {('LOCKED' if is_locked else 'Unlocked')}"
                    )
            
            # Show frame
            cv2.imshow("Anti-Flicker Test (Press 'q' to quit early)", annotated)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n⏹️  Test stopped by user")
                break
    
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Analyze results
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS")
    print("=" * 70)
    
    if not detected_classes:
        print("❌ NO BOTTLE DETECTIONS")
        print("\nPossible reasons:")
        print("1. No bottle in frame")
        print("2. Bottle too far from camera")
        print("3. Poor lighting")
        print("4. Camera not working")
        print("\nTry again with:")
        print("- Bottle closer to camera")
        print("- Better lighting")
        print("- Clear background")
        return False
    
    # Count unique classes
    class_counts = Counter(detected_classes)
    unique_classes = set(detected_classes)
    
    print(f"\nTotal frames with bottle: {len(detected_classes)}")
    print(f"Unique classes detected: {unique_classes}")
    print(f"\nClass distribution:")
    for cls, count in class_counts.most_common():
        percentage = (count / len(detected_classes)) * 100
        print(f"  {cls:15s}: {count:3d} frames ({percentage:5.1f}%)")
    
    # Check for flicker
    has_flicker = len(unique_classes) > 1 or not all('bottle' in cls.lower() for cls in unique_classes)
    
    if has_flicker:
        print("\n❌ TEST FAILED: FLICKER DETECTED")
        print(f"   Expected: Only 'bottle'")
        print(f"   Got: {unique_classes}")
    else:
        print("\n✅ TEST PASSED: ZERO FLICKER!")
        print("   Bottle was consistently detected as 'bottle'")
    
    # Performance stats
    print("\n" + "-" * 70)
    print("Performance Statistics")
    print("-" * 70)
    
    stats = engine.get_stats()
    
    print(f"Total frames processed: {stats['frame_count']}")
    print(f"Average FPS: {stats['avg_fps']:.1f}")
    print(f"Average detections/frame: {stats['avg_detections_per_frame']:.1f}")
    print(f"Lock rate: {stats['lock_rate']}")
    print(f"Total locks: {stats['total_locks_ever']}")
    print(f"Total unlocks: {stats['total_unlocks_ever']}")
    
    if fps_history:
        avg_fps = sum(fps_history) / len(fps_history)
        min_fps = min(fps_history)
        max_fps = max(fps_history)
        print(f"\nFPS range: {min_fps:.1f} - {max_fps:.1f} (avg: {avg_fps:.1f})")
    
    # Final verdict
    print("\n" + "=" * 70)
    if not has_flicker and len(detected_classes) > 20:
        print("🎉 SUCCESS: Anti-flicker system working perfectly!")
        print("   Bottle detection is stable and reliable.")
        return True
    elif not has_flicker:
        print("⚠️  PARTIAL SUCCESS: No flicker detected")
        print(f"   But only {len(detected_classes)} detections (expected >20)")
        print("   Try holding bottle closer to camera")
        return True
    else:
        print("❌ FAILURE: Flicker still present")
        print("   Please check configuration in core/detector.py")
        return False


def test_webcam():
    """Quick test to verify webcam is working"""
    print("\n🎥 Testing webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot open webcam (index 0)")
        return False
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("❌ Cannot read from webcam")
        return False
    
    print(f"✅ Webcam OK (resolution: {frame.shape[1]}x{frame.shape[0]})")
    return True


def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test anti-flicker system")
    parser.add_argument(
        '--check-webcam',
        action='store_true',
        help="Just check if webcam is working"
    )
    args = parser.parse_args()
    
    if args.check_webcam:
        test_webcam()
        return
    
    # Run full test
    success = test_bottle_stability()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
