# -*- coding: utf-8 -*-
from __future__ import with_statement
from gauth.handlers import registry

__all__ = ('PermissionBackend',)


class PermissionBackend(object):
    """Authentication backend for cheking permissions

    This backend is used to check permissions. The permissions
    are handled with ``PermissionHandler`` which have to be registered in
    ``fluidpermission.handlers.registry`` before use.

    ``has_perm(user_obj, perm, obj=None)`` method of detected model's
    ``PermissionHandler`` will be used to cheking process.

    If no model was detected or no handler was registered, this backend
    does not touch that permission and return ``None`` to pass the permission
    checking process to downstream backends.

    """
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        """This backend is only for checking permission"""
        return None

    def has_perm(self, user_obj, perm, obj=None):
        """check permission"""
        # get permission handlers fot this perm
        cache_name = '_%s_cache' % perm
        if hasattr(self, cache_name):
            handlers = getattr(self, cache_name)
        else:
            handlers = [h for h in registry.get_handlers() if perm in h.get_permissions()]
            setattr(self, cache_name, handlers)
        for handler in handlers:
            if handler.has_perm(user_obj, perm, obj=obj):
                return True
        # do not touch this permission
        return False

    def has_module_perms(self, user_obj, app_label):
        # get permission handlers fot this perm
        handlers = registry.get_module_handlers(app_label)
        for handler in handlers:
            if handler.has_module_perms(user_obj, app_label):
                return True
        return False
