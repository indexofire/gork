# -*- coding: utf-8 -*-
from django.conf import settings


def site_info(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', None),
        'CODE_AUTHOR': getattr(settings, 'CODE_AUTHOR', None),
        'TEMPLATE_AUTHOR': getattr(settings, 'TEMPLATE_AUTHOR', None),
        'SITE_URL': getattr(settings, 'SITE_URL', None),
        'SITE_DESCRIPTION': getattr(settings, 'SITE_DESCRIPTION', None),
    }
