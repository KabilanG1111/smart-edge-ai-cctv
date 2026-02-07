# Smart Edge-AI CCTV System - AI Pipeline Integration Guide

## 🎯 What Was Changed

### Problem Statement
The original system streamed **raw camera feed** to the frontend. The AI modules (motion detection, ROI validation, alerts) existed but were **NOT integrated into the video stream**. Users saw a plain camera feed with no visual intelligence.

### Solution Architecture
Refactored backend to implement a **unified AI processing pipeline** that processes every frame before streaming:

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI PROCESSING FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Camera Capture → AI Pipeline → Overlays → Encode → Stream     │
│                                                                 │
│  1. cv2.VideoCapture()                                         │
│  2. AIProcessingPipeline.process_frame()                       │
│     ├─ Motion Detection (MotionDetector)                       │
│     ├─ ROI Validation (inside_roi)                             │
│     ├─ Context Classification (IDLE/MOTION/ALERT)              │
│     └─ Visual Overlays (boxes, labels, status)                 │
│  3. cv2.imencode() - encoded processed frame                   │
│  4. StreamingResponse - multipart/x-mixed-replace              │
│  5. Frontend <img> - displays AI-processed video               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Files Created/Modified

### ✅ Created: `core/ai_pipeline.py`
**Purpose**: Unified AI processing pipeline that integrates all AI modules

**Key Components**:
- `AIProcessingPipeline` class: Main processing engine
- `process_frame()`: Core method that applies AI to each frame
- State machine: Tracks IDLE → MOTION → ALERT transitions
- Visual overlay system: Draws bounding boxes, labels, confidence scores

**AI Features Integrated**:
1. **Motion Detection**: Uses existing `MotionDetector` class
2. **ROI Validation**: Checks if detected motion is in Region of Interest
3. **Context Classification**: Determines current state (IDLE/MOTION/ALERT)
4. **Confidence Scoring**: Calculates detection confidence based on area
5. **Visual Overlays**:
   - ✅ Bounding boxes (green for normal, red for ROI)
   - ✅ Object labels with motion count
   - ✅ Confidence percentages (0-100%)
   - ✅ Status indicator (bottom-left)
   - ✅ AI active indicator (top-left)
   - ✅ Object counter (top-right)
   - ✅ Animated alert banners (top)
   - ✅ Timestamp (bottom-left)
   - ✅ ROI boundary visualization

---

### ✅ Modified: `backend/main_api.py`
**Changes**:

#### 1. Import AI Pipeline
```python
from core.ai_pipeline import AIProcessingPipeline
```

#### 2. Added Global AI Pipeline Instance
```python
ai_pipeline = None  # Initialized when streaming starts
```

#### 3. Refactored `gen_frames()` Function
**BEFORE** (raw streaming):
```python
def gen_frames():
    while streaming:
        success, frame = cam.read()
        if not success:
            continue
        _, buffer = cv2.imencode(".jpg", frame)  # ❌ Raw frame
        yield frame_bytes
```

**AFTER** (AI-processed streaming):
```python
def gen_frames():
    global streaming, ai_pipeline
    cam = get_camera()
    
    # Initialize AI pipeline
    if ai_pipeline is None:
        ai_pipeline = AIProcessingPipeline()

    while streaming:
        success, frame = cam.read()
        if not success:
            continue

        # ⚡ AI PROCESSING PIPELINE ⚡
        processed_frame = ai_pipeline.process_frame(frame)
        
        # Encode processed frame
        _, buffer = cv2.imencode(".jpg", processed_frame)  # ✅ AI-processed
        yield frame_bytes
```

#### 4. Enhanced `/stop` Endpoint
```python
@app.post("/stop")
def stop_camera():
    # Release camera
    cap.release()
    
    # Reset AI pipeline state ✅ NEW
    if ai_pipeline is not None:
        ai_pipeline.reset()
        ai_pipeline = None
    
    return {"status": "camera stopped", "ai_pipeline": "reset"}
```

#### 5. Added New Endpoints
```python
@app.get("/")  # Health check
@app.get("/status")  # AI status polling
```

---

### ✅ Modified: `cctv/src/App.js`
**Changes**:

#### 1. Added AI Status State
```javascript
const [aiStatus, setAiStatus] = useState("IDLE");
```

#### 2. Added Status Polling (useEffect)
```javascript
useEffect(() => {
  if (!live) return;

  const interval = setInterval(async () => {
    const response = await fetch(`${API_BASE_URL}/status`);
    const data = await response.json();
    setAiStatus(data.ai_status || "IDLE");
  }, 2000);

  return () => clearInterval(interval);
}, [live]);
```

#### 3. Added AI Status Badge UI
```javascript
{live && (
  <div className="ai-status-badge">
    <span className="ai-indicator">⚡ AI</span>
    <span className={`status-text status-${aiStatus.toLowerCase()}`}>
      {aiStatus}
    </span>
  </div>
)}
```

---

### ✅ Modified: `cctv/src/App.css`
**Changes**: Added styling for AI status badge with animations

```css
.ai-status-badge { ... }
.status-idle { background: green; }
.status-motion { background: yellow; }
.status-alert { background: red; animation: pulse; }
```

---

## 🔧 Integration Points

### Critical Integration: Where AI Happens

**Location**: `backend/main_api.py` → `gen_frames()` function → Line ~47

```python
# THIS IS THE CRITICAL INTEGRATION POINT
processed_frame = ai_pipeline.process_frame(frame)
```

**What Happens Here**:
1. Raw frame enters from camera
2. `AIProcessingPipeline.process_frame()` is called
3. Inside `process_frame()`:
   - Motion detection runs (`detector.detect()`)
   - ROI validation checks each detection
   - State machine updates (IDLE/MOTION/ALERT)
   - Visual overlays are drawn on frame
4. Processed frame exits with all AI overlays
5. Frame is encoded and streamed to frontend

**Pipeline Execution Order** (inside `process_frame()`):
```python
def process_frame(self, frame):
    # Step 1: Motion Detection
    boxes, thresh = self.detector.detect(frame)
    
    # Step 2: ROI Analysis
    for (x, y, w, h) in boxes:
        in_roi = inside_roi(x, y, w, h)
        # Draw bounding box
        # Add label
        # Add confidence
    
    # Step 3: State Machine
    self._update_state(motion_detected, roi_triggered, current_time)
    
    # Step 4: Visual Overlays
    display = self._render_overlays(display, current_time, motion_count)
    
    return display  # Fully processed frame
```

---

## 🚀 How to Run

### Terminal 1: Backend
```bash
cd F:\CCTV
uvicorn backend.main_api:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2: Frontend
```bash
cd F:\CCTV\cctv
npm start
```

### Testing Steps
1. Open browser: `http://localhost:3000`
2. Click "LIVE" button
3. **Verify AI is working**: You should see:
   - ✅ Green bounding boxes around moving objects
   - ✅ "Motion #1", "Motion #2" labels
   - ✅ Confidence percentages (e.g., "87%")
   - ✅ "AI PROCESSING: ACTIVE" (top-left)
   - ✅ "STATUS: MOTION" (bottom-left)
   - ✅ "OBJECTS: X" counter (top-right)
   - ✅ Yellow "MOTION DETECTED" banner animation
   - ✅ AI status badge (top-left) showing real-time state

---

## 🎨 Visual AI Indicators

### On-Screen Elements

1. **Top-Left Corner**:
   - "AI PROCESSING: ACTIVE" (green text)
   - AI Status Badge: "⚡ AI | IDLE/MOTION/ALERT"

2. **Top-Right Corner**:
   - "OBJECTS: X" (motion counter)

3. **Top Center**:
   - Animated banner (slides down)
   - Yellow: "MOTION DETECTED"
   - Red: "⚠ SUSPICIOUS ACTIVITY DETECTED"

4. **Bottom-Left Corner**:
   - "STATUS: IDLE/MOTION/ALERT" (color-coded)
   - Timestamp: "HH:MM:SS"

5. **On Detections**:
   - Bounding boxes (green/red)
   - Labels: "Motion #1 [ROI]"
   - Confidence: "87%"

6. **ROI Boundary**:
   - Red rectangle marking monitored zone

---

## 🧪 Verification Checklist

### Backend Verification
- [ ] Terminal shows: `Application startup complete.`
- [ ] No import errors for `core.ai_pipeline`
- [ ] `/live` endpoint streams without errors
- [ ] `/status` endpoint returns AI status

### Frontend Verification
- [ ] React app loads on `localhost:3000`
- [ ] "LIVE" button starts stream
- [ ] AI status badge appears when streaming
- [ ] Video shows processed frames (not raw camera)

### AI Visual Verification
- [ ] Move in front of camera
- [ ] Green bounding boxes appear
- [ ] Motion labels show ("Motion #1")
- [ ] Confidence percentages display
- [ ] Status changes: IDLE → MOTION
- [ ] Banner animation slides down
- [ ] AI status badge updates (IDLE → MOTION → ALERT)

### Performance Check
- [ ] Stream is smooth (no lag)
- [ ] Overlays render clearly
- [ ] No frame drops
- [ ] CPU usage acceptable (~30-50% for single core)

---

## 🐛 Troubleshooting

### Issue: "No AI overlays visible"
**Cause**: Pipeline not initialized or motion threshold too high

**Solution**:
```python
# Check config/settings.py
MIN_CONTOUR_AREA = 1500  # Lower this for more sensitive detection
```

### Issue: "Status stays IDLE even with motion"
**Cause**: Motion detected but not significant enough

**Check**:
1. Open browser console
2. Check `/status` endpoint response
3. Verify `motion_detected` is `true` in backend logs

### Issue: "Stream shows raw feed"
**Cause**: AI pipeline not being called

**Verify**:
```python
# In backend/main_api.py, line ~47, should see:
processed_frame = ai_pipeline.process_frame(frame)

# NOT:
# processed_frame = frame  # ❌ Wrong!
```

### Issue: "Import error: core.ai_pipeline"
**Cause**: File not created or wrong location

**Fix**:
```bash
# Verify file exists
ls F:\CCTV\core\ai_pipeline.py

# Should show the file
```

---

## 📊 Performance Optimization

### Current Settings
- JPEG Quality: 85% (balance between quality and bandwidth)
- Frame Processing: ~30 FPS (depends on camera)
- Motion Detection: Gaussian blur (21x21) for noise reduction

### To Improve FPS
```python
# In core/ai_pipeline.py, modify render_overlays():
# Reduce overlay complexity
# Skip some overlays for faster rendering
```

### To Reduce Bandwidth
```python
# In backend/main_api.py, modify gen_frames():
_, buffer = cv2.imencode(".jpg", processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
# Lower quality = smaller size = faster streaming
```

---

## 🔐 Production Considerations

### Security
1. **API Authentication**: Add JWT tokens to endpoints
2. **CORS Restrictions**: Limit `allow_origins` to production domain
3. **Camera Access**: Restrict to authorized users only

### Scalability
1. **Multi-Camera Support**: Create separate pipeline instances per camera
2. **Cloud Deployment**: Use WebSockets for lower latency
3. **Recording**: Add frame buffering for recording processed streams

### Monitoring
1. **Logging**: Add structured logging to pipeline
2. **Metrics**: Track FPS, detection count, alert frequency
3. **Health Checks**: Monitor `/status` endpoint for uptime

---

## 📖 API Reference

### GET `/live`
**Description**: Streams AI-processed video feed

**Response**: `multipart/x-mixed-replace` MJPEG stream

**AI Features**:
- Motion detection
- ROI validation
- Visual overlays
- Status tracking

---

### POST `/stop`
**Description**: Stops camera and resets AI pipeline

**Response**:
```json
{
  "status": "camera stopped",
  "ai_pipeline": "reset"
}
```

---

### GET `/status`
**Description**: Get current AI system status

**Response**:
```json
{
  "streaming": true,
  "camera_active": true,
  "ai_pipeline_active": true,
  "ai_status": "MOTION"
}
```

**AI Status Values**:
- `IDLE`: No motion detected
- `MOTION`: Motion detected, analyzing
- `ALERT`: Suspicious activity in ROI

---

### GET `/`
**Description**: Health check

**Response**:
```json
{
  "service": "Smart Edge-AI CCTV System",
  "version": "1.0.0",
  "ai_enabled": true,
  "streaming": false,
  "ai_pipeline_active": false
}
```

---

## 🎓 Code Explanation

### Why This Architecture?

**Single Pipeline Approach**:
- ✅ **Consistency**: Every frame processed identically
- ✅ **Maintainability**: One place to modify AI logic
- ✅ **State Management**: Pipeline maintains state across frames
- ✅ **Testability**: Easy to test pipeline in isolation

**Alternative Approaches (Not Used)**:
- ❌ Multiple endpoints (`/live-raw`, `/live-ai`) - confusing
- ❌ Frontend processing - too slow, requires JS AI libraries
- ❌ Separate AI service - adds network latency

### State Machine Design

```
IDLE ──────► MOTION ──────► ALERT
  ▲            │              │
  │            │              │
  └────────────┴──────────────┘
     (motion stops)
```

**State Transitions**:
1. `IDLE → MOTION`: Motion detected
2. `MOTION → ALERT`: Motion in ROI for >0.5s
3. `ALERT → IDLE`: No motion + cooldown period
4. `MOTION → IDLE`: Motion stopped (no ROI trigger)

---

## ✨ Future Enhancements

### AI Improvements
1. **Object Recognition**: Add YOLO/MobileNet for person/vehicle classification
2. **Face Detection**: Integrate face recognition for access control
3. **Anomaly Detection**: ML model for unusual behavior patterns
4. **License Plate Recognition**: OCR for vehicle identification

### UI Improvements
1. **Multi-Camera Grid**: Display 4/9/16 camera feeds
2. **Playback Controls**: Pause, rewind, speed control
3. **Alert History**: Timeline of detected events
4. **Export**: Download processed video clips

### Backend Improvements
1. **Database**: Store detections in PostgreSQL/MongoDB
2. **Notifications**: Email/SMS/push notifications for alerts
3. **Cloud Storage**: Upload snapshots to S3/Azure Blob
4. **Analytics**: Dashboard with detection statistics

---

## 📞 Support

**Issue**: Backend not starting?
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`

**Issue**: Frontend not connecting?
- Verify backend is running on port 8000
- Check CORS configuration in `main_api.py`
- Clear browser cache: Ctrl+Shift+Delete

**Issue**: AI not detecting motion?
- Lower `MIN_CONTOUR_AREA` in `config/settings.py`
- Increase camera brightness
- Ensure camera is not in low-light environment

---

## 🎉 Success Metrics

Your AI integration is successful if:

✅ Video stream shows processed frames (not raw camera)
✅ Bounding boxes appear around moving objects
✅ Labels and confidence scores are visible
✅ Status changes dynamically (IDLE → MOTION → ALERT)
✅ AI status badge updates in real-time
✅ Banner animations slide down on detection
✅ Frontend console shows no errors
✅ Backend logs show no warnings

**Expected User Experience**:
"When I click LIVE, I see intelligent video with green boxes around moving objects, clear labels showing what was detected, and a live status indicator that changes color based on threat level. It feels like professional surveillance software, not just a webcam feed."

---

**Status**: ✅ AI Pipeline Fully Integrated  
**Version**: 1.0.0  
**Date**: January 27, 2026
