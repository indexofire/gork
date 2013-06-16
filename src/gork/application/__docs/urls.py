# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include


url_patterns = patterns('docs.views',
    # For serving docs locally and when nginx isn't
    url((r'^docs/(?P<project_slug>[-\w]+)/(?P<lang_slug>%s)/(?P<version_slug>' r'[-._\w]+?)/(?P<filename>.*)$') % LANGUAGES_REGEX, 'core.serve_docs', name='docs_detail'),
    # Redirect to default version.
    url(r'^docs/(?P<project_slug>[-\w]+)/$', 'core.serve_docs', {'version_slug': None, 'lang_slug': None, 'filename': ''}, name='docs_detail'),
    # Handle /page/<path> redirects for explicit "latest" version goodness.
    url(r'^docs/(?P<project_slug>[-\w]+)/page/(?P<filename>.*)$', 'core.serve_docs', {'version_slug': None, 'lang_slug': None}, name='docs_detail'),
)


urlpatterns += patterns('docs.views.private',
    url(r'^private/$', 'project_dashboard', name='projects_dashboard'),
    url(r'^private/import/$', 'project_import', name='projects_import'),
    url(r'^private/upload_html/(?P<project_slug>[-\w]+)/$', 'upload_html', name='projects_upload_html'),
    url(r'^private/export/(?P<project_slug>[-\w]+)/$', 'export', name='projects_export'),
    url(r'^private/(?P<project_slug>[-\w]+)/$', 'project_manage', name='projects_manage'),
    url(r'^private/(?P<project_slug>[-\w]+)/alias/(?P<id>\d+)/', 'edit_alias', name='projects_alias_edit'),
    url(r'^private/(?P<project_slug>[-\w]+)/alias/$', 'edit_alias', name='projects_alias_create'),
    url(r'^private/(?P<project_slug>[-\w]+)/alias/list/$', 'list_alias', name='projects_alias_list'),
    url(r'^private/(?P<project_slug>[-\w]+)/edit/$', 'project_edit', name='projects_edit'),
    url(r'^private/(?P<project_slug>[-\w]+)/version/(?P<version_slug>[-\w.]+)/$', 'project_version_detail', name='project_version_detail'),
    url(r'^private/(?P<project_slug>[-\w]+)/versions/$', 'project_versions', name='projects_versions'),
    url(r'^private/(?P<project_slug>[-\w]+)/delete/$', 'project_delete', name='projects_delete'),
    url(r'^private/(?P<project_slug>[-\w]+)/subprojects/delete/(?P<child_slug>[-\w]+)/$', 'project_subprojects_delete', name='projects_subprojects_delete'),
    url(r'^private/(?P<project_slug>[-\w]+)/subprojects/$', 'project_subprojects', name='projects_subprojects'),
    url(r'^private/(?P<project_slug>[-\w]+)/users/$', 'project_users', name='projects_users'),
    url(r'^private/(?P<project_slug>[-\w]+)/users/delete/$', 'project_users_delete', name='projects_users_delete'),
    url(r'^private/(?P<project_slug>[-\w]+)/notifications/$', 'project_notifications', name='projects_notifications'),
    url(r'^private/(?P<project_slug>[-\w]+)/notifications/delete/$', 'project_notifications_delete', name='projects_notification_delete'),
    url(r'^private/(?P<project_slug>[-\w]+)/translations/$', 'project_translations', name='projects_translations'),
    url(r'^private/(?P<project_slug>[-\w]+)/translations/delete/(?P<child_slug>[-\w]+)/$', 'project_translations_delete', name='projects_translations_delete'),
)


urlpatterns += patterns('docs.views.public',
    # base view, flake8 complains if it is on the previous line.
    url(r'^public/$', 'project_index', name='projects_list'),
    url(r'^public/tags/$', 'tag_index', name='projects_tag_list'),
    url(r'^public/search/$', 'search', name='project_search'),
    url(r'^public/search/autocomplete/$', 'search_autocomplete', name='search_autocomplete'),
    url(r'^public/autocomplete/version/(?P<project_slug>[-\w]+)/$', 'version_autocomplete', name='version_autocomplete'),
    url(r'^public/autocomplete/filter/version/(?P<project_slug>[-\w]+)/$', 'version_filter_autocomplete', name='version_filter_autocomplete'),
    url(r'^public/tags/(?P<tag>[-\w]+)/$', 'project_index', name='projects_tag_detail'),
    url(r'^public/(?P<project_slug>[-\w]+)/$', 'project_detail', name='projects_detail'),
    url(r'^public/(?P<project_slug>[-\w]+)/downloads/$', 'project_downloads', name='project_downloads'),
    url(r'^public/(?P<username>\w+)/$', 'project_index', name='projects_user_list'),
)
