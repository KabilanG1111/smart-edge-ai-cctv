# Smart CCTV - Edge AI Surveillance System

🏆 **Hackathon Project:** Intelligent CCTV system with real-time AI detection and behavioral analysis.

## 🚀 Live Demo

**Production Deployment:** [https://your-app.onrender.com](https://your-app.onrender.com)

> **Note:** Demo deployment runs without live camera. Full features require local setup with camera hardware.

---

## ✨ Features

- 🎥 **Real-time Video Streaming** - Live camera feed with MJPEG streaming
- 🤖 **AI-Powered Detection** - YOLO-based object and anomaly detection  
- 🧠 **Behavioral Analysis** - Cognitive state tracking and baseline learning
- ⚡ **Edge Processing** - 100% local processing, no cloud uploads
- 🎨 **Modern UI** - React-based responsive interface
- 📊 **Intelligence Dashboard** - Real-time system metrics and alerts

## 🛠️ Tech Stack

### Frontend
- **React 19** - Modern UI framework
- **Framer Motion** - Smooth animations
- **React Router** - SPA navigation

### Backend
- **FastAPI** - High-performance Python API
- **OpenCV** - Computer vision processing
- **Ultralytics YOLO** - Object detection models
- **PyTorch** - Deep learning inference

### Deployment
- **Render** - Cloud platform (demo mode)
- **Local** - Full features with camera hardware

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 16+
- Webcam (for local deployment)

### Local Setup (Full Features)

```bash
# Clone repository
git clone https://github.com/yourusername/smart-cctv.git
cd smart-cctv

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd cctv
npm install

# Start backend
cd ..
python -m uvicorn backend.main_api:app --host 0.0.0.0 --port 8000

# Start frontend (new terminal)
cd cctv
npm start
```

Access at: **http://localhost:3000**

---

## 🌐 Production Deployment

### Quick Deploy to Render

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Render:**
   - Sign up at [render.com](https://render.com)
   - New Web Service → Connect GitHub repo
   - Build: `bash build.sh`
   - Start: `uvicorn backend.main_api_production:app --host 0.0.0.0 --port $PORT`
   - Add env: `DEMO_MODE=true`

3. **Access:** `https://your-app.onrender.com`

**Detailed guide:** [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

---

## 🎮 Usage

### Local Development

**Terminal 1: Backend**
```bash
python -m uvicorn backend.main_api:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2: Frontend**
```bash
cd cctv
npm start
```

### Production Testing

```bash
.\test_production.ps1
```

---

## 📁 Project Structure

```
cctv-system/
├── backend/
│   ├── main_api.py              # Local development API
│   └── main_api_production.py   # Production API (demo mode)
├── cctv/                         # React frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LiveStream.js    # Main streaming interface
│   │   │   ├── AICopilot.js     # AI assistant
│   │   │   └── EvidenceVault.js # Recorded clips
│   │   └── components/
│   └── public/
├── core/                         # AI processing modules
│   ├── ai_pipeline.py           # Main AI pipeline
│   ├── behavior_analyzer.py     # Behavioral analysis
│   ├── intelligence_layer.py    # Cognitive reasoning
│   └── camera_lifecycle_manager.py
├── config/
│   └── settings.py              # Configuration
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render config
└── build.sh                     # Build script

```

---

## 🔧 API Endpoints

### Health
- `GET /api/` - Service status

### Camera Control
- `POST /api/start` - Start camera stream
- `POST /api/stop` - Stop camera stream
- `GET /api/live` - MJPEG video stream

### System Status
- `GET /api/status` - Current system state
- `GET /api/intelligence` - AI layer metrics

---

## 🧪 Testing

### Test Production Build
```bash
# Windows
.\test_production.ps1

# Linux/Mac
bash build.sh
python backend/main_api_production.py
```

### Test Local Development
```bash
# Backend
python test_integration.py

# Frontend
cd cctv
npm test
```

---

## 🚧 Development vs Production

| Feature | Local Development | Production (Demo) |
|---------|------------------|-------------------|
| Camera Access | ✅ Real webcam | ❌ Not available |
| AI Detection | ✅ YOLO models | ❌ Mock responses |
| Video Streaming | ✅ Live feed | ⚠️ Demo message |
| API Endpoints | ✅ Full features | ✅ Working |
| UI | ✅ Complete | ✅ Complete |
| Performance | High (local GPU) | Limited (free tier) |

---

## 🐛 Troubleshooting

### Camera not opening
```bash
# Check camera permissions
# Close other apps using camera (Zoom, Teams, etc.)
```

### Port already in use
```bash
# Kill process on port 8000
taskkill /F /IM python.exe  # Windows
lsof -ti:8000 | xargs kill   # Linux/Mac
```

### Build errors
```bash
# Clear caches
cd cctv
rm -rf node_modules build
npm install
npm run build
```

---

## 📝 Environment Variables

### Local Development (`.env`)
```env
# Automatically proxied - no setup needed
```

### Production (Render)
```env
DEMO_MODE=true
PYTHON_VERSION=3.11.0
```

---

## 🎯 Hackathon Submission

**Project Name:** Smart CCTV - Edge AI Surveillance  
**Category:** AI/ML, Computer Vision, IoT  
**Deployment:** https://your-app.onrender.com  
**Repository:** https://github.com/yourusername/smart-cctv  

**Demo Notes:**
- Production demo runs without camera hardware
- Full system requires local deployment with webcam
- All source code and documentation included
- Setup time: ~15 minutes for local deployment

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 👥 Team

- **Your Name** - Full Stack Development, AI Integration
- [GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Ultralytics YOLO](https://ultralytics.com/) - Object detection models
- [React](https://react.dev/) - Frontend framework
- [Render](https://render.com/) - Cloud deployment platform

---

**Built with ❤️ for [Hackathon Name] 2026**
