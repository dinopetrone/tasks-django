"""Development settings and globals."""


from os.path import join, normpath
from os import getenv

from base import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {


        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'django',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': '',
        'PORT': '',
    }
}
# REDIS_HOST = getenv('REDISTOGO_URL', 'redis://localhost:6379')
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEVSERVER_DEFAULT_ADDR = '0.0.0.0'
INSTALLED_APPS += (
    'debug_toolbar',
    'devserver',
    'storages',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
}
########## END TOOLBAR CONFIGURATION



########## STORAGE SETTINGS

AWS_ACCESS_KEY_ID = 'awspublickey'
AWS_SECRET_ACCESS_KEY = 'awssecretkey'

AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME = 'tasks-app-local'
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = "utils.storage.MediaRootS3BotoStorage"
MEDIA_URL = 'http://s3.amazonaws.com/{}/uploads/'.format(AWS_STORAGE_BUCKET_NAME)

STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'

########## END STORAGE SETTINGS

