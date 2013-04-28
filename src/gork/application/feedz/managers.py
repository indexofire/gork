# -*- coding: utf-8 -*-
from django.db import models


class ActivePostManager(models.Manager):
    def get_query_set(self):
        return super(ActivePostManager, self).get_query_set().filter(active=True)
