# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url
from django.core.urlresolvers import get_callable
from feincms.admin import item_editor
from feincms.admin.item_editor import ItemEditor
from feincms.models import Base
from feincms.content.application import models as app_models
from feincms.utils.managers import ActiveAwareContentManagerMixin
from article.mixins import ContentModelMixin


class ArticleManager(ActiveAwareContentManagerMixin, models.Manager):
    active_filters = {
        'simple-active': Q(active=True),
    }


class Article(Base, ContentModelMixin):
    active = models.BooleanField(
        default=True,
    )
    title = models.CharField(
        _('title'),
        max_length=255,
        help_text=_('article Title'),
    )
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        help_text=_('generated from the title, only english character, numbers or -'),
        unique=True,
        editable=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        blank=False,
    )
    publish_date = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
        default=datetime.now(),
    )

    class Meta:
        ordering = ['title']
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    objects = ArticleManager()
    #_feincms_content_types = []
    #feincms_item_editor_context_processors = {}

    @classmethod
    def get_urlpatterns(cls):
        """get url pattern of article object"""
        return patterns(
            'article.views',
            url(r'^$', 'ArticleList.as_view()', name='article_index'),
            url(r'^(?P<slug>[a-z0-9_-]+)/$', 'ArticleDetail.as_view()', name='article_detail'),
        )

    @classmethod
    def remove_field(cls, f_name):
        """Remove a field. Effectively inverse of contribute_to_class"""
        # Removes the field form local fields list
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name):
            delattr(cls, f_name)

    @classmethod
    def get_urls(cls):
        return cls.get_urlpatterns()

    def __unicode__(self):
        return u"%s" % (self.title)

    @app_models.permalink
    def get_absolute_url(self):
        return ('article_detail', 'article.urls', (), {'slug': self.slug, })

    @property
    def is_active(self):
        return Article.objects.active().filter(pk=self.pk).count() > 0

    def save(self, request, *args, **kwargs):
    #    #self.author = CustomUser.objects.get(id=1)
        self.author = request.user
        super(Article, self).save(*args, **kwargs)

    @classmethod
    def register_ext(cls, register_fn):
        register_fn(cls, ArticleAdmin)

    @classmethod
    def register_exts(cls, *extensions):
        if not hasattr(cls, '_profile_extensions'):
            cls._profile_extensions = set()

        here = cls.__module__.split('.')[:-1]
        here_path = '.'.join(here + ['extensions'])

        for ext in extensions:
            if ext in cls._profile_extensions:
                continue

            try:
                if isinstance(ext, basestring):
                    try:
                        fn = get_callable(ext + '.register', False)
                    except ImportError:
                        fn = get_callable('%s.%s.register' % (here_path, ext), False)
                # Not a string, so take our chances and just try to access "register"
                else:
                    fn = ext.register

                cls.register_ext(fn)
                cls._profile_extensions.add(ext)
            except Exception:
                raise


ModelAdmin = get_callable(
    getattr(
        settings,
        'ARTICLE_MODELADMIN_CLASS',
        'django.contrib.admin.ModelAdmin',
    )
)


class ArticleAdmin(ItemEditor):
    list_display = ['__unicode__', 'active', 'author', 'publish_date']
    list_filter = ['author', 'publish_date', 'active']
    search_fields = ['title', 'slug', 'author']
    filter_horizontal = []
    prepopulated_fields = {
        'slug': ('title',),
    }
    fieldset_insertion_index = 2

    fieldsets = [
        (_('Article'), {
            'fields': ['active', 'title', 'slug']
        }),
        (_('Category'), {
            'fields': ['category', ]
        }),
        #(_('Important dates'), {
        #    'fields': ('publication_date', )
        #}),
        #item_editor.FEINCMS_CONTENT_FIELDSET,
    ]

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save(request=request)
        return instance

    def get_form(self, *args, **kwargs):
        from django.utils.functional import curry
        form = super(ArticleAdmin, self).get_form(*args, **kwargs)
        return curry(form)

    @classmethod
    def add_extension_options(cls, *f):
        if isinstance(f[-1], dict):     # called with a fieldset
            cls.fieldsets.insert(cls.fieldset_insertion_index, f)
            f[1]['classes'] = list(f[1].get('classes', []))
            f[1]['classes'].append('collapse')
        else:   # assume called with "other" fields
            cls.fieldsets[1][1]['fields'].extend(f)


admin.site.register(Article, ArticleAdmin)
