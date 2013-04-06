# -*- coding: utf-8 -*-
from django.db.models import Manager, Q
from ask.settings import POST_OPEN, POST_CLOSED


class AllManager(Manager):
    """Returns all posts"""
    def get_query_set(self):
        return super(AllManager, self).get_query_set().select_related('author')


class OpenManager(Manager):
    """Returns all open posts"""
    def get_query_set(self):
        return super(OpenManager, self).get_query_set().filter(Q(status=POST_OPEN) | Q(status=POST_CLOSED)).select_related('author')
