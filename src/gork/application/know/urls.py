# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.utils.importlib import import_module
from gauth.views import SignupView, LoginView, LogoutView
from know.views import article
from know.conf import settings
from know.core.plugins import registry

'''
urlpatterns = patterns('',
    url('^$', article.ArticleView.as_view(), name='root', kwargs={'path': ''}),
    url('^create-root/$', article.root_create, name='root_create'),
    url('^_revision/diff/(?P<revision_id>\d+)/$', article.diff, name='diff'),
)
'''

class WikiURLPatterns(object):
    """
    configurator for wiki urls.

    To customize, you can define your own subclass, either overriding
    the view providers, or overriding the functions that collect
    views.
    """

    # basic views
    article_view_class = article.ArticleView
    article_create_view_class = article.Create
    article_delete_view_class = article.Delete
    article_deleted_view_class = article.Deleted
    article_dir_view_class = article.Dir
    article_edit_view_class = article.Edit
    article_preview_view_class = article.Preview
    article_history_view_class = article.History
    article_settings_view_class = article.Settings
    article_source_view_class = article.Source
    article_plugin_view_class = article.Plugin
    revision_change_view = 'know.views.article.change_revision'
    revision_merge_view = 'know.views.article.merge'

    create_root = 'know.views.article.root_create'
    search_view_class = article.SearchView
    article_diff_view = 'know.views.article.diff'

    # account views
    signup_view_class = SignupView
    login_view_class = LoginView
    logout_view_class = LogoutView

    def get_urls(self):
        urlpatterns = self.get_root_urls()
        urlpatterns += self.get_accounts_urls()
        urlpatterns += self.get_revision_urls()
        urlpatterns += self.get_article_urls()
        urlpatterns += self.get_plugin_urls()

        # This ALWAYS has to be the last of all the patterns since
        # the paths in theory could wrongly match other targets.
        urlpatterns += self.get_article_path_urls()
        return urlpatterns

    def get_root_urls(self):
        urlpatterns = patterns('',
            url('^$', self.article_view_class.as_view(), name='root', kwargs={'path': ''}),
            url('^create-root/$', self.create_root, name='root_create'),
            url('^_search/$', self.search_view_class.as_view(), name='search'),
            url('^_revision/diff/(?P<revision_id>\d+)/$', self.article_diff_view, name='diff'),
       )
        return urlpatterns

    def get_accounts_urls(self):
        urlpatterns = patterns('',
            url('^_accounts/sign-up/$', self.signup_view_class.as_view(), name='signup'),
            url('^_accounts/logout/$', self.logout_view_class.as_view(), name='logout'),
            url('^_accounts/login/$', self.login_view_class.as_view(), name='login'),
           )
        return urlpatterns

    def get_revision_urls(self):
        urlpatterns = patterns('',
            # This one doesn't work because it don't know where to redirect after...
            url('^_revision/change/(?P<article_id>\d+)/(?P<revision_id>\d+)/$', self.revision_change_view, name='change_revision'),
            url('^_revision/preview/(?P<article_id>\d+)/$', self.article_preview_view_class.as_view(), name='preview_revision'),
            url('^_revision/merge/(?P<article_id>\d+)/(?P<revision_id>\d+)/preview/$', self.revision_merge_view, name='merge_revision_preview', kwargs={'preview': True}),
           )
        return urlpatterns

    def get_article_urls(self):
        urlpatterns = patterns('',
            # Paths decided by article_ids
            url('^(?P<article_id>\d+)/$', self.article_view_class.as_view(), name='get'),
            url('^(?P<article_id>\d+)/delete/$', self.article_delete_view_class.as_view(), name='delete'),
            url('^(?P<article_id>\d+)/deleted/$', self.article_deleted_view_class.as_view(), name='deleted'),
            url('^(?P<article_id>\d+)/edit/$', self.article_edit_view_class.as_view(), name='edit'),
            url('^(?P<article_id>\d+)/preview/$', self.article_preview_view_class.as_view(), name='preview'),
            url('^(?P<article_id>\d+)/history/$', self.article_history_view_class.as_view(), name='history'),
            url('^(?P<article_id>\d+)/settings/$', self.article_settings_view_class.as_view(), name='settings'),
            url('^(?P<article_id>\d+)/source/$', self.article_source_view_class.as_view(), name='source'),
            url('^(?P<article_id>\d+)/revision/change/(?P<revision_id>\d+)/$', self.revision_change_view, name='change_revision'),
            url('^(?P<article_id>\d+)/revision/merge/(?P<revision_id>\d+)/$', self.revision_merge_view, name='merge_revision'),
            url('^(?P<article_id>\d+)/plugin/(?P<slug>\w+)/$', self.article_plugin_view_class.as_view(), name='plugin'),
           )
        return urlpatterns

    def get_article_path_urls(self):
        urlpatterns = patterns('',
            # Paths decided by URLs
            url('^(?P<path>.+/|)_create/$', self.article_create_view_class.as_view(), name='create'),
            url('^(?P<path>.+/|)_delete/$', self.article_delete_view_class.as_view(), name='delete'),
            url('^(?P<path>.+/|)_deleted/$', self.article_deleted_view_class.as_view(), name='deleted'),
            url('^(?P<path>.+/|)_edit/$', self.article_edit_view_class.as_view(), name='edit'),
            url('^(?P<path>.+/|)_preview/$', self.article_preview_view_class.as_view(), name='preview'),
            url('^(?P<path>.+/|)_history/$', self.article_history_view_class.as_view(), name='history'),
            url('^(?P<path>.+/|)_dir/$', self.article_dir_view_class.as_view(), name='dir'),
            url('^(?P<path>.+/|)_settings/$', self.article_settings_view_class.as_view(), name='settings'),
            url('^(?P<path>.+/|)_source/$', self.article_source_view_class.as_view(), name='source'),
            url('^(?P<path>.+/|)_revision/change/(?P<revision_id>\d+)/$', self.revision_change_view, name='change_revision'),
            url('^(?P<path>.+/|)_revision/merge/(?P<revision_id>\d+)/$', self.revision_merge_view, name='merge_revision'),
            url('^(?P<path>.+/|)_plugin/(?P<slug>\w+)/$', self.article_plugin_view_class.as_view(), name='plugin'),
            # This should always go last!
            url('^(?P<path>.+/|)$', self.article_view_class.as_view(), name='get'),
           )
        return urlpatterns

    def get_plugin_urls(self):
        urlpatterns = patterns('',)
        for plugin in registry.get_plugins().values():
            slug = getattr(plugin, 'slug', None)
            plugin_urlpatterns = getattr(plugin, 'urlpatterns', None)
            if slug and plugin_urlpatterns:
                urlpatterns += patterns('',
                    url('^(?P<article_id>\d+)/plugin/' + slug + '/', include(plugin_urlpatterns)),
                    url('^(?P<path>.+/|)_plugin/' + slug + '/', include(plugin_urlpatterns)),
               )
        return urlpatterns


def get_pattern(app_name="know", namespace="know", url_config_class=None):
    """
    Every url resolution takes place as "know:view_name".

    You should not attempt to have multiple deployments of the know in a single Django project.
    https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    if url_config_class is None:
        url_config_classname = getattr(settings, 'URL_CONFIG_CLASS', None)
        if url_config_classname is None:
            url_config_class = WikiURLPatterns
        else:
            url_config_modname, config_classname = url_config_classname.rsplit('.', 1)
            url_config_mod = import_module(url_config_modname)
            url_config_class = getattr(url_config_mod, config_classname)
    urlpatterns = url_config_class().get_urls()
    return urlpatterns, app_name, namespace
