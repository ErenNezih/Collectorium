"""
Passenger WSGI Entry Point for Collectorium
cPanel/CloudLinux + Passenger WSGI Configuration
Production-Ready Version
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
# ENVIRONMENT CONFIGURATION
# =============================================================================

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.hosting')

# =============================================================================
# MYSQL BOOTSTRAP (PyMySQL fallback)
# =============================================================================

# Import MySQL bootstrap for mysqlclient fallback support
try:
    from project_bootstrap_mysql import *  # noqa
except ImportError:
    pass  # Bootstrap not critical, will use mysqlclient if available

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