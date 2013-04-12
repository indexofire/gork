# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^favicon\.ico/$', RedirectView.as_view(url='%s/img/favicon.ico' % settings.STATIC_URL), name='icon'),
    url(r'^admin/', include(admin.site.urls), name='site-admin'),
    url(r'^auth/', include('gauth.urls')),
    #url(r'^msg/', include('gmessage.urls')),
    #url(r'^gallery/', include('gallery.urls')),
    #url(r'^/', include('gqanda.urls')),
    #url(r'^ask/', include('ask.urls')),
    #url(r'^wiki/', include('know.urls')),
)

#from gwiki.urls import get_pattern as get_wiki_pattern
#from gnotify.urls import get_pattern as get_notify_pattern
#urlpatterns += patterns('',
    #(r'^notify/', get_notify_pattern()),
    #(r'^wiki/', get_wiki_pattern()),
#)


from know.urls import get_pattern as get_wiki_pattern
urlpatterns += patterns('',
    #(r'^notify/', get_notify_pattern()),
    (r'^know/', get_wiki_pattern()),
)

# default url route
urlpatterns += patterns('',
    url(r'^', include('feincms.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT},
        ),
        url(r'^%s/(?P<path>.*)$' % settings.STATIC_URL.strip('/'),
            'django.views.static.serve', {'document_root': settings.STATIC_ROOT},
        ),
    )
