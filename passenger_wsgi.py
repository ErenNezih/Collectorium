"""
Passenger WSGI Entry Point for Collectorium
cPanel/CloudLinux + Passenger WSGI Configuration
DEBUG VERSION - Environment Variables Logging
"""

import os
import sys
from dotenv import load_dotenv

# =============================================================================
# HATA AYIKLAMA KODU - ORTAM DEĞİŞKENLERİ LOG DOSYASI
# =============================================================================

# Passenger'ın gördüğü tüm ortam değişkenlerini logla
debug_log_path = '/home/collecto/collectorium/passenger_env.log'
with open(debug_log_path, 'w') as f:
    f.write("=== PASSENGER ORTAM DEĞİŞKENLERİ LOG DOSYASI ===\n")
    f.write(f"Python Version: {sys.version}\n")
    f.write(f"Current Directory: {os.path.dirname(os.path.abspath(__file__))}\n")
    f.write(f"Python Path: {sys.path}\n\n")
    f.write("=== ORTAM DEĞİŞKENLERİ ===\n")
    for key, value in os.environ.items():
        f.write(f"{key}: {value}\n")
    f.write("\n=== KRİTİK DEĞİŞKENLER KONTROLÜ ===\n")
    f.write(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT_SET')}\n")
    f.write(f"SECRET_KEY: {os.environ.get('SECRET_KEY', 'NOT_SET')[:10]}...\n")
    f.write(f"DB_ENGINE: {os.environ.get('DB_ENGINE', 'NOT_SET')}\n")
    f.write(f"DB_NAME: {os.environ.get('DB_NAME', 'NOT_SET')}\n")
    f.write(f"DB_USER: {os.environ.get('DB_USER', 'NOT_SET')}\n")
    f.write(f"DB_HOST: {os.environ.get('DB_HOST', 'NOT_SET')}\n")
    f.write(f"DEBUG: {os.environ.get('DEBUG', 'NOT_SET')}\n")
    f.write(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'NOT_SET')}\n")

# =============================================================================
# HARDCODED ENVIRONMENT VARIABLES - 503 ERROR ÇÖZÜMÜ
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
    # .env dosyası yoksa, HARDCODED environment variables kullan
    with open('/home/collecto/collectorium/env_loaded.log', 'w') as f:
        f.write(f".env dosyasi bulunamadi: {env_path}\n")
        f.write("HARDCODED environment variables kullaniliyor.\n")
    
    # HARDCODED ENVIRONMENT VARIABLES - 503 ERROR ÇÖZÜMÜ
    os.environ['DJANGO_SETTINGS_MODULE'] = 'collectorium.settings.hosting'
    os.environ['SECRET_KEY'] = '8%!f93#asd!j0we0'
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = 'collectorium.com.tr,www.collectorium.com.tr'
    os.environ['CSRF_TRUSTED_ORIGINS'] = 'https://collectorium.com.tr,https://www.collectorium.com.tr'
    os.environ['DB_ENGINE'] = 'django.db.backends.mysql'
    os.environ['DB_NAME'] = 'collecto_collectorium_db'
    os.environ['DB_USER'] = 'collecto_eren_collectorium_db'
    os.environ['DB_PASSWORD'] = '1e2r3e4n5555'
    os.environ['DB_HOST'] = 'localhost'
    
    # Debug: Hardcoded variables'ları logla
    with open('/home/collecto/collectorium/hardcoded_env.log', 'w') as f:
        f.write("=== HARDCODED ENVIRONMENT VARIABLES ===\n")
        f.write(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}\n")
        f.write(f"SECRET_KEY: {os.environ.get('SECRET_KEY')[:10]}...\n")
        f.write(f"DB_ENGINE: {os.environ.get('DB_ENGINE')}\n")
        f.write(f"DB_NAME: {os.environ.get('DB_NAME')}\n")
        f.write(f"DB_USER: {os.environ.get('DB_USER')}\n")
        f.write(f"DB_HOST: {os.environ.get('DB_HOST')}\n")
        f.write(f"DEBUG: {os.environ.get('DEBUG')}\n")
        f.write(f"ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS')}\n")

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

