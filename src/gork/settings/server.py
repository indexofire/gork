# -*- coding: utf-8 -*-
import os
from .base import *

SITE_THEME = 'gork'
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hzcdclabs',
        'USER': 'hzcdclabs',
        'PASSWORD': os.environ["DATABASE_PWD"],
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


INSTALLED_APP += (
    'gunicorn',
)
SECRET_KEY = os.environ["SECRET_KEY"]
