# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from sale.settings import STATUS_CHOICES


class ShoppingItem(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    info = models.CharField(max_length=1024)
    create_time = models.DateTimeField(auto_now=True)
    lastedit_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    list = models.ForeignKey('ShoppingList', related_name='shopping_list')

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return


class ShoppingList(models.Model):
    create_time = models.DateTimeField()
    lastedit_time = models.DateTimeField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
