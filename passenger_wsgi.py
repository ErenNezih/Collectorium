"""
Passenger WSGI Entry Point for Collectorium
cPanel/CloudLinux + Passenger WSGI Configuration
Production-Ready Version with .env Support
"""

import os
import sys
from dotenv import load_dotenv

# =============================================================================
# ENVIRONMENT CONFIGURATION - .env DOSYASI DESTEĞİ
# =============================================================================

# Proje dizininin yolunu belirle
project_directory = os.path.dirname(os.path.abspath(__file__))

# .env dosyasını bul ve içindeki değişkenleri yükle
env_path = os.path.join(project_directory, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    # Debug: .env dosyasının yüklendiğini logla
    with open('/home/collecto/collectorium/env_loaded.log', 'w') as f:
        f.write(f".env dosyasi yuklendi: {env_path}\n")
        f.write(f"DB_ENGINE: {os.environ.get('DB_ENGINE', 'NOT_SET')}\n")
        f.write(f"DB_NAME: {os.environ.get('DB_NAME', 'NOT_SET')}\n")
        f.write(f"SECRET_KEY: {os.environ.get('SECRET_KEY', 'NOT_SET')[:10]}...\n")
else:
    # .env dosyası yoksa, cPanel environment variables'ları kullan
    with open('/home/collecto/collectorium/env_loaded.log', 'w') as f:
        f.write(f".env dosyasi bulunamadi: {env_path}\n")
        f.write("cPanel environment variables kullaniliyor.\n")

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Add project directory to Python path
if project_directory not in sys.path:
    sys.path.insert(0, project_directory)

# =============================================================================
# MYSQL BOOTSTRAP (PyMySQL fallback)
# =============================================================================

# Import MySQL bootstrap for mysqlclient fallback support
try:
    from project_bootstrap_mysql import *  # noqa
except ImportError:
    pass  # Bootstrap not critical, will use mysqlclient if available

# =============================================================================
# DJANGO SETTINGS MODULE
# =============================================================================

# Set Django settings module (from .env or default)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')

# =============================================================================
# WSGI APPLICATION
# =============================================================================

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # If Django fails to load, create a simple error application
    import traceback
    def application(environ, start_response):
        status = '500 Internal Server Error'
        error_details = f'Error loading Django application: {str(e)}\n\nTraceback:\n{traceback.format_exc()}'
        output = error_details.encode('utf-8')
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(output)))
        ]
        start_response(status, response_headers)
        return [output]

