# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
#from feincms import extensions
from taggit.managers import TaggableManager


def get_urlpatterns(cls):
    urlpatterns = patterns('taggit.views',
        url(r'^tags/(?P<slug>[^/]+)/$', 'tagged_object_list', {
            'queryset': cls.objects.active,
            }, name="article_tagged_list"),
        )
    return cls.get_urlpatterns_orig() + urlpatterns

'''
class Extension(extensions.Extension):
    """
    tag extension for article
    """
    def handle_model(self):
        self.model.add_to_class('tags', TaggableManager(
            verbose_name=_('tags'), blank=True))
        self.model.get_urlpatterns_orig = self.model.get_urlpatterns
        self.model.get_urlpatterns = classmethod(get_urlpatterns)

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options('tags')
'''


def register(cls, admin_cls):
    cls.add_to_class(
        'tags',
        TaggableManager(verbose_name=_('tags'), blank=True)
    )

    cls.get_urlpatterns_orig = cls.get_urlpatterns

    @classmethod
    def get_urlpatterns(cls):
        return cls.get_urlpatterns_orig() + patterns('taggit.views',
            url(r'^tags/(?P<slug>[^/]+)/$', 'tagged_object_list',
                {'queryset': cls.objects.active},
                name="article_tagged_list"),
            )
    cls.get_urlpatterns = get_urlpatterns

    if admin_cls:
        if admin_cls.fieldsets:
            admin_cls.fieldsets.append(
                (_('Tags'),
                    {
                        'fields': ('tags', ),
                        'classes': ('collapse',),
                    }
                )
            )
