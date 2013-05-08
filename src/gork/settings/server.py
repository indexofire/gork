# -*- coding: utf-8 -*-
import os
from gork.settings.base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'America/Chicago'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hzcdclabs',
        'USER': 'hzcdclabs',
        'PASSWORD': get_env("DATABASE_PWD"),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS += (
    'gunicorn',
    'social_auth',
)

BROKER_URL = 'amqp://hzcdclabs:hzcdclabs@localhost:5672/hzcdclabs'

SECRET_KEY = os.environ["SECRET_KEY"]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = get_env("EMAIL_ADDRESS")
EMAIL_HOST_PASSWORD = get_env("EMAIL_PWD")
EMAIL_USE_TLS = True

ALLOWED_HOSTS = [
    '.hzcdclabs.org',
]

ADMIN_URL = get_env("ADMIN_URL")

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.weibo.WeiboBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
    'gauth.backends.RoleBackend',
    'gauth.backends.PermissionBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/auth/'

WEIBO_CLIENT_KEY = get_env('WEIBO_KEY')
WEIBO_CLIENT_SECRET = get_env('WEIBO_SECRET')
GOOGLE_OAUTH2_CLIENT_ID = get_env('GOOGLE_OAUTH2_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = get_env('GOOGLE_OAUTH2_SECRET')
