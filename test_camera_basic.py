"""
Quick test to verify camera access and basic functionality
Tests with standard OpenCV (no GStreamer required)
"""

import cv2
import sys

print("=" * 60)
print("Testing Camera Access with OpenCV")
print("=" * 60)

# Test if OpenCV can access camera
print("\n1. Opening camera with cv2.VideoCapture(0)...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Cannot open camera")
    print("   - Check if camera is connected")
    print("   - Check if another app is using the camera")
    sys.exit(1)

print("✅ Camera opened successfully")

# Read a few frames
print("\n2. Reading test frames...")
for i in range(5):
    ret, frame = cap.read()
    if not ret:
        print(f"❌ Failed to read frame {i+1}")
        cap.release()
        sys.exit(1)
    print(f"✅ Frame {i+1}: {frame.shape[1]}x{frame.shape[0]}, dtype={frame.dtype}")

cap.release()

print("\n3. Testing motion detector import...")
try:
    from core.motion_detector import MotionDetector
    detector = MotionDetector()
    print("✅ MotionDetector imported successfully")
except Exception as e:
    print(f"❌ Failed to import MotionDetector: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - Camera and OpenCV working!")
print("=" * 60)
print("\nNext steps:")
print("1. Install GStreamer (optional, for lower latency)")
print("   Download from: https://gstreamer.freedesktop.org/download/")
print("2. Run: python test_gstreamer_integration.py")
