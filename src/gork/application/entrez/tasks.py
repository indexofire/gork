# -*- coding: utf-8 -*-
from celery import task


@task()
def add(x, y):
    return x + y


@task()
def fetch_recent_entry(*args, **kwargs):
    pass
