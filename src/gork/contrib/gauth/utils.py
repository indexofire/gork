# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission


def perm_to_permission(perm):
    """
    Convert string permission to permission instance.
    The string permission must be written as
    ``"app_label.codename"``

    Usage::

        >>> permission = perm_to_permission('auth.add_user')
        >>> permission.content_type.app_label
        u'auth'
        >>> permission.codename
        u'add_user'

    """
    try:
        app_label, codename = perm.split('.', 1)
    except IndexError:
        raise AttributeError(
            "passed string perm has wrong format. "
            "string perm should be 'app_label.codename'."
        )
    else:
        permission = Permission.objects.get(
            content_type__app_label=app_label,
            codename=codename
        )
        return permission


def permission_to_perm(permission):
    """
    Convert permission instance to string permission.

    Usage::

        >>> permission = Permission.objects.get(
        ...     content_type__app_label='auth',
        ...     codename='add_user',
        ... )
        >>> permission_to_perm(permission)
        u'auth.add_user'

    """
    app_label = permission.content_type.app_label
    codename = permission.codename
    return "%s.%s" % (app_label, codename)


def get_permission_codename(perm):
    """get permission codename from permission string

    Usage::

        >>> get_permission_codename(u'app_label.codename_model')
        u'codename_model'
        >>> get_permission_codename(u'app_label.codename')
        u'codename'
        >>> get_permission_codename(u'codename_model')
        u'codename_model'
        >>> get_permission_codename(u'codename')
        u'codename'
        >>> get_permission_codename(u'app_label.app_label.codename_model')
        u'app_label.codename_model'

    """
    try:
        perm = perm.split('.', 1)[1]
    except IndexError:
        pass
    return perm
