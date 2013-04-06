# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from mptt.models import TreeManager


class RoleManager(TreeManager):
    def get_by_natural_key(self, codename):
        return self.get(codename=codename)

    def filter_by_user(self, user_obj):
        """return queryset of roles which ``user_obj`` have"""
        # do not defer anything otherwise the returning queryset
        # contains defered instance.
        roles_qs = self.none()
        for role in self.filter(_users=user_obj).iterator():
            roles_qs |= role.get_ancestors()
            roles_qs |= self.filter(pk=role.pk)
        return roles_qs

    def get_all_permissions_of_user(self, user_obj):
        """get a set of all permissions of ``user_obj``"""
        # name, parent, _users, _permissions are required.
        roles = self.defer('codename', 'description').filter(_users=user_obj)
        permissions = Permission.objects.none()
        for role in roles.iterator():
            permissions |= role.permissions
        return permissions.distinct()


class Role(MPTTModel):
    """A role model for enhanced permission system."""
    name = models.CharField(_('name'), max_length=50)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, help_text=_('A description of this permission role'))
    parent = TreeForeignKey('self', verbose_name=_('parent role'), related_name='children', blank=True, null=True)
    _users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name='_roles', db_column='users', blank=True)
    _permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), related_name='roles', db_column='permissions', blank=True)

    objects = RoleManager()

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')
        app_label = 'gauth'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.codename,)

    @property
    def users(self):
        """get all users who belongs to this role or superroles"""
        role_pks = self.get_descendants(True).values_list('id', flat=True)
        qs = get_user_model().objects.only('id', '_roles').filter(_roles__pk__in=role_pks).distinct()
        qs = qs.defer(None)

        def remove_role_perm_cache_before(fn):
            def inner(manager, *objs):
                for obj in objs:
                    if hasattr(obj, '_role_perm_cache'):
                        delattr(obj, '_role_perm_cache')
                return fn(manager, *objs)
            return inner
        # add methods
        qs.add = remove_role_perm_cache_before(self._users.add)
        qs.remove = remove_role_perm_cache_before(self._users.remove)
        qs.clear = self._users.clear
        return qs

    @property
    def permissions(self):
        """get all permissions which this role or subroles have"""
        role_pks = list(self.get_ancestors().values_list('id', flat=True))
        role_pks.append(self.pk)
        qs = Permission.objects.only('id', 'roles').filter(roles__pk__in=role_pks).distinct()
        qs = qs.defer(None)
        # add methods
        qs.add = self._permissions.add
        qs.remove = self._permissions.remove
        qs.clear = self._permissions.clear
        return qs

    def is_belong(self, user_obj):
        """whether the ``user_obj`` belongs to this role or superroles"""
        return self.users.filter(pk=user_obj.pk).exists()


def get_permission_instance(str_or_instance):
    """get permission instance from string or instance"""
    if isinstance(str_or_instance, basestring):
        app_label, codename = str_or_instance.split('.', 1)
        instance = Permission.objects.get(
            content_type__app_label=app_label,
            codename=codename
        )
    else:
        instance = str_or_instance
    return instance
