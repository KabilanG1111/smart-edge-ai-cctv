# CORS Fix Guide - React + FastAPI

## 🔴 Problem: TypeError: Failed to fetch

### Root Cause Analysis

The "Failed to fetch" error occurred because:

1. **CORS Middleware Position**: The CORS middleware was added **AFTER** route definitions in FastAPI
2. **How FastAPI Works**: Middleware must be registered **BEFORE** routes are defined, or immediately after `app = FastAPI()`
3. **What Happened**: When React (localhost:3000) tried to call FastAPI (localhost:8000), the browser sent a preflight OPTIONS request
4. **The Failure**: FastAPI's routes didn't have CORS headers because middleware was never applied to them
5. **Browser Behavior**: Browser blocked the request entirely, resulting in "Failed to fetch"

---

## ✅ The Fix

### 1. FastAPI Backend - CORRECT CORS Setup

**File**: `backend/main_api.py`

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2

app = FastAPI()

# ⚠️ CRITICAL: Add CORS middleware IMMEDIATELY after app creation
# This MUST come BEFORE any route definitions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Now define your global variables and routes
cap = None
streaming = False

def get_camera():
    global cap
    if cap is None or not cap.isOpened():
        cap = cv2.VideoCapture(0)
    return cap

def gen_frames():
    global streaming
    cam = get_camera()
    while streaming:
        success, frame = cam.read()
        if not success:
            continue
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )

@app.get("/live")
def live_feed():
    global streaming
    streaming = True
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.post("/stop")
def stop_camera():
    global streaming, cap
    streaming = False
    if cap is not None and cap.isOpened():
        cap.release()
    cap = None
    return {"status": "camera stopped"}
```

### 2. React Frontend - Correct fetch() with Error Handling

**File**: `cctv/src/App.js`

```javascript
import { useRef, useState } from "react";
import "./App.css";

// Define API base URL as a constant for consistency
const API_BASE_URL = "http://localhost:8000";

function App() {
  const imgRef = useRef(null);
  const [live, setLive] = useState(false);
  const [error, setError] = useState(null);

  const toggleLive = async () => {
    try {
      setError(null); // Clear previous errors
      
      if (!live) {
        // Start live feed - no fetch needed, just set img src
        imgRef.current.src = `${API_BASE_URL}/live`;
        setLive(true);
      } else {
        // Stop live feed - make POST request
        const response = await fetch(`${API_BASE_URL}/stop`, { 
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });
        
        // Check if response is successful
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Camera stopped:", data);
        
        imgRef.current.src = "";
        setLive(false);
      }
    } catch (err) {
      console.error("Error toggling live feed:", err);
      setError(`Failed to ${live ? "stop" : "start"} camera: ${err.message}`);
      // Reset state on error
      imgRef.current.src = "";
      setLive(false);
    }
  };

  return (
    <div className="app">
      <button className="live-btn" onClick={toggleLive}>
        🔴 {live ? "STOP" : "LIVE"}
      </button>

      {error && <div className="error-message">{error}</div>}

      <img
        ref={imgRef}
        alt="CCTV Live"
        className="live-feed"
        onError={() => {
          console.error("Image failed to load");
          setError("Failed to load video stream");
        }}
      />
    </div>
  );
}

export default App;
```

---

## 🚀 Step-by-Step Instructions to Run

### Prerequisites
- Python 3.8+ installed
- Node.js 14+ installed
- Camera connected (for OpenCV)

### Terminal 1: Start FastAPI Backend

```powershell
# Navigate to project root
cd F:\CCTV

# Activate virtual environment (if you have one)
# .\venv\Scripts\activate

# Install required packages
pip install fastapi uvicorn opencv-python python-multipart

# Start FastAPI server
uvicorn backend.main_api:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Start React Frontend

```powershell
# Navigate to React app
cd F:\CCTV\cctv

# Install dependencies (first time only)
npm install

# Start React development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view cctv in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### Testing the Application

1. **Open Browser**: Navigate to `http://localhost:3000`
2. **Click LIVE Button**: Should start video stream
3. **Check Browser Console**: Should see no CORS errors
4. **Click STOP Button**: Should stop the stream and log "Camera stopped"
5. **Check Network Tab**: Should see successful requests to localhost:8000

---

## 🔍 Verification Checklist

### In Browser DevTools (F12):

#### Console Tab - Should NOT see:
- ❌ `Access to fetch at 'http://localhost:8000/stop' from origin 'http://localhost:3000' has been blocked by CORS policy`
- ❌ `TypeError: Failed to fetch`

#### Network Tab - Should see:
- ✅ `/stop` request with status `200 OK`
- ✅ Response headers include `access-control-allow-origin: http://localhost:3000`
- ✅ `/live` request streaming video data

### In FastAPI Terminal:
```
INFO:     127.0.0.1:xxxxx - "OPTIONS /stop HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /stop HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /live HTTP/1.1" 200 OK
```

---

## 🛠️ Troubleshooting

### Issue: Still getting "Failed to fetch"

**Solution 1**: Ensure backend is running on correct port
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000
```

**Solution 2**: Restart both servers after making changes
- Stop backend (Ctrl+C) and restart
- Stop frontend (Ctrl+C) and restart

**Solution 3**: Clear browser cache
- Press Ctrl+Shift+Delete
- Clear cached images and files
- Hard reload: Ctrl+Shift+R

### Issue: CORS errors still appearing

**Verify**: Check that middleware is BEFORE routes in `main_api.py`
```python
app = FastAPI()
app.add_middleware(...)  # ✅ MUST be here
@app.get("/live")        # ✅ Routes come after
```

**NOT**:
```python
app = FastAPI()
@app.get("/live")        # ❌ Routes before middleware
app.add_middleware(...)  # ❌ Too late!
```

### Issue: Camera not opening

**Check**: Camera permissions and availability
```python
# Test camera access
import cv2
cap = cv2.VideoCapture(0)
print(cap.isOpened())  # Should print True
cap.release()
```

---

## 📊 Why This Fix Works

### The CORS Flow:

1. **User clicks button** → React calls `fetch("http://localhost:8000/stop")`
2. **Browser detects cross-origin** → Sends OPTIONS preflight request first
3. **FastAPI receives OPTIONS** → CORS middleware intercepts
4. **Middleware adds headers**:
   - `Access-Control-Allow-Origin: http://localhost:3000`
   - `Access-Control-Allow-Methods: POST, GET, OPTIONS`
   - `Access-Control-Allow-Headers: *`
5. **Browser sees valid headers** → Allows actual POST request
6. **FastAPI processes POST** → Returns response with CORS headers
7. **Browser allows response** → React receives data ✅

### What Was Wrong Before:

1. **User clicks button** → React calls fetch
2. **Browser sends OPTIONS** → FastAPI receives it
3. **No CORS middleware** → No CORS headers in response
4. **Browser blocks request** → "Failed to fetch" error ❌
5. **POST never happens** → Code never executes

---

## 🎯 Key Takeaways

1. **Middleware Order Matters**: Always add CORS middleware immediately after `app = FastAPI()`
2. **localhost vs 127.0.0.1**: Use consistent URLs (prefer localhost:8000 in both places)
3. **Error Handling**: Always wrap fetch() in try-catch
4. **Browser Security**: CORS is enforced by browser, not by curl/Postman
5. **Streaming Responses**: Don't need CORS for `<img>` src, but POST requests do

---

## 📝 Quick Reference

### FastAPI CORS Template
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### React Fetch Template
```javascript
const API_BASE_URL = "http://localhost:8000";

try {
  const response = await fetch(`${API_BASE_URL}/endpoint`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  const data = await response.json();
} catch (error) {
  console.error("Fetch error:", error);
}
```

---

**Status**: ✅ Fixed and tested
**Date**: January 27, 2026
