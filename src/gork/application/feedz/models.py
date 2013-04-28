# -*- coding: utf-8 -*-
from urlparse import urlsplit
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.content.application import models as app_models
from feedz.managers import ActivePostManager
from feedz.settings import *
from feedz.utils import clean_html


class Feed(models.Model):
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    feed_url = models.CharField(
        _('feed url'),
        max_length=255,
        unique=True,
    )
    site_url = models.CharField(
        _('site url'),
        max_length=255,
    )
    active = models.BooleanField(
        _('active'),
        blank=True,
        default=True,
    )
    #etag = models.CharField(u'ETag', max_length=255, blank=True, default='')
    last_checked = models.DateTimeField(
        _('last checked'),
        blank=True,
        null=True,
    )
    skip_filters = models.BooleanField(
        _('allow all messages'),
        blank=True,
        default=False,
    )
    author = models.CharField(
        _('feed author'),
        blank=True,
        max_length=255,
    )
    created = models.DateTimeField(
        _('Date of submition'),
        blank=True,
        null=True,
        auto_now_add=True,
    )
    feedentry_count = models.IntegerField(
        blank=True,
        default=0,
    )
    active_feedentry_count = models.IntegerField(
        blank=True,
        default=0,
    )

    def __unicode__(self):
        return self.title

    @app_models.permalink
    def get_absolute_url(self):
        return ('feedz-feed', 'feedz.urls', (self.id, ), {})

    def site_hostname(self):
        return urlsplit(self.site_url).hostname

    class Meta:
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')

    def author_or_title(self):
        return self.author or self.title

    def update_counts(self):
        self.entry_count = self.entrys.count()
        self.active_post_count = self.posts.filter(active=True).count()
        self.save()


class FeedEntry(models.Model):
    feed = models.ForeignKey(
        Feed,
        verbose_name=_('feed'),
        related_name='posts',
    )
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    link = models.CharField(
        _('link'),
        max_length=255,
    )
    summary = models.TextField(
        _('summary'),
        blank=True,
    )
    content = models.TextField(
        _('content'),
        blank=True,
    )
    created = models.DateTimeField(
        _('creation time'),
    )
    guid = models.CharField(
        _('identifier'),
        max_length=255,
        unique=True,
    )
    #tags = TagField()
    active = models.BooleanField(
        _('active'),
        blank=True,
        default=True,
    )

    objects = models.Manager()
    active_objects = ActivePostManager()

    class Meta:
        ordering = ['-created']
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse('feedzilla_post', args=[self.id])
        return self.link

    def summary_uncached(self):
        return clean_html(self.content[:FEED_SUMMARY_SIZE])


class Request(models.Model):
    url = models.CharField(
        _('request url'),
        max_length=255,
        unique=True,
    )
    title = models.CharField(
        _('request title'),
        max_length=255,
    )
    author = models.CharField(
        _('request author'),
        blank=True,
        max_length=50,
    )
    feed_url = models.CharField(
        _('feed url'),
        blank=True,
        max_length=255,
        help_text=u'RSS/Atom feed url')
    created = models.DateTimeField(
        _('Creation date'),
        auto_now_add=True,
    )

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-created']
        verbose_name = _('Request')
        verbose_name_plural = _('Requests')
