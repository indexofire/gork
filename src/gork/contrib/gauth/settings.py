# -*- coding: utf-8 -8-
import pytz
from django.conf import settings
from django.utils.translation import get_language_info
#from gauth.forms import SigninUsernameForm


#GAUTH_FORM_CLASS = SigninUsernameForm
GAUTH_EMAIL_CONFIRMATION_EXPIRE_DAYS = getattr(settings, 'GAUTH_EMAIL_CONFIRMATION_EXPIRE_DAYS', 14)
GAUTH_DEFAULT_FROM_EMAIL = getattr(settings, 'GAUTH_DEFAULT_FROM_EMAIL', '')

# set true if open new register users, or false if you close the registration
GAUTH_OPEN_SIGNUP = getattr(settings, 'GAUTH_OPEN_SIGNUP', True)

GAUTH_USER_DEFAULT_EXTENSIONS = (
    'gauth.extensions.avatar',
    'gauth.extensions.portfolio',
)
GAUTH_USER_EXTENSIONS = getattr(settings, 'GAUTH_USER_EXTENSIONS', GAUTH_USER_DEFAULT_EXTENSIONS)

GAUTH_LOGIN_URL = getattr(settings, 'LOGIN_URL', "/auth/login/")
GAUTH_LOGIN_REDIRECT_URL = getattr(settings, 'GAUTH_LOGIN_REDIRECT_URL', '/')
GAUTH_LOGOUT_REDIRECT_URL = getattr(settings, 'GAUTH_LOGOUT_REDIRECT_URL', '/')
GAUTH_SIGNUP_REDIRECT_URL = getattr(settings, 'GAUTH_SIGNUP_REDIRECT_URL', '/')

GAUTH_EMAIL_UNIQUE = getattr(settings, 'GAUTH_EMAIL_UNIQUE', True)

GAUTH_EMAIL_CONFIRMATION_REQUIRED = getattr(settings, 'GAUTH_EMAIL_CONFIRMATION_REQUIRED', False)

GAUTH_PASSWORD_CHANGE_REDIRECT_URL = getattr(settings, 'GAUTH_PASSWORD_CHANGE_REDIRECT_URL', "/")
GAUTH_PASSWORD_RESET_REDIRECT_URL = getattr(settings, 'GAUTH_PASSWORD_RESET_REDIRECT_URL', "/auth/login/")
GAUTH_REMEMBER_ME_EXPIRY = 60 * 60 * 24 * 30 * 3
GAUTH_USER_DISPLAY = lambda user: user.username
GAUTH_CREATE_ON_SAVE = True
GAUTH_EMAIL_CONFIRMATION_EMAIL = False
GAUTH_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
GAUTH_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/auth/login/"
GAUTH_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
GAUTH_SETTINGS_REDIRECT_URL = "/account/settings/"
GAUTH_NOTIFY_ON_PASSWORD_CHANGE = True
GAUTH_DELETION_MARK_CALLBACK = "account.callbacks.GAUTH_delete_mark"
GAUTH_DELETION_EXPUNGE_CALLBACK = "account.callbacks.GAUTH_delete_expunge"
GAUTH_DELETION_EXPUNGE_HOURS = 48
GAUTH_TIMEZONES = zip(pytz.all_timezones, pytz.all_timezones)
GAUTH_LANGUAGES = [(code, get_language_info(code).get("name_local")) for code, lang in settings.LANGUAGES]
GAUTH_DEFAULT_FROM_EMAIL = ''
GAUTH_DEFAULT_PASSWORD = '123456'

# User permission settings
PERMISSION_MODULE_NAME = getattr(settings, 'PERMISSION_MODULE_NAME', 'permissions')
PERMISSION_BUILTIN_TEMPLATETAGS = getattr(settings, 'PERMISSION_BUILTIN_TEMPLATETAGS', True)
PERMISSION_REPLACE_BUILTIN_IF = getattr(settings, 'PERMISSION_REPLACE_BUILTIN_IF', True)
PERMISSION_EXTEND_USER_CLASS = getattr(settings, 'PERMISSION_EXTEND_USER_CLASS', True)
