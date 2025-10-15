"""
Render.com Production Settings for Collectorium.
Optimized for Render deployment with full production security.
"""

from .base import *
import os
import dj_database_url
import re

# ============================================================================
# SECURITY
# ============================================================================

# Production mode - never enable DEBUG
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = [
    '.onrender.com',
    'collectorium.onrender.com',
]

# Get Render service URL if available
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# Security headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ============================================================================
# DATABASE - PostgreSQL
# ============================================================================

# Render provides DATABASE_URL automatically via Blueprint
DATABASE_URL = os.environ.get('DATABASE_URL', '')

if DATABASE_URL:
    # Clean URL (remove any query parameters for dj-database-url)
    clean_url = DATABASE_URL.split('?')[0] if '?' in DATABASE_URL else DATABASE_URL
    
    try:
        # Primary method: use dj-database-url
        DATABASES = {
            'default': dj_database_url.parse(
                clean_url,
                conn_max_age=600,
                conn_health_checks=True,
                ssl_require=False,
            )
        }
    except Exception as parse_error:
        # Fallback: manual PostgreSQL parsing
        # Format: postgresql://user:pass@host:port/dbname
        match = re.match(
            r'postgres(?:ql)?://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/(.+)',
            clean_url
        )
        if match:
            user, password, host, port, dbname = match.groups()
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': dbname,
                    'USER': user,
                    'PASSWORD': password,
                    'HOST': host,
                    'PORT': port or '5432',
                    'CONN_MAX_AGE': 600,
                    'OPTIONS': {
                        'connect_timeout': 10,
                    }
                }
            }
        else:
            raise ValueError(f'Cannot parse DATABASE_URL. Format should be postgresql://user:pass@host:port/dbname. Error: {parse_error}')
else:
    raise ValueError('DATABASE_URL environment variable is required for production!')

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================

# Static files - WhiteNoise configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================================================
# EMAIL (Console backend for now)
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================================
# LOGGING
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================================================
# PRODUCTION OPTIMIZATIONS
# ============================================================================

# Remove debug toolbar
INSTALLED_APPS = [app for app in INSTALLED_APPS if 'debug_toolbar' not in app]
MIDDLEWARE = [mw for mw in MIDDLEWARE if 'debug_toolbar' not in mw]

# Template caching (APP_DIRS must be False when custom loaders are set)
TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['loaders'] = [
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
    ),
]

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False

# Connection pooling
CONN_MAX_AGE = 600

