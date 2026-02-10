import cv2
import sys

print("Testing camera access...")
cap = cv2.VideoCapture(0)
print(f"Camera opened: {cap.isOpened()}")

if cap.isOpened():
    ret, frame = cap.read()
    print(f"Frame read successful: {ret}")
    if ret:
        print(f"Frame shape: {frame.shape}")
        print("✅ Camera is working!")
    else:
        print("❌ Camera opened but cannot read frames")
        print("This could be:")
        print("  - Camera in use by another application")
        print("  - Camera driver issue")
        print("  - Permissions issue")
else:
    print("❌ Cannot open camera")
    print("Trying other camera indices...")
    for i in range(1, 5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Found camera at index {i}")
            ret, frame = cap.read()
            if ret:
                print(f"  ✅ Camera {i} works! Frame shape: {frame.shape}")
            cap.release()
            
cap.release()
