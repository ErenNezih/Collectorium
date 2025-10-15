#!/usr/bin/env bash
# Render Build Script for Collectorium
# This script runs during deployment

set -o errexit  # Exit on error

echo "🚀 Starting Collectorium build process..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

echo "✅ Build completed successfully!"

