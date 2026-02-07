# Frontend Production Build & Deploy Script
# Use this for hackathon/demo when using ngrok

param(
    [Parameter(Mandatory=$true)]
    [string]$NgrokBackendUrl
)

Write-Host "🏗️  Building Frontend for Production..." -ForegroundColor Cyan
Write-Host "Backend URL: $NgrokBackendUrl" -ForegroundColor Yellow

# Navigate to frontend directory
Set-Location "$PSScriptRoot\cctv"

# Update .env.production with ngrok backend URL
$envContent = "REACT_APP_API_URL=$NgrokBackendUrl"
$envContent | Out-File -FilePath ".env.production" -Encoding utf8 -Force
Write-Host "✅ Updated .env.production" -ForegroundColor Green

# Build production bundle
Write-Host "📦 Building optimized production bundle..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build complete! Artifacts in: cctv\build\" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
    Write-Host "   Option 1: Serve locally and expose via ngrok" -ForegroundColor White
    Write-Host "   Run: npx serve -s build -p 3000" -ForegroundColor Gray
    Write-Host "   Then: ngrok http 3000" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   Option 2: Deploy to hosting (Vercel/Netlify)" -ForegroundColor White
    Write-Host "   Upload the 'build' folder to your hosting provider" -ForegroundColor Gray
} else {
    Write-Host "❌ Build failed!" -ForegroundColor Red
}
