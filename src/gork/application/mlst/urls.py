# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


url_patterns = patterns(
    'mlst.views',
    url(r'^$', 'index', name='mlst-index'),
)
