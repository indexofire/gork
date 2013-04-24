# -*- coding: utf-8 -*-
import os
from gork.settings.base import *


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


INSTALLED_APPS += (
    'gunicorn',
    'article',
    'article.module.category',
)
SECRET_KEY = os.environ["SECRET_KEY"]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hzcdclabs@gmail.com'
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PWD"]
EMAIL_USE_TLS = True
