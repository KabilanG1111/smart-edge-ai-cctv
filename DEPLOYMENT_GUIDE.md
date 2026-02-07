# 🚀 Hackathon Demo Deployment Guide
## FastAPI + React + ngrok Production Setup

**YOU NEED EXACTLY 3 TERMINALS. NO MORE, NO LESS.**

---

## 🎯 The Brutal Truth

### Why Your Setup Keeps Breaking:

1. **Hardcoded localhost** → Frontend couldn't reach ngrok-exposed backend
2. **CORS blocking ngrok** → Backend rejected requests from ngrok frontend
3. **Process dies when terminal closes** → Closing terminal = killing backend/ngrok
4. **No environment variables** → Frontend had no way to know ngrok URL

### What We Fixed:

✅ Backend now accepts ngrok CORS requests  
✅ Frontend uses `REACT_APP_API_URL` environment variable  
✅ Production scripts handle build/deploy correctly  
✅ Clear terminal workflow (no more guessing)

---

## 📋 Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] ngrok installed (`choco install ngrok` or download from ngrok.com)
- [ ] ngrok authenticated (`ngrok authtoken YOUR_TOKEN`)
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`cd cctv && npm install`)

---

## 🔥 Production Deployment (Hackathon/Demo Mode)

### **Terminal Layout:**

```
Terminal 1: Backend (FastAPI)
Terminal 2: ngrok Backend Tunnel
Terminal 3: Frontend (React) - Optional if using live dev server
```

---

### **STEP 1: Start Backend** (Terminal 1)

```powershell
# Open PowerShell Terminal 1 in VS Code or external CMD
cd F:\CCTV
.\start_backend.ps1
```

**What happens:**
- FastAPI starts on `0.0.0.0:8000` (accessible from network)
- Backend runs with auto-reload enabled
- **KEEP THIS TERMINAL OPEN** - closing = backend dies

**Verify:**
Open browser → `http://localhost:8000` → Should see JSON response

---

### **STEP 2: Expose Backend via ngrok** (Terminal 2)

```powershell
# Open PowerShell Terminal 2
cd F:\CCTV
.\start_ngrok_backend.ps1
```

**What happens:**
- ngrok creates public tunnel to localhost:8000
- You'll see output like:

```
Forwarding  https://abc123xyz.ngrok-free.app -> http://localhost:8000
```

**⚠️ CRITICAL: COPY THE HTTPS URL IMMEDIATELY**

Example: `https://abc123xyz.ngrok-free.app`

**Verify:**
Open browser → `https://abc123xyz.ngrok-free.app` → Should see same JSON response

**KEEP THIS TERMINAL OPEN** - closing = tunnel dies

---

### **STEP 3: Deploy Frontend** (Two Options)

#### **Option A: Production Build (Recommended for Demos)**

```powershell
# Terminal 3
cd F:\CCTV

# Build frontend with ngrok backend URL
.\deploy_frontend.ps1 -NgrokBackendUrl "https://abc123xyz.ngrok-free.app"
```

**What happens:**
1. Updates `.env.production` with your ngrok backend URL
2. Builds optimized React bundle
3. Creates `cctv/build/` folder

**Serve the build:**

```powershell
# In cctv/ directory
npx serve -s build -p 3000
```

**Access:**
- Localhost: `http://localhost:3000`
- Expose via ngrok: `ngrok http 3000` (in Terminal 4)

---

#### **Option B: Development Server (Quick Testing)**

**If backend = localhost:**

```powershell
cd F:\CCTV
.\start_frontend_dev.ps1
```

**If backend = ngrok:**

1. Edit `cctv/.env`:
```env
REACT_APP_API_URL=https://abc123xyz.ngrok-free.app
```

2. Start dev server:
```powershell
cd F:\CCTV\cctv
npm start
```

**Access:** `http://localhost:3000`

---

## 🌐 Full Remote Access (All Services via ngrok)

For evaluators to access everything remotely:

### **Terminal 1:** Backend
```powershell
.\start_backend.ps1
```

### **Terminal 2:** Backend ngrok
```powershell
.\start_ngrok_backend.ps1
```
→ Copy URL: `https://backend-abc.ngrok-free.app`

### **Terminal 3:** Frontend (production build)
```powershell
.\deploy_frontend.ps1 -NgrokBackendUrl "https://backend-abc.ngrok-free.app"
cd cctv
npx serve -s build -p 3000
```

### **Terminal 4:** Frontend ngrok
```powershell
ngrok http 3000
```
→ Copy URL: `https://frontend-xyz.ngrok-free.app`

**Share with evaluators:** `https://frontend-xyz.ngrok-free.app`

---

## 🐛 Troubleshooting

### **"Failed to fetch" Error**

**Cause:** Frontend calling wrong backend URL

**Fix:**
1. Check browser console → Look for API URL being called
2. Verify `.env` or `.env.production` has correct ngrok URL
3. Restart frontend after changing `.env`
4. Clear browser cache

---

### **"Connection Severed" Error**

**Cause:** Backend or ngrok tunnel died

**Fix:**
1. Check Terminal 1 (backend) → Should show logs
2. Check Terminal 2 (ngrok) → Should show "Session Status: online"
3. If either is closed → restart them
4. Verify ngrok URL didn't change (ngrok free tier assigns new URLs on restart)

---

### **CORS Error**

**Cause:** Backend rejecting frontend's origin

**Fix:**
1. Backend is updated to allow `*.ngrok-free.app`
2. Restart backend if you just updated CORS settings
3. Check browser Network tab → Response headers should include `Access-Control-Allow-Origin`

---

### **ngrok "ERR_NGROK_6024" (Auth Required)**

**Fix:**
```powershell
ngrok authtoken YOUR_AUTH_TOKEN
```

Get token from: https://dashboard.ngrok.com/get-started/your-authtoken

---

### **Backend Crashes on Camera Access**

**Cause:** Camera busy or permission denied

**Fix:**
1. Close other apps using camera (Zoom, Teams, etc.)
2. Check camera permissions in Windows Settings
3. Restart backend

---

## 🚨 Common Mistakes That Cause Failures

### ❌ **WRONG: Running multiple backends**
- Starting backend in multiple terminals
- Old Python processes hanging
- **Fix:** `taskkill /F /IM python.exe` (kill all), then restart

### ❌ **WRONG: Closing terminals during demo**
- Minimize, don't close
- Closing = process dies immediately
- **Fix:** Keep terminals open, move to another desktop if needed

### ❌ **WRONG: Using HTTP when backend is HTTPS**
- ngrok URLs are always HTTPS
- Mixed content errors if frontend is HTTP
- **Fix:** Always use HTTPS ngrok URL in `.env.production`

### ❌ **WRONG: Not updating .env after ngrok restarts**
- ngrok free tier assigns new URLs each restart
- Old URL in `.env` = 404 errors
- **Fix:** Update `.env.production` and rebuild frontend

### ❌ **WRONG: Running backend on localhost only**
- `--host 127.0.0.1` won't work with ngrok
- **Fix:** Always use `--host 0.0.0.0` (already in scripts)

---

## ✅ Pre-Demo Checklist

**15 minutes before evaluation:**

- [ ] Backend running (Terminal 1)
- [ ] ngrok backend tunnel active (Terminal 2)
- [ ] Frontend built with correct ngrok URL
- [ ] Frontend served and accessible (Terminal 3)
- [ ] Optional: Frontend ngrok tunnel (Terminal 4)
- [ ] Links tested in incognito browser
- [ ] Camera permissions granted
- [ ] No other apps using camera
- [ ] Battery/AC power connected
- [ ] Internet connection stable

---

## 🎬 Demo Day Workflow

### **Morning Setup (30 min before):**

1. Open 3-4 terminals (PowerShell or CMD)
2. Start backend → Wait for startup logs
3. Start ngrok backend → Copy HTTPS URL
4. Build frontend with ngrok URL
5. Serve frontend
6. Test end-to-end in browser
7. **Keep terminals minimized, not closed**

### **During Demo:**

- Frontend accessible via ngrok or localhost
- Backend logs visible in Terminal 1
- Don't restart anything
- If crash happens → Restart backend + ngrok in order

### **After Demo:**

- Stop services with Ctrl+C
- Terminals stay open → Just stop processes
- Or close all terminals if done

---

## 📊 Expected Behavior

### **Healthy System:**
- Backend logs show "🚀 FastAPI server starting..."
- ngrok shows "Session Status: online"
- Frontend displays video stream
- No CORS errors in browser console

### **Unhealthy System:**
- Backend shows errors/crashes
- ngrok shows "failed to start tunnel"
- Frontend shows "Failed to fetch"
- CORS errors in console

---

## 🔗 Quick Reference

| Service | Local URL | Command |
|---------|-----------|---------|
| Backend | http://localhost:8000 | `.\start_backend.ps1` |
| Frontend Dev | http://localhost:3000 | `.\start_frontend_dev.ps1` |
| Frontend Prod | http://localhost:3000 | `npx serve -s build -p 3000` |
| ngrok Backend | https://*.ngrok-free.app | `.\start_ngrok_backend.ps1` |
| ngrok Frontend | https://*.ngrok-free.app | `ngrok http 3000` |

---

## 💡 Pro Tips

1. **Use Windows Terminal** → Split panes for all terminals in one window
2. **Pin ngrok URLs** → Paid ngrok = static URLs (no rebuild needed)
3. **Use PM2** → Keep processes alive even if terminal closes (overkill for hackathon)
4. **Test early** → Run full setup 1 day before demo
5. **Screenshot working setup** → Reference if things break

---

## 🆘 Emergency Recovery

**If everything breaks 5 minutes before demo:**

```powershell
# Kill all Python processes
taskkill /F /IM python.exe
taskkill /F /IM ngrok.exe

# Restart in order
cd F:\CCTV
.\start_backend.ps1          # Terminal 1
.\start_ngrok_backend.ps1    # Terminal 2 → Copy URL
# Update .env.production with new ngrok URL
.\deploy_frontend.ps1 -NgrokBackendUrl "https://NEW_URL.ngrok-free.app"
cd cctv
npx serve -s build -p 3000   # Terminal 3
```

**Time to recover: 2-3 minutes**

---

## 📞 Debug Commands

```powershell
# Check if backend is running
curl http://localhost:8000

# Check if ngrok is running
curl https://YOUR_NGROK_URL.ngrok-free.app

# Check frontend build env variables
cat cctv\.env.production

# View backend logs
# (Just look at Terminal 1)

# Kill specific process by port
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 🎯 Final Advice

**Do this once, test thoroughly, then DON'T TOUCH IT before demo.**

The setup is now production-grade. The scripts handle everything. Your only job is:

1. Run scripts in order
2. Keep terminals open
3. Copy/paste ngrok URL correctly

If you follow this guide, your demo will be bulletproof. Good luck! 🚀
