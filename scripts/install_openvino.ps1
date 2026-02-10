# OpenVINO Installation for Windows 11
# Intel CPU-optimized deep learning inference

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenVINO Toolkit Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion" -ForegroundColor Yellow

if ($pythonVersion -notmatch "Python 3\.(9|10|11)") {
    Write-Host "⚠️  Warning: OpenVINO requires Python 3.9-3.11" -ForegroundColor Red
    Write-Host "Your version: $pythonVersion" -ForegroundColor Red
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}

Write-Host ""
Write-Host "📦 Installing OpenVINO toolkit..." -ForegroundColor Cyan

# Activate virtual environment if exists
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
} elseif (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

# Install OpenVINO
Write-Host ""
Write-Host "Installing openvino..." -ForegroundColor Green
python -m pip install --upgrade pip
python -m pip install openvino openvino-dev

# Install dependencies
Write-Host ""
Write-Host "Installing additional dependencies..." -ForegroundColor Green
python -m pip install numpy opencv-python pyyaml

# Verify installation
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Verifying Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$verification = python -c "from openvino.runtime import Core; print('OpenVINO version:', Core().get_versions('CPU')['CPU'].description)" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ OpenVINO installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "OpenVINO Info:" -ForegroundColor Yellow
    Write-Host $verification
    Write-Host ""
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Next Steps" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Export YOLOv8 to ONNX:" -ForegroundColor Yellow
    Write-Host "   python scripts/export_to_onnx.py --model yolov8n.pt --imgsz 320" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Convert ONNX to OpenVINO IR:" -ForegroundColor Yellow
    Write-Host "   mo --input_model yolov8n.onnx --output_dir models/openvino --data_type FP16" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Run stable production pipeline:" -ForegroundColor Yellow
    Write-Host "   python -m uvicorn backend.main_api_production:app --host 0.0.0.0 --port 8000" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "❌ OpenVINO installation failed" -ForegroundColor Red
    Write-Host "Error:" -ForegroundColor Red
    Write-Host $verification
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "- Ensure Python 3.9-3.11 is installed" -ForegroundColor White
    Write-Host "- Try: python -m pip install --upgrade pip" -ForegroundColor White
    Write-Host "- Check internet connection" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
