# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


url_patterns = patterns(
    'mlst.views',
    url(r'^$', 'index', name='mlst-index'),
    url(r'^t/$', 'taxon-list', name='mlst-taxon-list'),
    url(r'^t/(?P<slug>[a-zA-Z0-9_-]+)/$', 'taxon-detail', name='mlst-taxon-detail'),
    url(r'^t/(?P<slug>[a-zA-Z0-9_-]+)/(?P<slug>[a-zA-Z0-9_-]+)/$', 'dataset', name='mlst-dataset-detail'),
)
