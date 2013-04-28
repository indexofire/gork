# -*- coding: utf-8 -*-
#import re
#from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
#from django.db.models import Count
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins
from common.pagination import paginate
from common.forms import build_form
from tagging.models import Tag, TaggedItem
from feedz.models import Feed, FeedEntry
from feedz.forms import AddBlogForm
from feedz.settings import *


def index(request):
    qs = FeedEntry.active_objects.all().select_related('feed')
    page = paginate(qs, request, settings.FEEDZILLA_PAGE_SIZE)
    return ('feedz/feedz_index.html', {
        'page': page, }
    )


def tag(request, tag_value):
    tag = get_object_or_404(Tag, name=tag_value)
    qs = TaggedItem.objects.get_by_model(FeedEntry, tag).filter(active=True).order_by('-created')
    page = paginate(qs, request, FEED_PAGE_SIZE)

    return ('feedz/feedz_tag.html', {
        'tag': tag,
        'page': page, }
    )


def source_list(request):

    feeds = Feed.objects.all()

    cursor = connection.cursor()
    cursor.execute("""
        SELECT f.id, COUNT(*)
        FROM feedz_feed f
        JOIN feedz_feedentry p
            ON p.feed_id = f.id AND p.active
        GROUP BY f.id
    """)

    count_map = dict(cursor.fetchall())
    for feed in feeds:
        feed.post_count = count_map.get(feed.pk, 0)

    return ('feedz/feedz_source_list.html', {
        'feed': feeds, }
    )


def search(request):
    query = request.GET.get('query', '')
    min_limit = 2
    if len(query) < min_limit:
        posts = []
        message = _('Your query is shorter than %d characters') % min_limit
    else:
        posts = FeedEntry.active_objects.filter(content__icontains=query)
        message = ''

    page = paginate(posts, request, settings.FEEDZILLA_PAGE_SIZE)

    return ('feedz/feedz_search.html', {
        'page': page,
        'message': message,
        'query': query, }
    )


def submit_blog(request):
    form = build_form(AddBlogForm, request)
    if form.is_valid():
        obj = form.save()
        success = True
        body = _('New submission for the planet: %s') % obj.url
        mail_admins(_('%s: new submission') % settings.FEEDZILLA_SITE_TITLE, body)
    else:
        success = False
    return ('feedz/feedz_submit_blog.html', {
        'form': form,
        'success': success, }
    )
