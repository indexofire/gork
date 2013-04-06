# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured
from gauth.exceptions import AlreadyRegistered, NotRegistered
from gauth.handlers.base import PermissionHandler


__all__ = ('registry', 'PermissionHandler',)


class Registry(object):
    """Registry of permission handlers

    Register permission handlers to this registry to use.

    """
    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, handler_class):
        """register new permission handler for the model(s)

        If the model is already registered in registry,
        ``AlreadyRegistered`` exception will come up.

        """
        # Don't import the humonogus validation code unless required
        if settings.DEBUG:
            from permission.validation import validate
        else:
            validate = lambda model, mediator: None

        if not hasattr(model_or_iterable, '__iter__'):
            # this mean subclass of models.Model
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            # Validate (which might be a no-op)
            validate(handler_class, model)

            if model._meta.abstract:
                raise ImproperlyConfigured(
                    'The model %s is abstract, so it cannot be registered '
                    'with permission.' % model.__name__
                )
            if model in self._registry:
                raise AlreadyRegistered(model)

            # Instantiate the handler to save in the registry
            instance = handler_class(model)
            self._registry[model] = instance

    def unregister(self, model_or_iterable):
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered(model)
            # remove from registry
            del self._registry[model]

    def get_handlers(self):
        return tuple(self._registry.values())

    def get_module_handlers(self, app_label):
        return tuple()

registry = Registry()
