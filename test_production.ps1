# Test Production Build Locally

Write-Host "🧪 Testing Production Build Locally..." -ForegroundColor Cyan

# Step 1: Build React frontend
Write-Host "`n📦 Step 1: Building React frontend..." -ForegroundColor Yellow
Set-Location "$PSScriptRoot\cctv"

if (Test-Path "build") {
    Write-Host "Removing old build..." -ForegroundColor Gray
    Remove-Item -Recurse -Force build
}

npm run build

if (-not (Test-Path "build\index.html")) {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Frontend build successful!" -ForegroundColor Green

# Step 2: Test production backend
Write-Host "`n🚀 Step 2: Starting production backend..." -ForegroundColor Yellow
Set-Location $PSScriptRoot

Write-Host "Installing Python dependencies..." -ForegroundColor Gray
pip install -q -r requirements.txt

Write-Host "`n🌐 Starting server on http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:8000" -ForegroundColor White
Write-Host "   API: http://localhost:8000/api/" -ForegroundColor White
Write-Host "   Status: http://localhost:8000/api/status" -ForegroundColor White
Write-Host "`nPress Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

python backend\main_api_production.py
