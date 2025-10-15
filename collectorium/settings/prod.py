"""
Production settings - Live environment

Usage:
    export DJANGO_SETTINGS_MODULE=collectorium.settings.prod
    export DJANGO_ENV=prod

CRITICAL SETTINGS:
- DEBUG must be False
- SECRET_KEY must be set in environment
- DATABASE_URL must be set
- ALLOWED_HOSTS must be configured
"""

from .base import *  # noqa
import dj_database_url
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Hosts/domain names that are valid for this site
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Ensure ALLOWED_HOSTS is set
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError('ALLOWED_HOSTS must be set in production')

# Database - PostgreSQL required for production
if database_url := os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    raise ValueError('DATABASE_URL must be set in production')

# Email - SMTP required
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@collectorium.com')

if not all([EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD]):
    import warnings
    warnings.warn('Email settings not fully configured')

# Cache - Redis recommended for production
if redis_url := os.environ.get('REDIS_URL'):
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
    # Fallback to local memory (not recommended for production)
    import warnings
    warnings.warn('Redis cache not configured. Using local memory cache.')
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Security Settings - STRICT for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Additional security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF trusted origins - MUST be set in production
if csrf_origins := os.environ.get('CSRF_TRUSTED_ORIGINS'):
    CSRF_TRUSTED_ORIGINS = csrf_origins.split(',')
else:
    raise ValueError('CSRF_TRUSTED_ORIGINS must be set in production')

# Static files - WhiteNoise compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files - Use cloud storage in production (AWS S3, Cloudinary, etc.)
# This should be configured based on STORAGE_BACKEND env var
if os.environ.get('STORAGE_BACKEND') == 's3':
    # AWS S3 configuration (install django-storages)
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    # AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    # AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'eu-central-1')
    pass

# Logging - Production logging (ERROR level)
LOGGING['root']['level'] = 'ERROR'
LOGGING['loggers']['django']['level'] = 'ERROR'

# Add file logging for production
LOGGING['handlers']['file'] = {
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': BASE_DIR / 'logs' / 'collectorium.log',
    'maxBytes': 1024 * 1024 * 10,  # 10 MB
    'backupCount': 5,
    'formatter': 'verbose',
}
LOGGING['root']['handlers'].append('file')

# Sentry error tracking (if configured)
if sentry_dsn := os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment='production',
    )

# Ensure logs directory exists
(BASE_DIR / 'logs').mkdir(exist_ok=True)

# Admin security - Limit admin access by IP (optional)
# ADMIN_ALLOWED_IPS = os.environ.get('ADMIN_ALLOWED_IPS', '').split(',')

