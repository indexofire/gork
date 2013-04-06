# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.base import ModelBase
from gauth.handlers import PermissionHandler
from gauth.exceptions import ValidationError


__all__ = ('validate',)


def validate(cls, model):
    """
    Does basic PermissionHandler option validation. Calls custom validation
    classmethod in the end if it is provided in cls. The signature of the
    custom validation classmethod should be: def validate(cls, model).

    """
    # Before we can introspect models, they need to be fully loaded so that
    # inter-relations are set up correctly. We force that here.
    models.get_apps()

    # validate model class
    if not isinstance(model, ModelBase):
        # this mean the model is not subclass of models.Model
        raise ValidationError(
            'The model "%s" must be a subclass of ``models.Model``.' % model.__class__.__name__
        )

    # validate handler class
    if not issubclass(cls, PermissionHandler):
        raise ValidationError(
            'The handler "%s" must be a subclass of '
            '``fluidpermission.handlers.PermissionHandler``.' % cls.__class__.__name__
        )

    # call custom validation classmethod
    if hasattr(cls, 'validate'):
        cls.validate(model)
