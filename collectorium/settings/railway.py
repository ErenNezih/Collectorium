"""
Railway Production Settings for Collectorium.
Optimized for Railway deployment with full production security.
"""

from .base import *
import os
import dj_database_url

# ============================================================================
# SECURITY
# ============================================================================

# CRITICAL: Never enable DEBUG in production
DEBUG = False

# Railway automatically provides domain
RAILWAY_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL', '')

# Allowed hosts - Railway domains
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS = [
        RAILWAY_DOMAIN,
        f'*.{RAILWAY_DOMAIN}',
        '*.up.railway.app',
        '*.railway.app',
    ]
else:
    ALLOWED_HOSTS = ['*.up.railway.app', '*.railway.app']

# CSRF trusted origins
if RAILWAY_DOMAIN:
    CSRF_TRUSTED_ORIGINS = [
        f'https://{RAILWAY_DOMAIN}',
        f'https://*.{RAILWAY_DOMAIN}',
        'https://*.up.railway.app',
        'https://*.railway.app',
    ]
else:
    CSRF_TRUSTED_ORIGINS = ['https://*.up.railway.app', 'https://*.railway.app']

# ============================================================================
# DATABASE - PostgreSQL (Railway provides this automatically)
# ============================================================================

# Railway sets DATABASE_URL automatically
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=False,  # Railway handles SSL internally
        )
    }
    # Ensure proper charset for Django
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
    }
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

# Additional static file finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# ============================================================================
# CACHE - Railway Redis (optional)
# ============================================================================

if redis_url := os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': redis_url,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# ============================================================================
# EMAIL
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================================================
# SECURITY HEADERS
# ============================================================================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

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
}

# ============================================================================
# PRODUCTION OPTIMIZATIONS
# ============================================================================

# Remove debug toolbar and development tools
INSTALLED_APPS = [app for app in INSTALLED_APPS if 'debug_toolbar' not in app]
MIDDLEWARE = [mw for mw in MIDDLEWARE if 'debug_toolbar' not in mw]

# Template caching
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Session engine - database backend for Railway
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False

# Connection pooling
CONN_MAX_AGE = 600

