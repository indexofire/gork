# -*- coding: utf-8 -*-


class ValidationError(Exception):
    """Validation error"""


class PermissionDetectionError(Exception):
    """Permission detection error"""


class AlreadyRegistered(Exception):
    """PermissionHandler of the model is already registered error"""
    def __init__(self, model):
        msg = 'Permission handler of the model "%s.%s" is already registered'
        msg = msg % (model._meta.app_label, model.__class__.__name__)
        super(AlreadyRegistered, self).__init__(msg)


class NotRegistered(Exception):
    """PermissionHandler of the model is not registered error"""
    def __init__(self, model):
        msg = 'Permission handler of the model "%s.%s" is not registered'
        msg = msg % (model._meta.app_label, model.__class__.__name__)
        super(NotRegistered, self).__init__(msg)
