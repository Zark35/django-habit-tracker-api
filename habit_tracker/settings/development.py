"""
Development settings for habit_tracker project.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Optional development apps
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Debug toolbar allowed IPs
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
]

# Disable SSL redirect in development
SECURE_SSL_REDIRECT = False

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Database logging
LOGGING['loggers'] = {
    'django.db.backends': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    },
}

REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] += ['rest_framework.filters.SearchFilter']
