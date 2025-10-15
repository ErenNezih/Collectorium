#!/bin/bash
# Auto-formatting script for Collectorium

set -e

echo "🎨 Formatting code..."
echo ""

echo "📝 Running black..."
black .

echo ""
echo "📦 Running isort..."
isort .

echo ""
echo "🔧 Running ruff with auto-fix..."
ruff check --fix .

echo ""
echo "✅ Code formatting complete!"

