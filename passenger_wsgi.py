"""
Passenger WSGI Entry Point for Collectorium
cPanel/CloudLinux + Passenger WSGI Configuration
"""

import os
import sys

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

# Get the absolute path to the project directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Add project directory to Python path
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# =============================================================================
# MYSQL BOOTSTRAP (PyMySQL fallback)
# =============================================================================

# Import MySQL bootstrap for mysqlclient fallback support
try:
    from project_bootstrap_mysql import *  # noqa
except ImportError:
    pass  # Bootstrap not critical, will use mysqlclient if available

# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================

# Set Django settings module
# This should match your hosting settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')

# Optional: Load environment variables from .env file
# Uncomment if you're using python-dotenv
# from dotenv import load_dotenv
# load_dotenv(os.path.join(CURRENT_DIR, '.env'))

# =============================================================================
# WSGI APPLICATION
# =============================================================================

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # If Django fails to load, create a simple error application
    # This helps with debugging deployment issues
    def application(environ, start_response):
        status = '500 Internal Server Error'
        output = f'Error loading Django application: {str(e)}'.encode('utf-8')
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(output)))
        ]
        start_response(status, response_headers)
        return [output]

# =============================================================================
# DEBUGGING (Development/Staging Only)
# =============================================================================

# Uncomment for debugging path issues in cPanel
# print("Python version:", sys.version, file=sys.stderr)
# print("Python path:", sys.path, file=sys.stderr)
# print("Current directory:", CURRENT_DIR, file=sys.stderr)
# print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'), file=sys.stderr)

