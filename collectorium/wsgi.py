"""
WSGI config for collectorium project.

Optimized for Railway deployment.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collectorium.settings.railway')

# Initialize Django application
application = get_wsgi_application()
