"""
cPanel/Passenger Production Settings for Collectorium

This settings file is specifically configured for cPanel shared hosting
with Passenger WSGI application server.

Environment: Production (cPanel/CloudLinux)
WSGI Server: Passenger
Web Server: Apache

Usage:
    export DJANGO_SETTINGS_MODULE=collectorium.settings.hosting

CRITICAL SETTINGS:
- DEBUG must be False
- SECRET_KEY must be set in environment
- DATABASE_URL must be set (PostgreSQL or MySQL)
- ALLOWED_HOSTS must be configured
- CSRF_TRUSTED_ORIGINS must be configured
"""

from .base import *  # noqa
import os

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hosts/domain names that are valid for this site
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    ALLOWED_HOSTS = ['collectorium.com.tr', 'www.collectorium.com.tr']

# CSRF trusted origins
if csrf_origins := os.environ.get('CSRF_TRUSTED_ORIGINS'):
    CSRF_TRUSTED_ORIGINS = csrf_origins.split(',')
else:
    CSRF_TRUSTED_ORIGINS = ['https://collectorium.com.tr', 'https://www.collectorium.com.tr']

# SSL/HTTPS Settings
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = False  # Set to True when SSL is ready
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_NAME = 'collectorium_session'

CSRF_COOKIE_SECURE = False  # Set to True when SSL is ready
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_NAME = 'collectorium_csrf'

# Additional security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# =============================================================================
# DATABASE CONFIGURATION - PostgreSQL OR MySQL
# =============================================================================

"""
cPanel supports both PostgreSQL (external) and MySQL (native).
Configuration is done via DATABASE_URL environment variable.

For PostgreSQL (recommended):
    DATABASE_URL=postgresql://user:pass@host:port/dbname

For MySQL (cPanel native):
    DATABASE_URL=mysql://user:pass@localhost:3306/dbname

The DB_ENGINE can also be explicitly set:
    DB_ENGINE=django.db.backends.postgresql
    DB_ENGINE=django.db.backends.mysql
"""

# Get database configuration from environment
database_url = os.environ.get('DATABASE_URL')
db_engine = os.environ.get('DB_ENGINE')

if database_url:
    # Parse DATABASE_URL using dj-database-url
    import dj_database_url
    
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,  # Connection pooling
            conn_health_checks=True,
            ssl_require=False  # cPanel may not require SSL for localhost MySQL
        )
    }
    
    # Override SSL requirement if explicitly set
    if os.environ.get('DB_SSL_REQUIRE', 'false').lower() == 'true':
        DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
    
elif all([
    os.environ.get('DB_NAME'),
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASSWORD'),
]):
    # Manual database configuration
    db_engine = db_engine or 'django.db.backends.postgresql'
    
    DATABASES = {
        'default': {
            'ENGINE': db_engine,
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432' if 'postgresql' in db_engine else '3306'),
            'CONN_MAX_AGE': 600,
        }
    }
    
    # Add database-specific options
    if 'postgresql' in db_engine:
        DATABASES['default']['OPTIONS'] = {
            'connect_timeout': 10,
        }
        if os.environ.get('DB_SSL_REQUIRE', 'false').lower() == 'true':
            DATABASES['default']['OPTIONS']['sslmode'] = 'require'
    
    elif 'mysql' in db_engine:
        DATABASES['default']['OPTIONS'] = {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 10,
        }

else:
    # Fallback to SQLite for development/testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# =============================================================================
# STATIC FILES - WhiteNoise
# =============================================================================

"""
cPanel hosting with Passenger can serve static files via:
1. WhiteNoise (recommended - no configuration needed)
2. Apache (requires .htaccess configuration)

We use WhiteNoise for simplicity and performance.
"""

# Static files configuration
STATIC_URL = '/static/'

# Use staticfiles/ as STATIC_ROOT (WhiteNoise will serve from here)
# This matches Django convention and works well with WhiteNoise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Additional static directories (if any)
# STATICFILES_DIRS is defined in base.py

# =============================================================================
# MEDIA FILES - User Uploads
# =============================================================================

"""
Media files are stored locally on cPanel.
For better performance and scalability, consider using:
- CloudFlare R2
- AWS S3
- DigitalOcean Spaces
- Cloudinary

For now, we use local storage.
"""

MEDIA_URL = '/media/'

# Media root - use standard 'media' directory
# cPanel/Apache can serve this via proper configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB

# =============================================================================
# EMAIL CONFIGURATION - SMTP
# =============================================================================

"""
Email configuration for cPanel hosting.
Supports:
- cPanel email (localhost SMTP)
- External SMTP (Gmail, SendGrid, etc.)
"""

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Email server settings
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() == 'true'

# Email authentication
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Email addresses
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@collectorium.com')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# Warn if email is not fully configured
if not all([EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD]) and EMAIL_HOST != 'localhost':
    import warnings
    warnings.warn(
        'Email configuration is incomplete. '
        'Set EMAIL_HOST, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD environment variables.'
    )

# =============================================================================
# CACHING - Local Memory (Redis/Memcached optional)
# =============================================================================

"""
Caching configuration for cPanel.
Default: Local memory cache (suitable for small sites)
Optional: Redis/Memcached (if available on cPanel)
"""

if redis_url := os.environ.get('REDIS_URL'):
    # Redis cache (if available)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': redis_url,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'collectorium',
            'TIMEOUT': 300,
        }
    }
else:
    # Local memory cache (default for cPanel)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'collectorium-cache',
        }
    }

# =============================================================================
# LOGGING - File and Console
# =============================================================================

"""
Logging configuration for cPanel hosting.
Logs are written to:
- Console (stderr - captured by Passenger)
- File (~/logs/django.log)
"""

# Ensure logs directory exists
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'error.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': os.environ.get('LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# =============================================================================
# SENTRY ERROR TRACKING (Optional)
# =============================================================================

if sentry_dsn := os.environ.get('SENTRY_DSN'):
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[DjangoIntegration()],
            traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
            send_default_pii=False,
            environment=os.environ.get('SENTRY_ENVIRONMENT', 'production'),
        )
    except ImportError:
        import warnings
        warnings.warn('Sentry SDK not installed. Install with: pip install sentry-sdk')

# =============================================================================
# PERFORMANCE OPTIMIZATIONS
# =============================================================================

# Template caching (for production)
if not DEBUG:
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

# Database connection settings
CONN_MAX_AGE = 600  # 10 minutes

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = False

# =============================================================================
# ADMIN CUSTOMIZATION (Optional)
# =============================================================================

# Optional: Change admin URL for security
# Update urls.py if using custom admin URL
# ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/')

# Optional: Limit admin access by IP
# ADMIN_ALLOWED_IPS = os.environ.get('ADMIN_ALLOWED_IPS', '').split(',')

# =============================================================================
# DEPLOYMENT VERIFICATION
# =============================================================================

# Verify critical settings are configured
_critical_settings = {
    'SECRET_KEY': bool(SECRET_KEY and SECRET_KEY != 'django-insecure-default'),
    'ALLOWED_HOSTS': bool(ALLOWED_HOSTS and ALLOWED_HOSTS != ['']),
    'CSRF_TRUSTED_ORIGINS': bool(CSRF_TRUSTED_ORIGINS),
    'DATABASE': bool(DATABASES.get('default')),
}

# Log missing settings instead of raising error
if not all(_critical_settings.values()):
    missing = [k for k, v in _critical_settings.items() if not v]
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f'Some settings not configured: {", ".join(missing)}')

# =============================================================================
# ENVIRONMENT INFO (for health checks)
# =============================================================================

DEPLOYMENT_INFO = {
    'environment': 'production',
    'hosting': 'cpanel',
    'wsgi': 'passenger',
    'database': DATABASES['default']['ENGINE'].split('.')[-1],
    'cache': CACHES['default']['BACKEND'].split('.')[-1],
}

