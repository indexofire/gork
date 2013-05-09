# -*- coding: utf-8 -*-
import os
import sys
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


def get_env(var):
    try:
        return os.environ[var]
    except KeyError:
        raise ImproperlyConfigured("Set the %s environment variable" % var)

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'contrib'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'application'))


SITE_NAME = 'HZCDCLabs'
SITE_AUTHOR = 'indexofire'
SITE_THEME = 'default'
SITE_THEME_AUTHOR = 'indexofire'
SITE_DESCRIPTION = 'Hangzhou Center for Disease Control and Prevention Lab Site'

ADMINS = (
    ('Mark Renton', 'indexofire@gmail.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh_CN'
LANGUAGES = (
    ('zh-cn', _('Simplified Chinese')),
)

ROOT_URLCONF = 'gork.urls'
WSGI_APPLICATION = 'gork.wsgi.application'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'assets/'),
    os.path.join(PROJECT_ROOT, 'themes/%s/assets/' % SITE_THEME),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'themes/%s/templates/' % SITE_THEME),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

AUTH_USER_MODEL = 'gauth.GUser'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',
    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'imagekit',
    'south',
    'mptt',
    'gbase',
    'gauth',
    'gform',
    'gtag',
    'gmessage',
    'know',
    'know.plugins.attachments',
    'know.plugins.notifications',
    'know.plugins.images',
    'know.plugins.macros',
    #'gallery',
    'django.contrib.humanize',
    'gnotify',
    'sekizai',
    'sorl.thumbnail',
    'article',
    'article.module.category',
    #'compressor',
    'denorm',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "feincms.context_processors.add_page_if_missing",
    "sekizai.context_processors.sekizai",
    "gbase.context_processors.site_info",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#FEINCMS_TIDY_HTML = True
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': '%s/libs/tiny_mce/tiny_mce.js' % STATIC_URL,
}
FEINCMS_FRONTEND_EDITING = True

LOGIN_URL = '/auth/login/'

FEINCMS_REVERSE_MONKEY_PATCH = False

GAUTH_USER_EXTENSIONS = (
    'gauth.extensions.avatar',
    'gauth.extensions.portfolio',
    'ask.extensions.question',
)
