# ByteTrack Quick Reference - Copy-Paste Code

## 🎯 Essential Code Snippets

### Model Loading (Once at Startup)
```python
from ultralytics import YOLO

# Load model ONCE
yolo_model = YOLO("yolov8n.pt")

# Tracker config
TRACKER_CONFIG = "bytetrack.yaml"
TRACK_COLORS = {}  # Cache for persistent colors
```

---

### Inference with Tracking
```python
# In your frame processing loop:
results = yolo_model.track(
    source=frame,              # BGR numpy array
    conf=0.5,                  # Confidence threshold
    tracker="bytetrack.yaml",  # ByteTrack config
    persist=True,              # CRITICAL: Maintains state
    verbose=False              # No console spam
)
```

---

### Extract Tracking Data
```python
for result in results:
    boxes = result.boxes
    
    for box in boxes:
        # Bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Class and confidence
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = yolo_model.names[class_id]
        
        # TRACKING ID (may be None for first few frames)
        track_id = None
        if box.id is not None:
            track_id = int(box.id[0])
        
        # Use tracking data
        if track_id is not None:
            print(f"ID:{track_id} {class_name} {confidence:.2f}")
```

---

### Draw with Tracking IDs
```python
# Generate persistent color per tracking ID
if track_id is not None:
    if track_id not in TRACK_COLORS:
        np.random.seed(track_id)
        TRACK_COLORS[track_id] = tuple(map(int, np.random.randint(0, 255, 3)))
    color = TRACK_COLORS[track_id]
else:
    color = (0, 255, 0)  # Green if no ID yet

# Draw bounding box
cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

# Draw label
label = f"ID:{track_id} {class_name} {confidence:.2f}" if track_id else f"{class_name}"
cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
```

---

## bytetrack.yaml (Minimal)
```yaml
tracker_type: bytetrack

bytetrack:
  track_high_thresh: 0.5
  track_low_thresh: 0.1
  new_track_thresh: 0.6
  track_buffer: 30
  match_thresh: 0.8
  frame_rate: 30
```

---

## Common Issues - One-Line Fixes

### Tracking IDs always None:
```python
persist=True  # ← Add this to track() call
```

### IDs reset every frame:
```python
# Load model OUTSIDE callback/loop, not inside
```

### Too many ID switches:
```yaml
# In bytetrack.yaml:
match_thresh: 0.6  # Lower = more lenient (was 0.8)
```

### Tracks lost during occlusion:
```yaml
# In bytetrack.yaml:
track_buffer: 60  # Higher = longer memory (was 30)
```

---

## Test Your Integration

```python
# Quick test:
python core/gstreamer_yolo_bridge.py

# Look for console output:
# ✅ [TRACK] ID:1 | person (0.87) at [x,y,w,h]
# ✅ [TRACK] ID:1 | person (0.89) at [x,y,w,h]  ← SAME ID = WORKING
```

**If you see "ID:X" labels on video → ByteTrack is working! 🎉**
