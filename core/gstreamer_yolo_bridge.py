import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import numpy as np
import cv2
from ultralytics import YOLO

# Initialize GStreamer
Gst.init(None)

# ========================================
# STEP 1: Load YOLO Model ONCE at Startup
# ========================================
# WHY: Model loading is expensive (~500ms). Loading once prevents FPS drops.
# YOLOv8n is fastest variant (6.3M params) for real-time edge inference.
print("🔄 Loading YOLOv8n model with ByteTrack...")
yolo_model = YOLO("yolov8n.pt")  # Automatically downloads if not present
print("✅ YOLOv8n loaded successfully")

# Tracking settings
CONFIDENCE_THRESHOLD = 0.5  # Only show detections above 50% confidence
TRACKER_CONFIG = "bytetrack.yaml"  # ByteTrack configuration file
CLASS_COLORS = {}  # Cache colors for each class (consistent per class)
TRACK_COLORS = {}  # Cache colors for each tracking ID (persistent across frames)

# GStreamer pipeline
PIPELINE = (
    "ksvideosrc ! "
    "videoconvert ! "
    "video/x-raw,format=BGR ! "
    "appsink name=sink emit-signals=true max-buffers=1 drop=true"
)

pipeline = Gst.parse_launch(PIPELINE)
appsink = pipeline.get_by_name("sink")

def on_new_sample(sink):
    """
    GStreamer callback - executed for EVERY frame.
    CRITICAL: Keep this function fast to maintain real-time FPS.
    """
    # ========================================
    # STEP 2: Extract Frame from GStreamer
    # ========================================
    sample = sink.emit("pull-sample")
    buffer = sample.get_buffer()
    caps = sample.get_caps()

    width = caps.get_structure(0).get_value("width")
    height = caps.get_structure(0).get_value("height")

    success, map_info = buffer.map(Gst.MapFlags.READ)
    if not success:
        return Gst.FlowReturn.ERROR

    # Convert buffer to NumPy array (BGR format already from pipeline)
    frame = np.frombuffer(map_info.data, dtype=np.uint8)
    frame = frame.reshape((height, width, 3))
    
    # Unmap buffer ASAP (best practice - release GStreamer resources early)
    buffer.unmap(map_info)
    
    # ========================================
    # STEP 3: Run YOLOv8 Inference with ByteTrack Tracking
    # ========================================
    # WHY track() instead of predict(): Enables persistent object tracking across frames
    # WHY persist=True: Maintains tracker state between frames (CRITICAL for tracking)
    # WHY tracker=TRACKER_CONFIG: Uses ByteTrack algorithm with custom config
    # Returns: Results object with boxes, classes, confidences, AND tracking IDs
    results = yolo_model.track(
        source=frame,
        conf=CONFIDENCE_THRESHOLD,
        tracker=TRACKER_CONFIG,  # ByteTrack config
        persist=True,  # CRITICAL: Maintains tracking state across frames
        verbose=False  # Prevents console spam
    )
    
    # ========================================
    # VERIFICATION: Count detections BEFORE drawing
    # ========================================
    detection_count = 0
    for result in results:
        detection_count += len(result.boxes)
    
    # ⚠️ VERIFICATION LOG: Print every 30 frames (~1 sec at 30 FPS)
    global frame_counter
    if 'frame_counter' not in globals():
        frame_counter = 0
    frame_counter += 1
    
    if frame_counter % 30 == 0:
        print(f"[YOLO VERIFICATION] Frame {frame_counter} | Detections: {detection_count}")
    
    # ========================================
    # STEP 4: Draw Bounding Boxes with Tracking IDs
    # ========================================
    # WHY: Visualize detections with persistent tracking IDs
    # Access detection + tracking data from Results object
    for result in results:
        boxes = result.boxes  # Boxes object containing all detections
        
        for box in boxes:
            # Extract box coordinates (xyxy format = x1, y1, x2, y2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Convert to int for OpenCV
            
            # Extract class and confidence
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = yolo_model.names[class_id]  # Get class name from model
            
            # ========================================
            # EXTRACT TRACKING ID (ByteTrack)
            # ========================================
            # CRITICAL: Check if tracking ID exists (may be None for first few frames)
            track_id = None
            if box.id is not None:
                track_id = int(box.id[0])  # Extract tracking ID
            
            # ⚠️ VERIFICATION LOG: Print detections with tracking IDs
            if track_id is not None:
                print(f"✅ [TRACK] ID:{track_id} | {class_name} ({confidence:.2f}) at [{x1},{y1},{x2},{y2}]")
            else:
                print(f"⚠️ [YOLO] No ID yet | {class_name} ({confidence:.2f}) at [{x1},{y1},{x2},{y2}]")
            
            # ========================================
            # COLOR STRATEGY: Use tracking ID for consistent colors
            # ========================================
            # WHY: Same object keeps same color across frames (better UX)
            if track_id is not None:
                if track_id not in TRACK_COLORS:
                    # Generate deterministic color based on track_id
                    np.random.seed(track_id)
                    TRACK_COLORS[track_id] = tuple(map(int, np.random.randint(0, 255, 3)))
                color = TRACK_COLORS[track_id]
            else:
                # Fallback: Use class color if no tracking ID yet
                if class_id not in CLASS_COLORS:
                    np.random.seed(class_id)
                    CLASS_COLORS[class_id] = tuple(map(int, np.random.randint(0, 255, 3)))
                color = CLASS_COLORS[class_id]
            
            # ========================================
            # DRAW BOUNDING BOX
            # ========================================
            # Thickness=5 for YOLO detections (vs thickness=2 for motion/ROI)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 5)
            
            # ========================================
            # DRAW LABEL with TRACKING ID
            # ========================================
            # Format: "ID:123 person 0.95" (includes tracking ID)
            if track_id is not None:
                label = f"ID:{track_id} {class_name} {confidence:.2f}"
            else:
                label = f"YOLO: {class_name} {confidence:.2f}"
            
            # Calculate label background size
            (label_width, label_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            
            # Draw label background (filled rectangle)
            cv2.rectangle(
                frame,
                (x1, y1 - label_height - 10),
                (x1 + label_width, y1),
                color,
                -1  # Filled
            )
            
            # Draw label text (white text on colored background)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),  # White text
                1,
                cv2.LINE_AA
            )
    
    # ========================================
    # STEP 5: Display Annotated Frame
    # ========================================
    cv2.imshow("YOLOv8 GStreamer CCTV", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        pipeline.set_state(Gst.State.NULL)
        cv2.destroyAllWindows()

    return Gst.FlowReturn.OK  # CRITICAL: Must return OK for pipeline to continue

appsink.connect("new-sample", on_new_sample)

pipeline.set_state(Gst.State.PLAYING)

# Keep pipeline alive
import time
while True:
    time.sleep(1)
