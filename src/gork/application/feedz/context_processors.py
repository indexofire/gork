# -*- coding: utf-8 -*-
from django.conf import settings


def feedz_settings(request):
    result = {}
    for key in dir(settings):
        if key.startswith('FEED_'):
            result[key] = getattr(settings, key)
    return result
