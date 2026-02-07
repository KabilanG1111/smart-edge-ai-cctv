#!/bin/bash
# Build script for Render deployment

echo "🏗️  Starting build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies and build React app
echo "📦 Installing frontend dependencies..."
cd cctv
npm install --legacy-peer-deps

# Build React production bundle
echo "🔨 Building React frontend..."
npm run build

# Verify build succeeded
if [ -d "build" ]; then
    echo "✅ Frontend build successful!"
    echo "📊 Build size:"
    du -sh build/
else
    echo "❌ Frontend build failed!"
    exit 1
fi

cd ..
echo "✅ Build process complete!"
