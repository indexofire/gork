# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from feedz.models import Feed, FeedEntry, Request
from feedz.utils import html_link


class FeedAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'active',
        'last_checked',
        'author',
        'admin_feed_url',
        'admin_site_url',
        'active_feedentry_count',
        'feedentry_count',
        'created',
    ]
    search_fields = ['title', 'site_url']

    def admin_feed_url(self, obj):
        return html_link(obj.feed_url)
    admin_feed_url.allow_tags = True
    admin_feed_url.short_description = _('Feed')

    def admin_site_url(self, obj):
        return html_link(obj.site_url)
    admin_site_url.allow_tags = True
    admin_site_url.short_description = _('Site')


class FeedEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'created', 'active',
                    'admin_post_link']
    list_filter = ['feed']
    search_fields = ['title', 'link', 'feed__title']

    def admin_post_link(self, obj):
        return html_link(obj.link)
    admin_post_link.allow_tags = True
    admin_post_link.short_description = _('Post link')


class RequestAdmin(admin.ModelAdmin):
    list_display = ['url', 'title', 'author', 'created', 'process_link']

    def process_link(self, obj):
        args = {
            'title': obj.title,
            'site_url': obj.url,
            'feed_url': obj.feed_url,
            'author': obj.author,
        }
        url = '%s?%s' % (reverse('admin:feedzilla_feed_add'), urlencode(args))
        return u'<a href="%s">%s</a>' % (url, _('Process'))

    process_link.allow_tags = True
    process_link.short_description = _('Process')

admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedEntry, FeedEntryAdmin)
admin.site.register(Request, RequestAdmin)
