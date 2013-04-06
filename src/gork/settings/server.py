# -*- coding: utf-8 -*-
from .base import *

SITE_THEME = 'gork'
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',

    }
}
