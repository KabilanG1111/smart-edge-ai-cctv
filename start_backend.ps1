# Backend Startup Script (Production-Grade)
# Run this in a dedicated terminal and keep it open

Write-Host "🚀 Starting Backend Server..." -ForegroundColor Cyan

# Navigate to project root
Set-Location $PSScriptRoot

# Activate virtual environment if exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

# Start backend on all interfaces (required for ngrok)
Write-Host "🌐 Starting FastAPI on 0.0.0.0:8000..." -ForegroundColor Green
python -m uvicorn backend.main_api:app --host 0.0.0.0 --port 8000 --reload

# If this script exits, backend has crashed
Write-Host "❌ Backend stopped" -ForegroundColor Red
