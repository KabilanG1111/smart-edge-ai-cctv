# 🚀 QUICK START GUIDE

## System is Ready! Here's how to use it:

---

## 🎬 **START THE SYSTEM**

### Terminal 1 - Backend (Already Running ✅)
```bash
cd f:\CCTV
f:\CCTV\.venv\Scripts\python.exe -m uvicorn backend.main_api:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 - Frontend (Check if running)
```bash
cd f:\CCTV\cctv
npm start
```

---

## 🌐 **OPEN BROWSER**

Navigate to: **http://localhost:3001**

---

## 🎯 **HOW TO USE**

### 1️⃣ **Click "DEPLOY" Button**
- Big glowing button in center
- Wait 1-2 seconds for camera initialization
- Stream will start automatically

### 2️⃣ **Watch Live Feed**
- AI overlays appear on video (green/red boxes)
- Telemetry panel shows stats (right side)
- AI Core indicator pulses (top-left)

### 3️⃣ **Monitor AI Status**
- **IDLE** (Cyan): No motion detected
- **MOTION** (Orange): Movement detected
- **ALERT** (Red): Anomaly detected

### 4️⃣ **Check Anomaly Alerts**
- Red banner appears at top if anomaly detected
- Shows severity: LOW/MEDIUM/HIGH/CRITICAL
- Displays confidence percentage

### 5️⃣ **Stop Surveillance**
- Click "DISENGAGE" button
- Stream stops, camera releases

---

## 🧭 **NAVIGATION**

### Left Sidebar (4 Pages)
- **📡 LIVE COMMAND**: Real-time monitoring (current page)
- **🗄️ EVIDENCE VAULT**: AI-flagged events archive
- **⚡ ALERT CENTER**: Priority alert management
- **🤖 AI COPILOT**: Conversational intelligence

---

## 🔧 **API ENDPOINTS**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/start` | POST | Initialize camera |
| `/live` | GET | MJPEG stream |
| `/status` | GET | AI status + stats |
| `/stop` | POST | Release camera |

---

## ✅ **SYSTEM CHECK**

Run this in your browser console (F12):
```javascript
fetch('http://localhost:8000/')
  .then(r => r.json())
  .then(console.log);
```

Should return:
```json
{
  "service": "Smart Edge-AI CCTV System",
  "version": "1.0.0",
  "ai_enabled": true
}
```

---

## 🐛 **TROUBLESHOOTING**

### Problem: "Camera not available"
**Fix**: Check if another app is using camera (Zoom, Teams, etc.)

### Problem: Stream not showing
**Fix**: 
1. Open F12 console, check errors
2. Refresh page (Ctrl+R)
3. Test: `http://localhost:8000/live` directly

### Problem: CORS error
**Fix**: Backend should include `localhost:3001` in CORS origins

---

## 📊 **EXPECTED PERFORMANCE**

- **FPS**: 20-25 with AI processing
- **Latency**: 150-200ms
- **CPU Usage**: 25-35%
- **Memory**: 300-400MB

---

## 🎉 **READY TO DEMO!**

Your system has:
✅ Live camera streaming  
✅ AI motion detection  
✅ Anomaly alerts  
✅ Futuristic 2050 UI  
✅ Auto-reconnect  
✅ Real-time telemetry  

**Just click DEPLOY and watch the magic! 🚀**

---

## 📚 **MORE INFO**

- Full integration guide: `INTEGRATION_GUIDE.md`
- UI design details: `UI_2050_README.md`
- Implementation summary: `INTEGRATION_COMPLETE.md`
