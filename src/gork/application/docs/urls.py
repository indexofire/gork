# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include


url_patterns = patterns('docs.views',
    url(r'^/', include('projects.urls.private')),
    url(r'^/', include('projects.urls.public')),
    # For serving docs locally and when nginx isn't
    url((r'^docs/(?P<project_slug>[-\w]+)/(?P<lang_slug>%s)/(?P<version_slug>' r'[-._\w]+?)/(?P<filename>.*)$') % LANGUAGES_REGEX, 'core.serve_docs', name='docs_detail'),
    # Redirect to default version.
    url(r'^docs/(?P<project_slug>[-\w]+)/$', 'core.serve_docs', {'version_slug': None, 'lang_slug': None, 'filename': ''}, name='docs_detail'),
    # Handle /page/<path> redirects for explicit "latest" version goodness.
    url(r'^docs/(?P<project_slug>[-\w]+)/page/(?P<filename>.*)$', 'core.serve_docs', {'version_slug': None, 'lang_slug': None}, name='docs_detail'),
)