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
    #'feedz',
    'djcelery',
    'entrez',
    'endless_pagination',
    'gfavor',
    'social_auth',
    #'actstream',
)

AUTHENTICATION_BACKENDS = (
    #'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.contrib.weibo.WeiboBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

WEIBO_CLIENT_KEY = get_env('WEIBO_KEY')
WEIBO_CLIENT_SECRET = get_env('WEIBO_SECRET')

#ACTSTREAM_SETTINGS = {
#    'MODELS': ('gauth.guser', 'auth.group', 'sites.site', 'comments.comment'),
#    'MANAGER': 'actstream.managers.ActionManager',
#    'FETCH_RELATIONS': True,
#    'USE_PREFETCH': True,
    #'USE_JSONFIELD': True,
    #'GFK_FETCH_DEPTH': 1,
#}

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
