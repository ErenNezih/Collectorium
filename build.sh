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

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"
