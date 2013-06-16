# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
#from django.views.generic import list_detail
from django.views.generic.list import ListView
from docs.models import SphinxDocProject
from docs.views import *
#from sphinxdoc.views import ProjectSearchView


project_info = {
    'queryset': SphinxDocProject.objects.all().order_by('name'),
    'template_object_name': 'project',
}

urlpatterns = patterns('',
    #url(r'^$', list_detail.object_list, project_info, name='sphinxdoc-index'),
    url(r'^$', ListView.as_view, project_info, name='sphinxdoc-index')
    #url(r'^(?P<slug>[\w-]+)/search/$', ProjectSearchView(), name='sphinxdoc-search'),
    # These URLs have to be without the / at the end so that relative links in
    # static HTML files work correctly and that browsers know how to name files
    # for download
    #url(r'^(?P<slug>[\w-]+)/(?P<type_>_images|_static|_downloads|_source)/(?P<path>.+)$', sphinx_serve, name='sphinxdoc-serve'),
    url(r'^(?P<slug>[\w-]+)/_objects/$', objects_inventory, name='objects-inv'),
    url(r'^(?P<slug>[\w-]+)/$', documentation, {'path': ''}, name='sphinxdocproject-index'),
    url(r'^(?P<slug>[\w-]+)/(?P<path>.+)/$', documentation, name='sphinxdocproject-detail'),
)
