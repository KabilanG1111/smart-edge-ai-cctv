# 🎯 QUICK START GUIDE - Smart Edge-AI CCTV System

## ✅ What You Got

### Before (Original System)
- ❌ Raw camera feed only
- ❌ No visual AI indicators
- ❌ AI modules existed but NOT integrated into video stream
- ❌ Frontend showed plain webcam output

### After (AI-Integrated System)
- ✅ **Every frame processed through AI pipeline**
- ✅ **Real-time motion detection with bounding boxes**
- ✅ **ROI validation (red boxes for suspicious areas)**
- ✅ **Confidence scoring (0-100%) on each detection**
- ✅ **Dynamic status tracking (IDLE → MOTION → ALERT)**
- ✅ **Animated alert banners**
- ✅ **Live AI status badge in frontend**
- ✅ **Visual overlays: labels, timestamps, counters**

---

## 🚀 Run It Now

### Step 1: Start Backend (FastAPI)
```bash
# Open PowerShell in F:\CCTV
cd F:\CCTV
uvicorn backend.main_api:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Start Frontend (React)
```bash
# Open new PowerShell in F:\CCTV\cctv
cd F:\CCTV\cctv
npm start
```

**Expected Output**:
```
Compiled successfully!
Local: http://localhost:3000
```

### Step 3: Test AI Features
1. Open browser: **http://localhost:3000**
2. Click **"LIVE"** button
3. Move in front of camera
4. **Watch for AI overlays**:
   - Green bounding boxes around motion
   - "Motion #1", "Motion #2" labels
   - Confidence percentages (e.g., "87%")
   - Status changes: IDLE → MOTION
   - Yellow banner: "MOTION DETECTED"
   - AI status badge (top-left): ⚡ AI | MOTION

---

## 🎨 Visual AI Features You'll See

### On Every Frame:
1. **Top-Left**: "AI PROCESSING: ACTIVE" + AI status badge
2. **Top-Right**: "OBJECTS: X" (motion counter)
3. **Top-Center**: Animated banner (when motion detected)
4. **Bottom-Left**: "STATUS: IDLE/MOTION/ALERT" + Timestamp
5. **Around Motion**: Green/red bounding boxes with labels
6. **On Boxes**: Confidence percentages

### Color Coding:
- 🟢 **Green boxes**: Normal motion detected
- 🔴 **Red boxes**: Motion in ROI (suspicious area)
- 🟡 **Yellow banner**: "MOTION DETECTED"
- 🔴 **Red banner**: "⚠ SUSPICIOUS ACTIVITY DETECTED"

---

## 🔍 Architecture Overview

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Camera     │────►│  AI Pipeline    │────►│   Stream     │
│ (Raw Frames) │     │  • Detect       │     │ (Processed)  │
└──────────────┘     │  • Classify     │     └──────────────┘
                     │  • Draw         │            │
                     │  • Encode       │            ▼
                     └─────────────────┘     ┌──────────────┐
                                             │  Frontend    │
                                             │  (Display)   │
                                             └──────────────┘
```

### Critical Integration Point
**File**: `backend/main_api.py`
**Line**: ~47
```python
# THIS LINE IS WHERE AI MAGIC HAPPENS:
processed_frame = ai_pipeline.process_frame(frame)
```

**Before this line**: Raw camera frame
**After this line**: AI-processed frame with overlays
**Streamed to frontend**: Processed frame only (NOT raw)

---

## 📁 Files Modified/Created

### ✅ Created
- `core/ai_pipeline.py` - Unified AI processing pipeline (250 lines)
- `AI_PIPELINE_INTEGRATION.md` - Complete documentation
- `QUICK_START.md` - This file

### ✅ Modified
- `backend/main_api.py` - Integrated AI pipeline into streaming
- `cctv/src/App.js` - Added AI status polling & badge
- `cctv/src/App.css` - Added AI status badge styling

---

## 🧪 Verification Checklist

### Backend Running?
- [ ] Terminal shows "Application startup complete"
- [ ] No import errors
- [ ] Port 8000 is listening

### Frontend Running?
- [ ] Terminal shows "Compiled successfully"
- [ ] Browser opens at localhost:3000
- [ ] No console errors

### AI Working?
- [ ] Click "LIVE" button
- [ ] Video stream loads
- [ ] AI status badge appears (top-left)
- [ ] Move in front of camera
- [ ] Green bounding boxes appear
- [ ] Labels show ("Motion #1")
- [ ] Status changes to "MOTION"
- [ ] Banner animates from top
- [ ] Confidence percentages visible

### ✅ SUCCESS CRITERIA
**If you see bounding boxes, labels, and AI status badge → AI integration is working!**

---

## 🐛 Troubleshooting

### Issue: "No bounding boxes appearing"
**Solution**: Move more dramatically or lower motion threshold
```python
# Edit: config/settings.py
MIN_CONTOUR_AREA = 500  # Lower = more sensitive
```

### Issue: "Stream shows plain camera feed"
**Problem**: AI pipeline not being called

**Check**: Open `backend/main_api.py` and verify line ~47:
```python
processed_frame = ai_pipeline.process_frame(frame)  # ✅ Should be this
# NOT: processed_frame = frame  # ❌ Wrong!
```

### Issue: "Import errors in backend"
**Solution**: Packages already installed, just Pylance warnings
```bash
# Verify installation:
pip list | grep -E "fastapi|uvicorn|opencv"

# Should show:
# fastapi       0.128.0
# uvicorn       0.40.0
# opencv-python 4.13.0.90
```

### Issue: "Frontend shows 'Failed to load video stream'"
**Check**:
1. Backend is running on port 8000?
2. Camera is connected and accessible?
3. Browser console for actual error message

---

## 📊 Performance Benchmarks

### Expected Performance:
- **FPS**: 25-30 (depends on camera)
- **Latency**: <100ms (local network)
- **CPU Usage**: 30-50% (single core)
- **Memory**: ~200-300MB (Python process)

### If Performance is Poor:
```python
# Option 1: Lower JPEG quality (in backend/main_api.py, line ~51)
cv2.imencode(".jpg", processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 70])

# Option 2: Lower motion sensitivity (in config/settings.py)
MIN_CONTOUR_AREA = 2500  # Higher = less processing

# Option 3: Skip some overlays (in core/ai_pipeline.py)
# Comment out non-essential overlay code
```

---

## 🎓 Understanding the Code

### Key Classes

#### `AIProcessingPipeline` (core/ai_pipeline.py)
**Purpose**: Unified AI processing engine

**Main Method**: `process_frame(frame)`
```python
def process_frame(self, frame):
    # 1. Detect motion
    boxes, thresh = self.detector.detect(frame)
    
    # 2. Validate ROI
    for (x, y, w, h) in boxes:
        in_roi = inside_roi(x, y, w, h)
    
    # 3. Update state
    self._update_state(motion_detected, roi_triggered, time)
    
    # 4. Render overlays
    display = self._render_overlays(frame, time, count)
    
    return display  # Processed frame
```

**State Machine**:
```
IDLE ──motion──► MOTION ──roi_trigger──► ALERT
  ▲                 │                       │
  └─────────────────┴───────────────────────┘
         (motion stops / cooldown)
```

### Key Endpoints

#### `GET /live`
- Starts streaming
- Initializes AI pipeline
- Returns processed frames

#### `POST /stop`
- Stops streaming
- Releases camera
- Resets AI pipeline

#### `GET /status`
- Returns current AI state
- Polled by frontend every 2s

---

## 🔐 Production Deployment

### Before Deploying:

1. **Add Authentication**:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.get("/live")
def live_feed(credentials: HTTPBasicCredentials = Depends(security)):
    # Validate credentials
    if credentials.username != "admin" or credentials.password != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    # ... rest of code
```

2. **Update CORS**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Production domain
    # ...
)
```

3. **Enable HTTPS**:
```bash
uvicorn backend.main_api:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

---

## 📞 Need Help?

### Check Logs:
```bash
# Backend logs
# Already visible in terminal running uvicorn

# Frontend logs
# Open browser console (F12)
```

### Common Error Messages:

**"Import cv2 could not be resolved"**
- Ignore - this is just Pylance warning
- Code runs fine (opencv is installed)

**"Failed to fetch"**
- Backend not running
- CORS issue
- Wrong URL

**"Camera not accessible"**
- Camera in use by another app
- No camera connected
- Permissions issue

---

## 🎉 You're Done!

### What You Achieved:
✅ Integrated motion detection into live stream
✅ Added real-time visual overlays
✅ Implemented state machine (IDLE/MOTION/ALERT)
✅ Created frontend AI status display
✅ Built production-ready AI pipeline architecture

### Next Steps (Optional):
1. Add object recognition (YOLO)
2. Implement face detection
3. Add database for event logging
4. Create alert notification system
5. Add multi-camera support

---

## 📚 Documentation Files

1. **AI_PIPELINE_INTEGRATION.md** - Complete technical documentation
2. **CORS_FIX_GUIDE.md** - CORS troubleshooting guide
3. **QUICK_START.md** - This file (quick reference)

---

**Status**: ✅ AI Integration Complete
**System**: Smart Edge-AI CCTV
**Date**: January 27, 2026
**Version**: 1.0.0

**Enjoy your intelligent CCTV system! 🚀**
