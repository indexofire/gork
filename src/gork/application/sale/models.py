# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from sale.settings import STATUS_CHOICES


class ShoppingItem(models.Model):
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL)
    item_name = models.CharField(max_length=255)
    item_info = models.CharField(max_length=1024)
    add_time = models.DateTimeField(auto_now=True)
    edit_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return


