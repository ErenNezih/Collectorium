#!/bin/bash
# Linting script for Collectorium

set -e

echo "🔍 Running linting checks..."
echo ""

echo "📝 Checking with ruff..."
ruff check .

echo ""
echo "🎨 Checking formatting with black..."
black --check .

echo ""
echo "📦 Checking import sorting with isort..."
isort --check-only .

echo ""
echo "✅ All linting checks passed!"

