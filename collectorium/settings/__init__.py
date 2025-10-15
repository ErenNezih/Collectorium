"""
Django settings package initialization.

Based on DJANGO_SETTINGS_MODULE environment variable, 
the appropriate settings file will be loaded:
- dev: Development settings (local development)
- stage: Staging settings (pre-production testing)
- prod: Production settings (live environment)

Default: dev
"""

import os

# Determine which settings to use
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'dev')

if DJANGO_ENV == 'prod':
    from .prod import *  # noqa
elif DJANGO_ENV == 'stage':
    from .stage import *  # noqa
else:
    from .dev import *  # noqa

