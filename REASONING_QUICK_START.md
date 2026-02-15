# 🚀 QUICK START - Real-Time Reasoning Engine

## 1-Minute Start Guide

### STEP 1: Start Backend
```powershell
cd F:\CCTV
.\.venv\Scripts\python.exe -m uvicorn backend.main_api:app --host 0.0.0.0 --port 8001
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
🧠 Realtime Reasoning Engine initialized
```

### STEP 2: Test WebSocket (Quick Test)
Open in browser: `F:\CCTV\test_reasoning_websocket.html`

**You should see**:
- ✅ Video feed on left (camera working)
- ✅ Green status dot (WebSocket connected)
- ✅ Events appearing on right as you move
- ✅ Colors: Red (critical), Yellow (warning), Cyan (normal)

### STEP 3: React Frontend (Full Experience)
```powershell
cd F:\CCTV\cctv
npm start
```

Navigate to: `http://localhost:3000` → **Intelligence Core** page

---

## Expected Behavior

### ✅ Correct Operation
1. Camera starts → Video streams
2. You move in front of camera
3. YOLO detects → "New person detected (ID 1)" (cyan)
4. After 15 seconds stationary → "Person ID 1 loitering for 15s" (yellow)
5. Move quickly → "Person ID 1 abnormal movement detected" (red)
6. Events appear instantly (no delay)

### ❌ Troubleshooting

**No video feed?**
```powershell
# Check if camera is connected
# Backend will try camera sources 0, 1, 2 automatically
```

**No events appearing?**
- Open browser console (F12)
- Look for: "🧠 Reasoning Engine connected"
- If not connected: Backend not running or wrong port

**Events but no colors?**
- Check browser console for JavaScript errors
- Verify CSS loaded correctly

**Backend errors?**
```powershell
# Install missing dependencies
cd F:\CCTV
.\.venv\Scripts\python.exe -m pip install websockets ultralytics opencv-python numpy
```

---

## Quick Test Commands

### Check Backend Status
```powershell
Invoke-WebRequest -Uri "http://localhost:8001/" -UseBasicParsing
# Should return: StatusCode: 200
```

### Test WebSocket (PowerShell)
```powershell
# Open test page
Start-Process "F:\CCTV\test_reasoning_websocket.html"
```

### View Backend Logs
Backend console shows:
```
🔍 Frame 30: 1 detections, 1 tracked
🧠 Reasoning: 1 events | Tracking 1 objects
🔌 WebSocket client connected. Total clients: 1
```

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `http://localhost:8001/` | GET | Health check |
| `http://localhost:8001/video_feed` | GET | MJPEG video stream |
| `ws://localhost:8001/ws/reasoning` | WebSocket | Real-time reasoning events |
| `http://localhost:8001/api/intelligence/live` | GET | Polling endpoint (legacy) |

---

## Test Scenarios

### Scenario 1: Detection Test
1. Move in front of camera
2. Wait 2 seconds
3. **Expected**: "New person detected (ID X)" (cyan)

### Scenario 2: Loitering Test
1. Stand still in front of camera
2. Wait 15 seconds
3. **Expected**: "Person ID X loitering for 15s" (yellow)

### Scenario 3: Speed Test
1. Move quickly across camera view
2. **Expected**: "Person ID X abnormal movement detected" (red)

### Scenario 4: Multi-Person Test
1. Have 3+ people in view
2. **Expected**: "Multiple people detected: X individuals in view" (cyan)

---

## File Locations

| Component | Path |
|-----------|------|
| Reasoning Engine | `F:\CCTV\core\reasoning_engine.py` |
| WebSocket Endpoint | `F:\CCTV\backend\main_api.py` |
| React Component | `F:\CCTV\cctv\src\pages\IntelligenceCore.js` |
| Styles | `F:\CCTV\cctv\src\pages\IntelligenceCore.css` |
| Test Page | `F:\CCTV\test_reasoning_websocket.html` |
| Documentation | `F:\CCTV\REALTIME_REASONING_ENGINE_COMPLETE.md` |

---

## Severity Reference

| Level | Color | Hex | Triggers |
|-------|-------|-----|----------|
| CRITICAL | 🔴 Red | #ff0055 | High speed (150+ px/s) |
| WARNING | 🟡 Yellow | #ff9100 | Loitering (15s), Stationary (30s), Confidence drop |
| NORMAL | 🔵 Cyan | #00d9ff | New detection, Crowd (3+ people) |

---

## Support

**Backend not starting?**
- Check Python version: `python --version` (should be 3.8+)
- Check virtual environment: `.\.venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements_stable.txt`

**Frontend not connecting?**
- Verify backend running: `http://localhost:8001/`
- Check port in code: Should be `8001` (not 8000)
- Clear browser cache and reload

**No detections?**
- Verify camera working: Check video feed shows image
- Check lighting: YOLO needs good lighting
- Lower confidence: Already set to 0.25 (CPU-optimized)

---

**Status**: ✅ System operational on port 8001  
**Last Updated**: February 15, 2026
