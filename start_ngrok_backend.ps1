# ngrok Backend Tunnel Script
# Run this AFTER backend is running
# Keep this terminal open during demo

Write-Host "🌐 Starting ngrok tunnel for backend..." -ForegroundColor Cyan

# Start ngrok for backend
Write-Host "🔗 Exposing localhost:8000 via ngrok..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  COPY THE HTTPS URL SHOWN BELOW" -ForegroundColor Red
Write-Host "   Update .env.production with: REACT_APP_API_URL=<ngrok_url>" -ForegroundColor Yellow
Write-Host ""

ngrok http 8000

Write-Host "❌ ngrok tunnel closed" -ForegroundColor Red
