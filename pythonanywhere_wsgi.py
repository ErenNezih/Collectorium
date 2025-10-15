"""
WSGI config for Collectorium on PythonAnywhere.

Bu dosyayı PythonAnywhere Web tab'ındaki WSGI file'a kopyalayın.
"""

import os
import sys

# ============================================================================
# BURAYA PYTHONANYWHERE KULLANICI ADINIZI YAZIN!
# Örnek: 'erennezih' veya 'collectorium' gibi
# ============================================================================
PYTHONANYWHERE_USERNAME = 'erennezih'  # <-- BURASI ÖNEMLİ! Kendi username'inizi yazın

# Add project directory to Python path
project_path = f'/home/{PYTHONANYWHERE_USERNAME}/Collectorium'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'collectorium.settings.base'
os.environ['DJANGO_ENV'] = 'production'

# Activate virtual environment
venv_path = f'/home/{PYTHONANYWHERE_USERNAME}/.virtualenvs/collectorium-env/bin/activate_this.py'
try:
    with open(venv_path) as f:
        exec(f.read(), {'__file__': venv_path})
except FileNotFoundError:
    pass  # Will be created during setup

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(project_path, '.env.pythonanywhere')
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not required if env vars set elsewhere

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

