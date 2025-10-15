"""
PythonAnywhere Production Settings for Collectorium.

Bu settings dosyası PythonAnywhere'e özel optimize edilmiştir.
"""

from .base import *
import os
import dj_database_url

# ============================================================================
# SECURITY
# ============================================================================

DEBUG = False

# Allowed hosts - PythonAnywhere subdomain
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.pythonanywhere.com').split(',')

# CSRF
CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS',
    'https://*.pythonanywhere.com'
).split(',')

# ============================================================================
# DATABASE - MySQL
# ============================================================================

# PythonAnywhere MySQL database configuration
if os.environ.get('DATABASE_URL'):
    # Use DATABASE_URL if provided
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ['DATABASE_URL'],
            conn_max_age=600,
        )
    }
else:
    # Manual MySQL configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', ''),
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', ''),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================

# Static files (WhiteNoise already configured in base.py)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================================================
# CACHE - Local Memory (PythonAnywhere free plan)
# ============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'collectorium-cache',
    }
}

# ============================================================================
# EMAIL - Console Backend (for testing)
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Gerçek email göndermek için (opsiyonel):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# ============================================================================
# SECURITY HEADERS
# ============================================================================

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# SSL - PythonAnywhere handles this
SECURE_SSL_REDIRECT = False  # PythonAnywhere already redirects
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ============================================================================
# LOGGING - PythonAnywhere
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'collectorium.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Ensure logs directory exists
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

# ============================================================================
# MIDDLEWARE - Remove Debug Toolbar
# ============================================================================

# Debug Toolbar'ı production'da kaldır
if 'debug_toolbar.middleware.DebugToolbarMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('debug_toolbar.middleware.DebugToolbarMiddleware')

if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')

