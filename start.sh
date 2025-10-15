#!/usr/bin/env bash
# Render Start Script for Collectorium
# Exit on error
set -e

echo "🚀 Starting Collectorium..."

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser automatically (non-interactive)
echo "👤 Creating superuser..."
python - <<'PYEOF'
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "collectorium.settings.render"))
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@collectorium.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "ChangeMe!123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser '{username}' created successfully!")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")
PYEOF

echo "🚀 Starting Gunicorn..."
# Start Gunicorn with config
exec gunicorn collectorium.wsgi:application --config gunicorn.conf.py

