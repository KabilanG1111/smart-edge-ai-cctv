# ✅ QUICK START CHECKLIST - Stream Integration

## Before You Start

Make sure you have:
- [ ] Backend code saved (no syntax errors)
- [ ] Frontend code saved (React app compiled)
- [ ] Camera connected (or will use test pattern)

---

## 🚀 START SEQUENCE

### 1️⃣ **Start Backend** (Terminal 1)

```bash
cd f:\CCTV
f:\CCTV\.venv\Scripts\python.exe -m uvicorn backend.main_api:app --reload --host 127.0.0.1 --port 8000
```

✅ **Success looks like:**
```
INFO: Application startup complete.
```

❌ **If it fails:**
- Check for Python syntax errors
- Verify virtual environment is active
- Check if port 8000 is already in use

---

### 2️⃣ **Verify Backend Works** (New Browser Tab)

Open: **http://localhost:8000/live**

✅ **Success looks like:**
- Video stream appears immediately
- You see motion detection boxes
- Smooth video playback

❌ **If it fails:**
- Check backend terminal for errors
- Verify camera is connected
- Try test_stream.html instead

---

### 3️⃣ **Start Frontend** (Terminal 2)

```bash
cd f:\CCTV\cctv
npm start
```

✅ **Success looks like:**
```
Compiled successfully!
Local: http://localhost:3001
```

❌ **If it fails:**
- Run `npm install` first
- Check for syntax errors in .js files
- Clear node_modules and reinstall

---

### 4️⃣ **Open React App**

Open: **http://localhost:3001**

✅ **Success looks like:**
- Futuristic dark UI loads
- Side navigation visible
- "DEPLOY" button visible in center

---

### 5️⃣ **Deploy Stream**

1. **Open DevTools**: Press F12
2. **Go to Console tab**
3. **Click DEPLOY button**
4. **Watch console logs**

✅ **Success logs:**
```
🚀 [DEPLOY] User clicked DEPLOY button
📡 [API] Calling POST http://localhost:8000/start
✅ [API] Camera initialized
📹 [STREAM] Starting MJPEG stream
✅ [STATE] Stream marked as active
✅ [STREAM] First frame loaded!
```

✅ **Success visuals:**
- Placeholder disappears
- Live video appears
- AI overlays visible
- Telemetry panel shows stats

---

## ❓ TROUBLESHOOTING SHORTCUTS

### Backend Won't Start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install fastapi uvicorn opencv-python
```

### Frontend Won't Compile
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm start
```

### Stream Won't Load
1. Verify backend is running: `http://localhost:8000/`
2. Check console for errors (F12)
3. Try test_stream.html
4. Refresh page (Ctrl+Shift+R)

### Video Appears But Placeholder Doesn't Hide
- Check `live` state in React DevTools
- Verify CSS is loaded (check Elements tab)
- Force refresh (Ctrl+Shift+R)

---

## 🎯 EXPECTED FINAL RESULT

When everything works correctly, you should see:

```
┌─────────────────────────────────────────────────┐
│  [📡 LIVE COMMAND]                              │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │  🤖 AI CORE    [MOTION]                   │ │
│  │                                           │ │
│  │     [LIVE VIDEO WITH GREEN BOXES]         │ │
│  │                                           │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│         [⏸ DISENGAGE]                          │
│                                                 │
│                          ┌──────────────────┐  │
│                          │ 📊 TELEMETRY     │  │
│                          │ FPS: 25          │  │
│                          │ Latency: 180ms   │  │
│                          │ Frames: 1547     │  │
│                          │ Anomalies: 12    │  │
│                          └──────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 📝 NOTES

- **First run**: Backend may take 2-3 seconds to initialize camera
- **Latency**: 150-200ms is normal for localhost
- **FPS**: 20-25 FPS is normal with AI processing
- **Auto-reconnect**: If stream drops, waits 2 seconds then retries
- **Console logs**: Use them! They show exactly what's happening

---

## 🎉 SUCCESS INDICATORS

You know it's working when:
- ✅ No errors in console
- ✅ Video is smooth and clear
- ✅ Motion detection boxes appear
- ✅ AI status changes with movement
- ✅ Telemetry numbers update
- ✅ Can stop and restart stream multiple times

---

**Ready? Start with Step 1! 🚀**
