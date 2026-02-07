# Production-Grade Edge AI CCTV Architecture

## 🏗️ System Architecture

### Backend: Camera Lifecycle Management

**File**: `core/camera_lifecycle_manager.py`

#### Design Principles
1. **Singleton Pattern**: Only ONE camera pipeline runs at a time across entire application
2. **Thread-Safe**: All state mutations protected by locks
3. **State Machine**: IDLE → STARTING → RUNNING → STOPPING → IDLE
4. **Graceful Shutdown**: Proper resource cleanup on Ctrl+C, reload, or crash
5. **GStreamer Integration**: Proper pipeline state transitions (NULL state on cleanup)

#### State Management
```python
class CameraState(Enum):
    IDLE = "IDLE"          # No camera running
    STARTING = "STARTING"  # Initializing camera
    RUNNING = "RUNNING"    # Active streaming
    STOPPING = "STOPPING"  # Cleaning up resources
    ERROR = "ERROR"        # Failure state
```

#### Key Methods
- `start_stream()`: Initialize camera, prevent duplicate starts
- `stop_stream()`: Release camera, set GStreamer to NULL state
- `read_frame()`: Thread-safe frame reading with counter
- `shutdown()`: Emergency cleanup on Ctrl+C
- `get_state()`: Current state, frame count, errors

---

## 🎬 Camera Lifecycle Flow

### Start Stream
```
Frontend clicks "Deploy"
  ↓
POST /start
  ↓
camera_manager.start_stream()
  ↓
Check current state (prevent duplicate)
  ↓
Release any existing camera
  ↓
Initialize cv2.VideoCapture or GStreamer
  ↓
Test read frame (verify camera works)
  ↓
Set state to RUNNING
  ↓
Return success to frontend
  ↓
GET /live starts MJPEG stream
  ↓
gen_frames() reads from camera_manager
```

### Stop Stream
```
Frontend clicks "Disengage" OR Backend Ctrl+C
  ↓
POST /stop OR signal_handler(SIGINT)
  ↓
Set streaming = False (stops gen_frames loop)
  ↓
camera_manager.stop_stream()
  ↓
Release camera (cap.release())
  ↓
GStreamer pipeline → NULL state (automatic via OpenCV)
  ↓
Reset AI pipeline
  ↓
Set state to IDLE
  ↓
Resources fully released
```

---

## 📈 Frame Counter Behavior

### Why Frame Count Increases Continuously

**This is EXPECTED and CORRECT behavior for live video:**

1. **Live Video is Continuous**: Camera captures at 30 FPS
   - 30 frames/second × 60 seconds = 1,800 frames/minute
   - Frame count tracks total processed frames since stream start

2. **Surveillance Analytics**: Frame counter is used for:
   - Performance monitoring (FPS calculation)
   - Anomaly detection statistics
   - System health metrics
   - Debugging and logging

3. **Counter Resets Only On**:
   - Stream stop/restart
   - Backend restart
   - Explicit reset command

### Managing Frame Counts WITHOUT Stopping Stream

**Option 1: Rolling Window Statistics** (Recommended)
```python
# Track last N frames for real-time metrics
recent_anomalies = deque(maxlen=1000)  # Last 1000 frames
recent_fps = deque(maxlen=30)  # Last 30 FPS samples

# Display rolling metrics instead of total count
ui_display = {
    "anomalies_last_1k": len([x for x in recent_anomalies if x]),
    "avg_fps_30s": sum(recent_fps) / len(recent_fps)
}
```

**Option 2: Periodic Reset** (Production pattern)
```python
# Reset counters every N frames without stopping camera
if frame_count % 10000 == 0:
    ai_pipeline.reset_statistics()  # Reset metrics, not camera
    frame_count = 0  # Reset counter
```

**Option 3: Separate Analytics Counter**
```python
# Keep total_frames, but show session_frames
session_start_count = frame_count
ui_display = {
    "session_frames": frame_count - session_start_count,
    "total_frames": frame_count  # For system logs
}
```

---

## 🚨 Graceful Shutdown Implementation

### Backend Signal Handlers

**File**: `backend/main_api.py`

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    def signal_handler(sig, frame):
        print(f"Received signal {sig}, shutting down...")
        cleanup_on_shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Kill
    
    yield  # Server runs
    
    # Shutdown
    cleanup_on_shutdown()

def cleanup_on_shutdown():
    """Ensures camera and GStreamer are properly released"""
    streaming = False
    camera_manager.shutdown()  # Force release camera
    if ai_pipeline:
        ai_pipeline.reset()
```

### What Happens on Ctrl+C
1. Signal handler catches SIGINT
2. `cleanup_on_shutdown()` called
3. Camera manager stops streaming
4. `cap.release()` called (releases camera hardware)
5. GStreamer pipeline → NULL state (OpenCV handles this)
6. AI pipeline reset
7. Server exits cleanly

### Uvicorn Auto-Reload Handling
When file changes trigger reload:
1. Lifespan shutdown event fires
2. Cleanup runs automatically
3. New process starts with clean state
4. Camera available for new process

---

## 🔄 Frontend Reconnect Strategy

### Recommended React Logic

**File**: `cctv/src/pages/LiveStream.js`

```javascript
const LiveStream = () => {
  const [connectionState, setConnectionState] = useState('disconnected');
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 3;
  const retryDelay = 2000; // 2 seconds

  const startStreamWithRetry = async () => {
    setConnectionState('connecting');
    
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        // 1. Call /start to initialize camera
        const startResponse = await fetch(`${API_BASE_URL}/start`, { 
          method: "POST",
          timeout: 5000  // 5 second timeout
        });
        
        if (!startResponse.ok) {
          throw new Error(`Start failed: ${startResponse.status}`);
        }
        
        // 2. Verify backend is ready
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 3. Start MJPEG stream
        const streamUrl = `${API_BASE_URL}/live?t=${Date.now()}`;
        imgRef.current.src = streamUrl;
        
        setConnectionState('connected');
        setRetryCount(0);
        return;
        
      } catch (error) {
        console.error(`Connection attempt ${attempt + 1} failed:`, error);
        setRetryCount(attempt + 1);
        
        if (attempt < maxRetries - 1) {
          console.log(`Retrying in ${retryDelay}ms...`);
          await new Promise(resolve => setTimeout(resolve, retryDelay));
        }
      }
    }
    
    // All retries failed
    setConnectionState('failed');
    setError(`Failed to connect after ${maxRetries} attempts`);
  };

  // Auto-reconnect on stream error
  useEffect(() => {
    if (!imgRef.current) return;
    
    const handleError = () => {
      if (connectionState === 'connected') {
        console.warn('Stream lost, attempting reconnect...');
        setConnectionState('reconnecting');
        startStreamWithRetry();
      }
    };
    
    imgRef.current.addEventListener('error', handleError);
    return () => imgRef.current?.removeEventListener('error', handleError);
  }, [connectionState]);

  // Health check polling
  useEffect(() => {
    if (connectionState !== 'connected') return;
    
    const healthCheck = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();
        
        // Backend stopped streaming but frontend still thinks it's active
        if (!data.streaming && connectionState === 'connected') {
          console.warn('Backend stopped streaming, reconnecting...');
          startStreamWithRetry();
        }
      } catch (error) {
        console.error('Health check failed:', error);
      }
    }, 5000); // Check every 5 seconds
    
    return () => clearInterval(healthCheck);
  }, [connectionState]);

  return (
    <div>
      {connectionState === 'connecting' && <div>Connecting...</div>}
      {connectionState === 'reconnecting' && (
        <div>Connection lost, retrying ({retryCount}/{maxRetries})...</div>
      )}
      {connectionState === 'failed' && (
        <div>
          Connection failed. 
          <button onClick={startStreamWithRetry}>Try Again</button>
        </div>
      )}
      <img ref={imgRef} />
    </div>
  );
};
```

### Connection States
- `disconnected`: Initial state, camera off
- `connecting`: Starting camera, waiting for /start
- `connected`: Active stream, receiving frames
- `reconnecting`: Lost connection, attempting recovery
- `failed`: All retry attempts exhausted

---

## 🛡️ Why This Architecture is Production-Grade

### 1. **Single Pipeline Guarantee**
- Singleton pattern prevents multiple camera instances
- State machine prevents concurrent starts
- Thread locks ensure atomic operations

### 2. **Resource Safety**
- All resources released on ANY exit path (normal, Ctrl+C, crash)
- GStreamer pipeline properly transitioned to NULL
- No zombie processes or locked camera devices

### 3. **Fault Tolerance**
- Automatic retry on frame read failures
- Graceful degradation on errors
- State tracking for debugging

### 4. **Operational Excellence**
- Frame counter for performance monitoring
- State reporting for system health
- Logging at every lifecycle transition

### 5. **Developer Experience**
- Clean FastAPI lifespan events
- Signal handlers for Ctrl+C
- Hot reload support

---

## 🚀 Deployment Checklist

### Backend Startup
```bash
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Start server with auto-reload
python -m uvicorn backend.main_api:app --host 0.0.0.0 --port 8000 --reload

# Server will:
# - Register signal handlers
# - Initialize camera lifecycle manager
# - Cleanup on Ctrl+C automatically
```

### Frontend Startup
```bash
cd cctv
npm start

# React app will:
# - Connect to backend on localhost:8000
# - Implement retry logic
# - Handle connection errors gracefully
```

### Stopping System
```bash
# Backend: Ctrl+C (graceful shutdown)
# - Signal handler catches SIGINT
# - cleanup_on_shutdown() runs
# - Camera released, GStreamer → NULL
# - Process exits cleanly

# Frontend: Ctrl+C (React dev server)
# - No cleanup needed (stateless client)
```

---

## 📊 Monitoring & Debugging

### Check Camera State
```bash
curl http://localhost:8000/status
```

Response:
```json
{
  "streaming": true,
  "camera_active": true,
  "camera_state": "RUNNING",
  "frame_count": 1524,
  "ai_pipeline_active": true
}
```

### Verify Singleton Behavior
```python
# Multiple calls to start_stream() should return:
# First call:  (True, "Camera started successfully")
# Second call: (True, "Camera already running")
# ⚠️ Camera hardware NOT reinitialized on second call
```

### Test Graceful Shutdown
1. Start backend and camera
2. Press Ctrl+C
3. Verify logs show:
   ```
   ⚠️  Received signal 2, shutting down gracefully...
   🧹 Starting cleanup...
   🛑 Emergency shutdown triggered
   🔓 Camera released
   ✅ Emergency shutdown complete
   ✅ Cleanup complete
   ```
4. Restart backend - camera should be available (not locked)

---

## 🎯 Key Takeaways

1. **Frame Counter**: Continuous increase is NORMAL and EXPECTED for live video
2. **Singleton Pattern**: Only ONE camera pipeline runs, preventing conflicts
3. **Graceful Shutdown**: Ctrl+C properly releases camera and GStreamer
4. **State Tracking**: IDLE/RUNNING states prevent duplicate starts
5. **Frontend Retry**: Implement exponential backoff and health checks
6. **Resource Cleanup**: ALL exit paths call cleanup (normal, error, signal)
7. **Production Ready**: Thread-safe, fault-tolerant, monitorable

---

## 🔧 Troubleshooting

### Issue: "Connection Severed" after restart
**Cause**: Backend not running or camera locked from previous crash
**Fix**: 
1. Kill any zombie Python processes: `taskkill /F /IM python.exe`
2. Restart backend with proper lifecycle manager
3. Frontend will auto-retry connection

### Issue: Multiple streams cause instability
**Cause**: Old code allowed multiple VideoCapture instances
**Fix**: Lifecycle manager enforces singleton, prevents duplicates

### Issue: GStreamer pipeline doesn't stop on Ctrl+C
**Cause**: No signal handlers registered
**Fix**: FastAPI lifespan + signal handlers ensure cleanup

### Issue: Frame count too high
**Not an issue**: This is surveillance system - frames counted since start
**Management**: Use rolling windows or periodic resets (see above)
