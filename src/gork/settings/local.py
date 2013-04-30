# -*- coding: utf-8 -*-
import os
import djcelery
from gork.settings.base import *

djcelery.setup_loader()
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/../test.db' % PROJECT_ROOT,
    }
}

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'ask',
    'feedz',
    'djcelery',
    'entrez',
)

#BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_PASSWORD = "local"
#BROKER_USER = "local"
#BROKER_VHOST = "mark-desktop"
#BROKER_URL = "amqp://local:local@mark-desktop:5672//"
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

INTERNAL_IPS = (
    '127.0.0.1',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

SECRET_KEY = '007'

SITE_THEME = 'default',


STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'assets/'),
    os.path.join(PROJECT_ROOT, 'themes/%s/assets/' % SITE_THEME),
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'themes/%s/templates/' % SITE_THEME),
)


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hzcdclabs@gmail.com'
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PWD"]
EMAIL_USE_TLS = True
