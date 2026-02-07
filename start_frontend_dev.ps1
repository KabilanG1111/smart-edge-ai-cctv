# Frontend Startup Script (Local Development)
# For ngrok deployment, use deploy_frontend.ps1 instead

Write-Host "🎨 Starting Frontend (Development Mode)..." -ForegroundColor Cyan

# Navigate to frontend directory
Set-Location "$PSScriptRoot\cctv"

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Start React dev server
Write-Host "🌐 Starting React on localhost:3000..." -ForegroundColor Green
npm start

Write-Host "❌ Frontend stopped" -ForegroundColor Red
