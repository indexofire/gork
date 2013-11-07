# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns(
    'mlst.views',
    url(r'^$', 'mlst_index', name='mlst-index'),
    #url(r'^t/$', 'taxon-list', name='mlst-taxon-list'),
    url(r'^t/(?P<slug>[a-zA-Z0-9_-]+)/$', 'taxon_detail', name='mlst-taxon-detail'),
    #url(r'^t/(?P<t_slug>[a-zA-Z0-9_-]+)/(?P<d_slug>[a-zA-Z0-9_-]+)/$', 'dataset', name='mlst-dataset-detail'),
    url(r'^d/(?P<slug>[a-zA-Z0-9_-]+)/add/$', 'add_strain', name='mlst-add-strain'),
)
