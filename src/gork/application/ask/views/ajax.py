# -*- coding: utf-8 -*-
import json
import logging
import traceback
from functools import partial
from collections import defaultdict
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from main.server import html, notegen, auth
#from main.server.html import get_page
from ask.settings import *
from ask.models import Post, Vote, insert_vote


# activate logging
logger = logging.getLogger(__name__)


def json_response(adict, **kwd):
    """Returns a http response in JSON format from a dictionary"""
    return HttpResponse(json.dumps(adict), **kwd)


def ajax_msg(msg, status):
    return json_response(dict(status=status, msg=msg))

ajax_success = partial(ajax_msg, status='success')
ajax_error = partial(ajax_msg, status='error')


class ajax_error_wrapper(object):
    """used as decorator to trap/display  errors in the ajax calls"""
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwds):
        try:
            # first parameter is the request
            if args[0].method != 'POST':
                return ajax_error('POST method must be used.')

            if not args[0].user.is_authenticated():
                return ajax_error('You must be logged in to do that')

            value = self.f(*args, **kwds)
            return value
        except Exception, exc:
            traceback.print_exc()
            return ajax_error('Error: %s' % exc)


@ajax_error_wrapper
def vote(request):
    """Handles all voting on posts"""
    author = request.user

    # attempt to find the post and vote
    post_id = int(request.POST.get('post'))
    post = Post.objects.get(id=post_id)

    # get vote type
    type = request.POST.get('type')

    # remap to actual type
    type = dict(upvote=VOTE_UP, accept=VOTE_ACCEPT, bookmark=VOTE_BOOKMARK, downvote=VOTE_DOWN).get(type)

    if not type:
        return ajax_error('invalid vote type')

    # throttle on downvoting, TODO: make it better
    if type == VOTE_DOWN:
        return ajax_success('Downvote received!')

    if type in (VOTE_UP, VOTE_DOWN, VOTE_ACCEPT) and post.author == author:
        return ajax_error('You may not vote on your own post')

    if type == VOTE_ACCEPT and post.parent.author != author:
        return ajax_error('Only the original poster may accept an answer')

    # voting throttle
    from django.utils.timezone import utc

    past = datetime.utcnow().replace(tzinfo=utc) - VOTE_SESSION_LENGTH
    count = Vote.objects.filter(author=author, date__gt=past).count()
    avail = MAX_VOTES_PER_SESSION - count

    if avail <= 0:
        msg = "You ran out of votes ;-) there will more in a little while"
        return ajax_error(msg)
    else:
        vote, msg = insert_vote(post=post, user=author, vote_type=type)
        return ajax_success(msg)


@ajax_error_wrapper
def comment_delete(request, pid):

    user = request.user
    post = Post.objects.get(id=pid)

    # two conditions where a comment destruction may occur
    permit = user.can_moderate or (user == post.author)
    if not permit:
        return ajax_error('Permission denied')

    status = POST_DELETED if (post.status != POST_DELETED) else POST_OPEN
    url = post_moderate(request=request, post=post, user=user, status=status)

    if url == "/":
        return ajax_success("destroyed") # this is required by the UI
    else:
        return ajax_success("The comment status set to %s" % post.get_status_display() )

def tagcomplete(request):
    term = request.GET['term']
    tags = models.Tag.objects.filter(name__startswith=term).order_by('name')[:50]
    return HttpResponse(json.dumps([tag.name for tag in tags]))
