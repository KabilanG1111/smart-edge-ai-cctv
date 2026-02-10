import cv2
import time

print("Testing camera with OpenCV...")

# Try to open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Could not open camera!")
    print("Possible reasons:")
    print("  - No camera connected")
    print("  - Camera already in use by another program")
    print("  - Permission denied")
    exit(1)

print("✅ Camera opened successfully!")

# Try to read a few frames
for i in range(5):
    ret, frame = cap.read()
    if ret:
        print(f"✅ Frame {i+1}: {frame.shape} - OK")
    else:
        print(f"❌ Frame {i+1}: Failed to read")
    time.sleep(0.1)

cap.release()
print("\n✅ Camera test complete!")
