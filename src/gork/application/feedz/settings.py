# -*- coding: utf-8 -*-
from django.conf import settings


FEED_PAGE_SIZE = getattr(settings, 'FEED_PAGE_SIZE', 25)
FEED_SUMMARY_SIZE = getattr(settings, 'FEED_SUMMARY_SIZE', 2000)
FEED_SITE_TITLE = getattr(settings, 'FEED_SITE_TITLE', 'HZCDCLabs')
FEED_SITE_DESCRIPTION = getattr(settings, 'FEED_SITE_DESCRIPTION', 'Labs of CDC in Hangzhou')
FEED_CLOUD_STEPS = getattr(settings, 'FEED_CLOUD_STEPS', 4)
FEED_CLOUD_MIN_COUNT = getattr(settings, 'FEED_CLOUD_MIN_COUNT', 2)
FEED_TAGS_LOWERCASE = getattr(settings, 'FEED_TAGS_LOWERCASE', True)
FEED_EXPAND_FULL = getattr(settings, 'FEED_EXPAND_FULL', False)
FEED_POST_PROCESSORS = getattr(settings, 'FEED_POST_PROCESSORS', (
    'feedz.processors.ContentFilterProcessor',
))
