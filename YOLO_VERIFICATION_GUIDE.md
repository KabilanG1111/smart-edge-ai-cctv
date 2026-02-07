# 🔍 YOLOv8 Verification Guide - Is YOLO Actually Running?

## ⚠️ **CRITICAL FINDING: You Have TWO Sources of Bounding Boxes**

### **Source 1: YOLOv8 Object Detection**
- **File**: [core/gstreamer_yolo_bridge.py](core/gstreamer_yolo_bridge.py)
- **Purpose**: Detect objects (person, phone, car, etc.)
- **Color**: Random colors per class (deterministic)
- **Thickness**: **5px** (THICK boxes)
- **Label**: `YOLO: person 0.87`

### **Source 2: Motion Detection (OpenCV)**
- **File**: [core/ai_pipeline.py](core/ai_pipeline.py) Line 95-96
- **Purpose**: Detect motion/movement
- **Color**: **RED (68, 0, 255)** for ROI, Cyan for normal
- **Thickness**: **2px** (THIN boxes)
- **Label**: `ROI-1` or `M1`

---

## 🎯 How to Verify YOLO is ACTUALLY Running

### **Method 1: Terminal Logs (Most Reliable)**

When you run `gstreamer_yolo_bridge.py`, you should see:

```bash
🔄 Loading YOLOv8n model...
Downloading yolov8n.pt...  # First time only
✅ YOLOv8n loaded successfully

# Then during inference:
[YOLO VERIFICATION] Frame 30 | Detections: 2
✅ [YOLO] Detected: person (0.91) at [145,210,340,580]
✅ [YOLO] Detected: cell phone (0.73) at [200,150,280,220]
[YOLO VERIFICATION] Frame 60 | Detections: 1
✅ [YOLO] Detected: person (0.88) at [150,215,345,585]
```

**What to look for:**
- ✅ Model loads at startup (only once)
- ✅ Detection logs show class names (person, phone, laptop, NOT "ROI-1")
- ✅ Confidence scores between 0.50-1.00
- ✅ Bounding box coordinates [x1, y1, x2, y2]

**If you DON'T see these logs:**
- ❌ YOLO is NOT running
- ❌ You're only seeing motion detection boxes

---

### **Method 2: Visual Inspection**

#### **YOLO Boxes:**
- **Thickness**: THICK (5px width)
- **Label**: `YOLO: person 0.87` (has "YOLO:" prefix)
- **Color**: Varies by class (person=one color, phone=another)
- **Detects**: Specific objects (person, phone, laptop, bottle)

#### **Motion Boxes:**
- **Thickness**: THIN (2px width)  
- **Label**: `ROI-1` or `M1` (NO class name, NO confidence)
- **Color**: RED for ROI motion, Cyan for normal motion
- **Detects**: Movement blobs (not object-specific)

#### **Side-by-Side Comparison:**

```
YOLO Box:                    Motion Box:
┌─────────────────────┐      ╔═══════════════╗
│ YOLO: person 0.91   │ vs   ║ ROI-1         ║
│                     │      ║               ║
│  THICK BORDER (5px) │      ║ THIN (2px)    ║
│  GREEN/BLUE/YELLOW  │      ║ RED/CYAN      ║
└─────────────────────┘      ╚═══════════════╝
```

---

### **Method 3: Code Inspection**

#### **✅ CORRECT: YOLO Running**
```python
# 1. Model loaded at startup (OUTSIDE callback)
yolo_model = YOLO("yolov8n.pt")  # ✅ Global scope

def on_new_sample(sink):
    # 2. Inference called inside callback
    results = yolo_model.predict(source=frame, conf=0.5, verbose=False)  # ✅
    
    # 3. Extracting detections
    for result in results:
        for box in result.boxes:
            class_name = yolo_model.names[int(box.cls[0])]  # ✅ Has class name
            confidence = float(box.conf[0])  # ✅ Has confidence
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # ✅ Has coordinates
```

#### **❌ WRONG: YOLO NOT Running (Common Mistakes)**

**Mistake 1: Model loaded but never called**
```python
yolo_model = YOLO("yolov8n.pt")  # Loaded...

def on_new_sample(sink):
    # ... but NEVER used
    cv2.rectangle(frame, ...)  # ❌ Drawing manually, not from YOLO
```

**Mistake 2: Model loaded inside callback (kills FPS)**
```python
def on_new_sample(sink):
    model = YOLO("yolov8n.pt")  # ❌ Loads EVERY FRAME (500ms delay)
    results = model.predict(frame)
```

**Mistake 3: Using motion detection instead**
```python
# This is motion detection, NOT YOLO:
contours, _ = cv2.findContours(thresh, ...)  # ❌ OpenCV motion
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(frame, (x, y), ...)  # ❌ Motion boxes, not YOLO
```

**Mistake 4: Calling YOLO but not drawing results**
```python
results = yolo_model.predict(frame)  # ✅ YOLO runs...
# ... but results are ignored ❌
cv2.imshow("frame", frame)  # Shows frame WITHOUT detections
```

---

## 🧪 Testing Procedure

### **Step 1: Run YOLO-enabled script**
```bash
cd F:\CCTV
.\venv\Scripts\Activate.ps1
python core\gstreamer_yolo_bridge.py
```

### **Step 2: Check terminal output**
```bash
# Expected output:
🔄 Loading YOLOv8n model...
✅ YOLOv8n loaded successfully

[YOLO VERIFICATION] Frame 30 | Detections: 2
✅ [YOLO] Detected: person (0.91) at [145,210,340,580]
✅ [YOLO] Detected: cell phone (0.73) at [200,150,280,220]
```

**If you see this**: ✅ YOLO is running  
**If you DON'T**: ❌ YOLO is not running

### **Step 3: Visual verification**
- **THICK boxes** with `YOLO: person 0.87` = YOLO running ✅
- **THIN RED boxes** with `ROI-1` = Motion detection only ❌

### **Step 4: Test with known objects**
Hold these objects in front of camera:
- **Cell phone** → Should detect `cell phone`
- **Laptop** → Should detect `laptop`
- **Bottle** → Should detect `bottle`
- **Person** → Should detect `person`

Motion detection will NOT know these are phones/laptops (just "movement").

---

## 📊 Performance Benchmarks (CPU-only)

### **Expected Performance (Intel i5, YOLOv8n):**
- **Model Load Time**: ~500ms (once at startup)
- **Inference Time**: 50-150ms per frame
- **FPS**: 8-20 FPS (depends on CPU)
- **Memory**: ~500MB

### **Performance-Safe Practices:**

#### **✅ DO:**
```python
# Load model ONCE
yolo_model = YOLO("yolov8n.pt")  # Global scope

# Use verbose=False
results = yolo_model.predict(frame, verbose=False)

# Drop old frames
appsink max-buffers=1 drop=true  # GStreamer config

# Release buffer early
buffer.unmap(map_info)  # Before inference
```

#### **❌ DON'T:**
```python
# Load model per frame
def callback():
    model = YOLO("yolov8n.pt")  # ❌ 500ms delay per frame

# Use verbose=True
results = model.predict(frame, verbose=True)  # ❌ Console spam

# Block on full buffer
appsink max-buffers=30  # ❌ Builds up latency

# Keep buffer mapped
results = model.predict(frame)
buffer.unmap(map_info)  # ❌ Too late
```

---

## 🔧 Troubleshooting

### **Problem: "I see red boxes but no YOLO logs"**
**Diagnosis**: Motion detection is running, YOLO is NOT.  
**Fix**: Check if `yolo_model.predict()` is called in callback.

### **Problem: "Terminal shows 'Detected: person' but boxes are THIN"**
**Diagnosis**: Another script is drawing motion boxes on top.  
**Fix**: Make sure you're running `gstreamer_yolo_bridge.py`, not `main.py` or `ai_pipeline.py`.

### **Problem: "Boxes appear but say 'ROI-1', not class names"**
**Diagnosis**: You're running motion detection script.  
**Fix**: Switch to YOLO script:
```bash
# Wrong script (motion detection):
python main.py  # ❌

# Correct script (YOLO):
python core/gstreamer_yolo_bridge.py  # ✅
```

### **Problem: "YOLO logs appear but FPS drops to 2-3"**
**Diagnosis**: Model loaded inside callback or verbose=True.  
**Fix**: 
```python
# Move this OUTSIDE callback:
yolo_model = YOLO("yolov8n.pt")

# Set verbose=False:
results = yolo_model.predict(frame, verbose=False)
```

### **Problem: "Detections are delayed by 2-3 seconds"**
**Diagnosis**: GStreamer buffer is full.  
**Fix**: Use `max-buffers=1 drop=true` in appsink config.

---

## 🎯 Quick Verification Checklist

Run this in your terminal:

```bash
cd F:\CCTV
.\venv\Scripts\Activate.ps1
python core\gstreamer_yolo_bridge.py

# Check for these indicators:
```

**✅ YOLO is Running IF you see:**
- [ ] `🔄 Loading YOLOv8n model...` at startup
- [ ] `✅ YOLOv8n loaded successfully`
- [ ] `[YOLO VERIFICATION] Frame 30 | Detections: X`
- [ ] `✅ [YOLO] Detected: person (0.87) at [x,y,w,h]`
- [ ] THICK boxes (5px) on video
- [ ] Labels with "YOLO:" prefix
- [ ] Class names (person, phone, laptop)
- [ ] Confidence scores (0.50-1.00)

**❌ YOLO is NOT Running IF you see:**
- [ ] No model loading message
- [ ] Only `ROI-1` or `M1` labels
- [ ] THIN boxes (2px)
- [ ] No confidence scores
- [ ] No class names

---

## 📝 Minimal YOLO Integration Snippet

If you need to add YOLO to a different callback:

```python
from ultralytics import YOLO
import cv2
import numpy as np

# STEP 1: Load model ONCE (global scope)
yolo_model = YOLO("yolov8n.pt")

def on_new_sample(sink):
    # ... extract frame as NumPy array ...
    
    # STEP 2: Run inference
    results = yolo_model.predict(
        source=frame,
        conf=0.5,  # Confidence threshold
        verbose=False  # No console spam
    )
    
    # STEP 3: Extract detections
    for result in results:
        for box in result.boxes:
            # Coordinates (x1, y1, x2, y2)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Class and confidence
            class_id = int(box.cls[0])
            class_name = yolo_model.names[class_id]
            confidence = float(box.conf[0])
            
            # STEP 4: Log detection
            print(f"Detected: {class_name} ({confidence:.2f})")
            
            # STEP 5: Draw on frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            label = f"{class_name} {confidence:.2f}"
            cv2.putText(frame, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # STEP 6: Display
    cv2.imshow("YOLO", frame)
    return Gst.FlowReturn.OK
```

---

## 🚨 Common "YOLO is Running" Misconceptions

### **Misconception 1: "I imported YOLO, so it must be running"**
**Reality**: Importing ≠ Executing. You must call `model.predict()`.

### **Misconception 2: "I see boxes, so YOLO must be working"**
**Reality**: Multiple sources can draw boxes (motion, ROI, YOLO). Check labels and thickness.

### **Misconception 3: "The model file exists, so inference is happening"**
**Reality**: Model file presence ≠ inference execution. Check logs.

### **Misconception 4: "FPS is slow, so YOLO must be running"**
**Reality**: Other issues can slow FPS (motion detection, poor GStreamer config).

---

## ✅ Final Verification Command

Run this exact command and watch terminal:

```bash
cd F:\CCTV
.\venv\Scripts\Activate.ps1
python core\gstreamer_yolo_bridge.py
```

**If YOLO is running**, you'll see:
```
🔄 Loading YOLOv8n model...
✅ YOLOv8n loaded successfully
[YOLO VERIFICATION] Frame 30 | Detections: 2
✅ [YOLO] Detected: person (0.91) at [145,210,340,580]
✅ [YOLO] Detected: cell phone (0.73) at [200,150,280,220]
```

**If YOLO is NOT running**, you'll see:
```
(Nothing, or only OpenCV/GStreamer logs)
```

---

## 🎬 Summary

**Your red boxes are from MOTION DETECTION ([ai_pipeline.py](core/ai_pipeline.py)), NOT YOLOv8.**

To see YOLOv8 detections:
1. Run `python core/gstreamer_yolo_bridge.py`
2. Check terminal for `✅ [YOLO] Detected: ...` logs
3. Look for THICK boxes (5px) with "YOLO:" prefix

**Two systems, two types of boxes:**
- **YOLO**: Object detection (person, phone) → THICK boxes, class names
- **Motion**: Movement detection (blobs) → THIN boxes, "ROI-1" labels
