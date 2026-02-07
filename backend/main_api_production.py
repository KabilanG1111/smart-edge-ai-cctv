# Production Backend (FastAPI serving React build)
# This version runs on Render without camera/AI dependencies

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import time

app = FastAPI(title="Smart CCTV System (Demo Mode)")

# CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine if running in demo mode (production) or full mode (local)
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
print(f"🚀 Starting in {'DEMO' if DEMO_MODE else 'FULL'} mode")

# API Routes (with /api prefix)
@app.get("/api/")
def root():
    """Health check endpoint"""
    return {
        "service": "Smart Edge-AI CCTV System",
        "version": "1.0.0",
        "mode": "demo" if DEMO_MODE else "full",
        "status": "online"
    }

@app.get("/api/status")
def get_status():
    """Get current system status"""
    if DEMO_MODE:
        return {
            "streaming": False,
            "camera_active": False,
            "ai_status": "DEMO_MODE",
            "mode": "demo",
            "message": "This is a demo deployment. Camera features disabled on cloud."
        }
    # Full mode status would go here
    return {"status": "full mode not implemented in production"}

@app.post("/api/start")
def start_camera():
    """Start camera endpoint (demo mode returns mock response)"""
    if DEMO_MODE:
        return {
            "status": "success",
            "mode": "demo",
            "message": "Demo mode: Camera simulation started",
            "note": "Live camera unavailable on cloud deployment"
        }
    return {"error": "Full mode requires local deployment"}

@app.get("/api/live")
def live_feed():
    """MJPEG stream endpoint (demo mode returns mock frames)"""
    if DEMO_MODE:
        def generate_demo_frame():
            # Return a simple mock frame for demo
            yield (
                b"--frame\r\n"
                b"Content-Type: text/plain\r\n\r\n"
                b"Demo mode: Live camera feed requires local deployment\r\n"
            )
        
        return StreamingResponse(
            generate_demo_frame(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
    return {"error": "Full mode requires local deployment"}

@app.post("/api/stop")
def stop_camera():
    """Stop camera endpoint"""
    return {
        "status": "stopped",
        "mode": "demo" if DEMO_MODE else "full",
        "message": "Camera stopped"
    }

@app.get("/api/intelligence")
def get_intelligence_status():
    """Get Intelligence Layer status"""
    if DEMO_MODE:
        return {
            "mode": "demo",
            "status": "OFFLINE",
            "message": "AI features require local deployment with GPU"
        }
    return {"error": "Full mode requires local deployment"}

# Serve React build (frontend)
# Mount static files LAST so API routes take precedence
frontend_build_path = Path(__file__).parent / "cctv" / "build"

if frontend_build_path.exists():
    # Serve static files (JS, CSS, images)
    app.mount("/static", StaticFiles(directory=frontend_build_path / "static"), name="static")
    
    # Serve index.html for all non-API routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        """Serve React app for all non-API routes"""
        # Don't interfere with API routes
        if full_path.startswith("api/"):
            return JSONResponse({"error": "Not found"}, status_code=404)
        
        index_file = frontend_build_path / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({"error": "Frontend not built"}, status_code=404)
else:
    @app.get("/")
    async def no_frontend():
        return {
            "error": "Frontend not built",
            "message": "Run 'npm run build' in cctv/ directory",
            "api_docs": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
