# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import permalink
from mptt.models import MPTTModel, TreeForeignKey
from gtag.managers import TaggableManager
#from taggit import *
from ask.managers import OpenManager, AllManager
from ask import settings as app_settings


class Post(MPTTModel):
    """
    Ask application: a post is a question or a answer.
    """

    # post's author which is a foreignkey from project user.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_(u'Who ask or answer the question'),
        related_name='author',
    )
    # post's content which is normal text as default
    content = models.TextField(
        'Content Markup',
        null=False,
        blank=False,
        max_length=25000,
    )

    # post's content which will be render by user.
    content_parser = models.CharField(
        choices=app_settings.ASK_CONTENT_PARSER,
        default='text',
        max_length=30,
    )

    # this is the sanitized HTML for display
    content_html = models.TextField(
        blank=True,
    )

    # post tile
    title = models.CharField(
        max_length=200,
        help_text=_(u'Title of Question or Answer'),
    )

    # post slug
    slug = models.SlugField(
        blank=True,
        max_length=200,
    )

    # The tag value is the canonical form of the post's tags
    #tag_val = models.CharField(max_length=200, blank=True,)

    # The tag set is built from the tag string and used only for fast filtering
    #tag_set = models.ManyToManyField(Tag, blank=True,)

    tags = TaggableManager()

    # the number of post views by users.
    views = models.IntegerField(
        default=0,
        blank=True,
        db_index=True,
    )

    # the number of post score by users.
    score = models.IntegerField(
        default=0,
        blank=True,
        db_index=True,
    )

    # the sum of the score of post and it's answers.
    full_score = models.IntegerField(
        default=0,
        blank=True,
        db_index=True,
    )

    # post created date.
    creation_date = models.DateTimeField(
        db_index=True,
    )

    # post edit date.
    lastedit_date = models.DateTimeField(
        db_index=True,
    )

    # post edit by who latest.
    lastedit_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='editor',
    )

    # keeps track of which posts have changed
    changed = models.BooleanField(
        default=True,
        db_index=True,
    )

    # post status: active, closed, deleted
    status = models.IntegerField(
        choices=app_settings.POST_STATUS_TYPES,
        default=app_settings.POST_OPEN,
    )

    # the type of the post
    type = models.IntegerField(
        choices=app_settings.POST_TYPES,
        db_index=True,
    )

    # used to display a context the post was created in
    context = models.TextField(
        max_length=1000,
        default='',
    )

    # this will maintain the ancestor/descendant relationship bewteen posts
    root = TreeForeignKey(
        'self',
        related_name="descendants",
        null=True,
        blank=True,
    )

    # this will maintain parent-child replationships between posts
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
    )

    # the number of answer that a post has
    answer_count = models.IntegerField(
        default=0,
        blank=True,
    )

    # bookmark count
    book_count = models.IntegerField(
        default=0,
        blank=True,
    )

    # stickiness of the post
    sticky = models.IntegerField(
        default=0,
        db_index=True,
    )

    # wether the post has accepted answers
    accepted = models.BooleanField(
        default=False,
        blank=True,
    )

    # used for post with a linkout
    url = models.URLField(
        default='',
        blank=True,
    )

    # relevance measure, initially by timestamp, other rankings measures
    rank = models.FloatField(
        default=0,
        blank=True,
    )

    # define all posts which will be displayed by admin or some kind
    # of special users like super moderator.
    all_posts = AllManager()

    # define posts which request.user has permission to view. all kinds
    # of hidden or deleted posts will not be display.
    open_posts = OpenManager()

    # default manager in django model
    objects = models.Manager()

    class MPTTMeta:
        order_insertion_by = ['full_score', 'creation_date']

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        """ Return the absolute url of a post. """
        #if self.top_level:
        #    url = "/p/%d/" % (self.id)
        #else:
        #    url = "/p/%d/#%d" % (self.root.id, self.id)

        # some objects have external links
        #if self.url:
        #    url = "/linkout/%s/" % self.id

        #return url
        if self.url:
            return ('link-detail', 'ask.urls', (), {'id': self.id})
        return ('ask-detail', 'ask.urls', (), {'id': self.id, })

    def answer_only(self):
        """The post should only have answers associate with it"""
        return self.type == app_settings.POST_QUESTION

    def set_tags(self):
        pass
    """
    def set_tags(self):
        if self.type not in POST_CONTENT_ONLY:
            # save it so that we can set the many2many fiels
            self.tag_set.clear()
            tags = [Tag.objects.get_or_create(name=name)[0] for name in self.get_tag_names()]
            self.tag_set.add(*tags)
        self.save()
    """

    def get_title(self):
        """ Return the title and a qualifier """
        title = self.title
        if self.deleted:
            title = "%s [deleted ]" % self.title
        elif self.closed:
            title = "%s [closed]" % self.title
        return "%s" % title

    @property
    def top_level(self):
        return self.type in app_settings.POST_TOPLEVEL

    @property
    def closed(self):
        return self.status == app_settings.POST_CLOSED

    @property
    def open(self):
        return self.status == app_settings.POST_OPEN

    @property
    def deleted(self):
        return self.status == app_settings.POST_DELETED

    @property
    def get_status(self):
        """Main status of a post"""
        if self.deleted:
            return 'deleted'
        elif self.closed:
            return 'closed'
        else:
            return ''

    @property
    def get_label(self):
        """Secondary status of open posts"""
        if self.answer_count == 0:
            return 'unanswered'
        elif self.accepted:
            return 'accepted'
        elif self.answer_count:
            return 'answered'
        else:
            return 'open'

    def get_tag_names(self):
        pass

    """
    def get_tag_names(self):
        tag_val = html.sanitize(self.tag_val)
        names = re.split('[ ,]+', tag_val)
        names = filter(None, names)
        return map(unicode, names)
    """

    def apply(self, dir):
        if self.type == app_settings.POST_ANSWER:
            self.parent.answer_count += dir
            self.parent.lastedit_date = self.creation_date
            self.parent.lastedit_user = self.author
            self.parent.save()

    def comments(self):
        """ Return post's comment """
        objects = Post.objects.filter(parent=self, type=app_settings.POST_COMMENT).select_related('author')
        return objects

    def set_rank(self):
        #self.rank = html.rank(self)
        pass

    def combine(self):
        """
        Returns a compact view that combines all parts of a post.
        Used in computing diffs between revisions
        """
        if self.type in app_settings.POST_CONTENT_ONLY:
            return self.content
        else:
            title = self.title
            content = self.content
            tag_val = self.tag_val
            return "TITLE:%s\n%s\nTAGS:%s" % (title, content, tag_val)


class Vote(models.Model):
    """
    >>> user, flag = User.objects.get_or_create(first_name='Jane', last_name='Doe', username='jane', email='jane')
    >>> post = Post.objects.create(author=user, type=POST_QUESTION, content='x')
    >>> vote = Vote(author=user, post=post, type=VOTE_UP)
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='votes')
    type = models.IntegerField(choices=app_settings.VOTE_TYPES, db_index=True)
    date = models.DateTimeField(db_index=True, auto_now=True)

    def apply(self, dir=1):
        """
        Applies a score and reputation changes upon a vote.
        Direction can be set to -1 to undo (ie delete vote)
        """

        post, root = self.post, self.post.parent
        if self.type == app_settings.VOTE_UP:
            post_score_change(post, amount=dir)
            user_score_change(post.author, amount=dir)

        if self.type == app_settings.VOTE_DOWN:
            post_score_change(post, amount=-dir)
            user_score_change(post.author, amount=-dir)

        if self.type == app_settings.VOTE_ACCEPT:
            post.accepted = root.accepted = (dir == 1)
            user_score_change(post.author, amount=1)
            post.save()
            root.save()
        """
        if self.type == app_settings.VOTE_BOOKMARK:
            post.book_count += dir
            post.save()
        """


def post_score_change(post, amount=1):
    """
    How post score changes with votes.
    Both the rank and the score changes
    """

    root = post.parent

    # post score increases
    post.score += amount
    post.full_score += amount

    print post.score, post.full_score

    if post != root:
        root.full_score += amount
        root.save()

    post.save()

    return post, post.root


def user_score_change(user, amount):
    """How user score changes with votes"""
    print user.username
    user.qa_score += amount
    user.save()


@transaction.commit_on_success
def insert_vote(post, user, vote_type):
    """Applies a vote. Applying an existing vote type removes it"""

    # due to race conditions (user spamming vote button) multiple votes may register
    # this removes votes with the metioned type
    votes = Vote.objects.filter(post=post, author=user, type=vote_type)
    if votes:
        vote = votes[0]
        for vote in votes:
            vote.delete()
        msg = '%s removed' % vote.get_type_display()
        return vote, msg

    # remove opposing votes
    opposing = app_settings.OPPOSING_VOTES.get(vote_type)
    if opposing:
        for vote in Vote.objects.filter(post=post, author=user, type=opposing):
            vote.delete()
            post = vote.post  # this reference now has been changed

    vote = Vote.objects.create(post=post, author=user, type=vote_type)
    vote.apply()
    vote.save()
    msg = '%s added' % vote.get_type_display()
    return vote, msg
