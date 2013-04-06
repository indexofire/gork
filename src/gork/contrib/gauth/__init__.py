# -*- coding: utf-8 -*-
# codes from repos:
# 1. `django-user-account` (http://github.com/pinax/django-user-accounts)
# 2. `django-extensible-profiles` (http://github.com/incuna/django-extensible-profiles)
# 3. `django-permission` (https://github.com/lambdalisue/django-permission)
import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from gauth.handlers import registry
from gauth.settings import *


# loading permission_tags globally
if PERMISSION_BUILTIN_TEMPLATETAGS:
    from django.template import add_to_builtins
    add_to_builtins('gauth.templatetags.permission_tags')

# backends and user class
if PERMISSION_EXTEND_USER_CLASS:
    from django.contrib import auth
    from django.contrib.auth.models import AnonymousUser
    #from django.contrib.auth import get_user_model

    def _user_has_role(user, role):
        backends = auth.get_backends()
        for backend in backends:
            if user.is_anonymous() or user.is_active or backend.support_inactive_user:
                if hasattr(backend, 'has_role'):
                    if backend.has_role(user, role):
                        return True

        return False

    def _user_get_all_roles(user):
        backends = auth.get_backends()
        for backend in backends:
            if user.is_anonymous() or user.is_active or backend.support_inactive_user:
                if hasattr(backend, 'get_all_roles'):
                    return backend.get_all_roles(user)
        return None

    #get_user_model().has_role = _user_has_role
    #get_user_model().roles = property(_user_get_all_roles)
    from gauth.models import GUser
    GUser.has_role = _user_has_role
    GUser.roles = property(_user_get_all_roles)
    AnonymousUser.has_role = lambda user, role: False
    AnonymousUser.roles = ()


def autodiscover(module_name=None):
    """
    Auto-discover INSTALLED_APPS permissions.py modules and fail silently when
    not present. This forces an import on them to register any permissions bits
    they may want.

    """
    module_name = module_name or PERMISSION_MODULE_NAME

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's permissions module
        try:
            before_import_registry = copy.copy(registry._registry)
            import_module('%s.%s' % (app, module_name))
        except:
            # Reset the model registry to the state before tha last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8254)
            registry._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an permissions module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, module_name):
                raise


autodiscover()
