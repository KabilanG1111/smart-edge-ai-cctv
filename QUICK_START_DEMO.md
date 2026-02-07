# 🚀 QUICK START - Hackathon Demo
## Copy-Paste Commands (No Thinking Required)

---

## TERMINAL 1: Backend
```powershell
cd F:\CCTV
.\start_backend.ps1
```
**Status:** Should see "🚀 FastAPI server starting..."  
**Keep open!**

---

## TERMINAL 2: ngrok Backend Tunnel
```powershell
cd F:\CCTV
.\start_ngrok_backend.ps1
```
**Status:** Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)  
**Keep open!**

---

## TERMINAL 3: Frontend Production Build
```powershell
cd F:\CCTV

# Replace URL with YOUR ngrok URL from Terminal 2
.\deploy_frontend.ps1 -NgrokBackendUrl "https://abc123.ngrok-free.app"

cd cctv
npx serve -s build -p 3000
```
**Access:** `http://localhost:3000`

---

## TERMINAL 4 (Optional): Frontend ngrok
```powershell
ngrok http 3000
```
**Share this URL** with evaluators: `https://xyz789.ngrok-free.app`

---

## ✅ Verification

- [ ] Terminal 1 shows FastAPI logs
- [ ] Terminal 2 shows "Session Status: online"
- [ ] Terminal 3 serves frontend
- [ ] Browser → `http://localhost:3000` → Works
- [ ] Browser console → No CORS errors

---

## 🐛 Quick Fixes

**"Failed to fetch"**
1. Check `.env.production` has correct ngrok URL
2. Rebuild: `.\deploy_frontend.ps1 -NgrokBackendUrl "https://YOUR_URL.ngrok-free.app"`

**Backend crashed**
1. Terminal 1 → Ctrl+C
2. Rerun: `.\start_backend.ps1`

**ngrok died**
1. Terminal 2 → Rerun script
2. **Update .env.production with NEW URL**
3. Rebuild frontend

---

## 🔥 Nuclear Option (Full Restart)
```powershell
# Kill everything
taskkill /F /IM python.exe
taskkill /F /IM ngrok.exe

# Start fresh
.\start_backend.ps1          # T1
.\start_ngrok_backend.ps1    # T2 → Copy URL
# Update .env.production
.\deploy_frontend.ps1 -NgrokBackendUrl "https://NEW_URL"
cd cctv && npx serve -s build -p 3000  # T3
```
