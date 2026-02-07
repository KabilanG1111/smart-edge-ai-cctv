# 🎯 HACKATHON DEPLOYMENT CHECKLIST

## Pre-Deployment (Do This First)

- [ ] Test React build locally: `cd cctv && npm run build`
- [ ] Test production backend: `python backend\main_api_production.py`
- [ ] Verify http://localhost:8000 shows frontend
- [ ] Verify http://localhost:8000/api/ returns JSON

## Git Setup

- [ ] Create GitHub repository
- [ ] Run: `git init`
- [ ] Run: `git add .`
- [ ] Run: `git commit -m "Production deployment"`
- [ ] Run: `git remote add origin YOUR_REPO_URL`
- [ ] Run: `git push -u origin main`

## Render Deployment

- [ ] Sign up at https://render.com (use GitHub login)
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Configure:
  - **Build Command:** `bash build.sh`
  - **Start Command:** `uvicorn backend.main_api_production:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variable: `DEMO_MODE=true`
- [ ] Click "Create Web Service"
- [ ] Wait 5-10 minutes for deployment

## Verification

- [ ] Open: `https://your-app.onrender.com`
- [ ] Frontend loads correctly
- [ ] Test: `https://your-app.onrender.com/api/`
- [ ] Test: `https://your-app.onrender.com/api/status`
- [ ] No console errors (F12 → Console tab)
- [ ] Works on mobile
- [ ] Test in incognito mode

## Submission

- [ ] Copy deployment URL
- [ ] Test URL one final time
- [ ] Prepare submission email/form:
  ```
  Project: Smart CCTV System
  URL: https://your-app.onrender.com
  GitHub: https://github.com/yourusername/repo
  Tech: React, FastAPI, Python
  
  Note: Demo deployment. Full features require local setup.
  ```
- [ ] Submit to hackathon

## Backup Plan (If Render Fails)

- [ ] Keep local deployment running
- [ ] Use ngrok: `ngrok http 8000`
- [ ] Submit ngrok URL
- [ ] Keep laptop awake during judging

---

**Total Time: 30-45 minutes**

**Questions? Check RENDER_DEPLOYMENT.md for detailed instructions**
