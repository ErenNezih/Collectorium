#!/usr/bin/env bash
# Render Build Script for Collectorium
# Exit on error
set -e

echo "🚀 Starting Collectorium build process..."

# Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Optional frontend build (Tailwind/PostCSS) if a Node pipeline exists
if [ -f "package.json" ]; then
  echo "📦 Installing Node dependencies..."
  if command -v npm >/dev/null 2>&1; then
    npm ci
    echo "🛠 Building frontend assets..."
    npm run build
  else
    echo "⚠️ npm not found; skipping frontend build"
  fi
fi

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"
