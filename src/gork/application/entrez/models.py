# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from entrez.settings import *


class EntrezEntry(models.Model):
    """
    Entrez's entry stored in django database
    """
    title = models.CharField(
        max_length=255,
    )
    url = models.CharField(
        max_length=255,
    )

    def __init__(self):
        return self.title

    def get_absolute_url(self):
        return self.url


class EntrezTerm(models.Model):
    title = models.CharField(
        max_length=255,
    )
    condition = models.CharField(
        max_length=255,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='search term owner',
    )

    def __init__(self):
        return self.title
