# -*- coding: utf-8 -*-
from __future__ import with_statement
from gauth.models import Role
from gauth.utils import permission_to_perm


__all__ = ('RoleBackend',)


class RoleBackend(object):
    """Authentication backend for role system"""
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = True

    def authenticate(self, username, password):
        """This backend is only for checking permission"""
        return None

    def get_all_roles(self, user_obj):
        if hasattr(user_obj, '_role_cache'):
            return user_obj._role_cache
        roles = Role.objects.filter_by_user(user_obj)
        roles = set([r.codename for r in roles])
        user_obj._role_cache = roles
        return user_obj._role_cache

    def get_all_permissions(self, user_obj, obj=None):
        if obj is not None:
            # role permission system doesn't handle
            # object permission
            return set()
        if hasattr(user_obj, '_role_perm_cache'):
            return user_obj._role_perm_cache
        perms = Role.objects.get_all_permissions_of_user(user_obj)
        perms = set([permission_to_perm(p) for p in perms])
        user_obj._role_perm_cache = perms
        return user_obj._role_perm_cache

    def has_role(self, user_obj, role):
        if user_obj.is_anonymous() or not user_obj.is_active:
            return False
        roles = self.get_all_roles(user_obj)
        return role in roles

    def has_perm(self, user_obj, perm, obj=None):
        if user_obj.is_anonymous() or not user_obj.is_active:
            return False
        permissions = self.get_all_permissions(user_obj, obj)
        return perm in permissions

    def has_module_perms(self, user_obj, app_label):
        if not user_obj.is_active:
            return False
        permissions = self.get_all_permissions(user_obj)
        for perm in permissions:
            if perm[:perm.index('.')] == app_label:
                return True
        return False
