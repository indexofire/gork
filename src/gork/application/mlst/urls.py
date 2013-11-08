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


urlpatterns = patterns(
    'mlst.views',
    # MLST main page show all collected species
    url(r'^$', 'mlst_index', name='mlst-index'),
    # MLST strains list info of one species
    url(r'^s/(?P<slug>[a-zA-Z]+)/$', 'strain_list', name='mlst-strain-list'),
    # MLST strain detail info of one species
    url(r'^s/(?P<slug>[a-zA-Z]+)/(?P<id>\d+)/$', 'strain_detail', name='mlst-strain-detail'),
    # MLST info syn page from official MLST siteof one species
    url(r'^s/(?P<slug>[a-zA-Z]+)/syn/$', 'mlst_syn', name='mlst-syn'),
    # MLST st list info of one species
    url(r'^s/(?P<slug>[a-zA-Z]+)/st/$', 'strain_st_list', name='mlst-strain-st-list'),
    # MLST st detail info of one species
    url(r'^s/(?P<slug>[a-zA-Z]+)/st/(?P<st>\d+))/$', 'strain_st_detail', name='mlst-strain-st-detail'),
)