# -*- coding: utf-8 -*-
try:
    import cPickle as pickle
except:
    import pickle
from base64 import b64decode
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from feincms.content.application.models import app_reverse
from pows.apps.account.models import Profile
from pows.apps.forum.managers import TopicManager
from pows.apps.attachment.models import Attachment


__all__ = [
    'Forum',
    'Thread',
    'Topic',
    'Reply',
]


class Forum(models.Model):
    """
    Forum is a collection of topics which used to divid topics into different sorts.
    """
    name = models.CharField(_('Forum Name'), max_length=255)
    description = models.TextField(_('Description'), help_text='Short description of this forum', blank=True, max_length=400)
    moderators = models.ManyToManyField(Profile, blank=True, null=True, verbose_name=_('Moderators'))
    ordering = models.PositiveIntegerField(_('Ordering'), blank=False, default=1)
    created = models.DateTimeField(_('Created Time'), blank=True, auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated Time'), blank=True, null=True)

    class Meta:
        ordering = ['ordering']
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    def __unicode__(self):
        return self.name

    def count_nums_post(self):
        return self.topic_set.all().aggregate(Sum('num_replies'))['num_replies__sum'] or 0

    def get_last_post(self):
        if not self.last_post:
            return {}
        return pickle.loads(b64decode(self.last_post))

    @property
    def get_topic_number(self):
        return self.topic_set.all().count()

    @property
    def get_thread_number(self):
        return self.thread_set.all().count()
        #return self.thread_set.all().aggregate(Sum('num_replies'))['num_replies__sum'] or 0

    @models.permalink
    def get_absolute_url(self):
        return app_reverse('forum-forum', 'pows.apps.forum.urls', {
            'forum_pk': self.pk,
        })


class Thread(models.Model):
    """
    Abstract models which could be a topic or a reply.
    """
    forum = models.ForeignKey(Forum, verbose_name=_('Forum'))
    author = models.ForeignKey(Profile)
    author_ip = models.IPAddressField(_('Author\'s IP'), blank=False, default='0.0.0.0')
    created = models.DateTimeField(_('Created Time'), blank=False, auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated Time'), blank=True, null=True)
    attachment = models.ManyToManyField(Attachment, blank=True)
    content = models.TextField()

    class Meta:
        abstract = True
        ordering = ['-created']
        get_latest_by = 'created'
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    def __unicode__(self):
        return self.pk

    @models.permalink
    def get_absolute_url(self):
        return app_reverse('forum-post', 'pows.apps.forum.urls', kwargs={
            'post_id': self.pk,
        })

    def render(self):
        self.content = ''


class Topic(Thread):
    """ A topic model for reply sets. """
    subject = models.CharField(_('Title'), max_length=255, blank=False, null=False)
    reply_num = models.PositiveIntegerField(default=0)
    view_num = models.PositiveIntegerField(default=0)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    objects = TopicManager()

    class Meta:
        ordering = ['-created']
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __unicode__(self):
        return self.subject

    def get_reply_number(self):
        pass

    def get_view_number(self):
        pass


class Reply(Thread):
    """ A reply model of a topic. """
    topic = models.ForeignKey(Topic, verbose_name=_('Topic'))

    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
        ordering = ['-created']
        get_latest_by = 'created'

    def __unicode__(self):
        return self.topic.subject