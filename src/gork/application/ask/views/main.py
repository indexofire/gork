# -*- coding: utf-8 -*-
#from django.shortcuts import render
#from django.views.generic import ListView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import app_reverse
#from gauth.models import GUser
from gtag.models import Tag  # , TaggedItem
from ask.models import Post
from ask.forms import QuestionForm, AnswerForm, CommentForm
#from django.contrib.contenttypes.models import ContentType


def tag_list():
    #ct = ContentType.objects.get_for_model(Post)
    #return TaggedItem.objects.filter(content_type=ct).select_related()
    return Tag.objects.all().select_related()


def tag_post(request, tag):
    qs = Post.objects.filter(tags__name__in=[tag]).select_related()
    return 'ask/ask_tag_post.html', {
        'qs': qs,
        'tags': tag_list(),
    }


def ask_index(request):
    qs = Post.objects.filter(level=0).select_related()
    print tag_list()
    return 'ask/ask_index.html', {
        'qs': qs,
        'tags': tag_list(),
    }


def show_post(request, id):
    """ Question display and quick reply. """
    q = Post.objects.select_related().get(id=id)
    form = AnswerForm
    answers = q.get_descendants().select_related()
    return 'ask/ask_detail.html', {
        'q': q,
        'nodes': answers,
        'tags': tag_list(),
        'form': form(),
    }
        #else:
        #    return 'ask/ask_no_permission.html', {
        #        'error': _(u"You have no permission to view the question.")
        #    }


@login_required()
def reply_question(request, id):
    form_class = AnswerForm
    post = Post.objects.select_related().get(id=id)
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            answer = Post.objects.create(
                author=request.user,
                content=form.cleaned_data['content'],
                title=post.title + '\'s answer by ' + request.user.username,
                parent=Post.objects.select_related().get(id=id),
                creation_date=timezone.now(),
                lastedit_date=timezone.now(),
                lastedit_user=request.user,
                type=2
            )
            tags = form.cleaned_data['tags'].replace(u'，', ',').replace(' ', '').split(',')
            for tag in tags:
                answer.tags.add(tag)
            answer.save()

            return HttpResponseRedirect(app_reverse("ask-detail", 'ask.urls', args=id))
        else:
            return 'ask/ask_new_post.html', {
                'form_error': form.errors,
                'q': post,
                'nodes': post.get_descendants().select_related(),
                'tags': tag_list(),
                'form': form_class(),
            }
    else:
        form = form_class()

    return 'ask/ask_new_post.html', {'form': form}


@login_required()
def comment_post(request, id):
    form_class = CommentForm
    post = Post.objects.select_related().get(id=id)
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            comment = Post.objects.create(
                author=request.user,
                content=form.cleaned_data['content'],
                title=post.title + '\'s comment by ' + request.user.username,
                parent=post,
                creation_date=timezone.now(),
                lastedit_date=timezone.now(),
                lastedit_user=request.user,
                type=3
            )
            tags = post.tags.all()
            for tag in tags:
                comment.tags.add(tag)
            comment.save()

            return HttpResponseRedirect(app_reverse("ask-detail", 'ask.urls'))

        else:
            return 'ask/ask_detail.html', {'form_errors': form.errors}


@login_required()
def ask_question(request):
    form_class = QuestionForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            question = Post.objects.create(
                author=request.user,
                content=form.cleaned_data['content'],
                title=form.cleaned_data['title'],
                creation_date=timezone.now(),
                lastedit_date=timezone.now(),
                lastedit_user=request.user,
                type=1
            )
            tags = form.cleaned_data['tags'].replace(u'，', ',').replace(' ', '').split(',')
            for tag in tags:
                question.tags.add(tag.replace(' ', ''))
            question.save()

            return HttpResponseRedirect(app_reverse("ask-index", 'ask.urls'))
    else:
        form = QuestionForm()
        return 'ask/ask_new_post.html', {'form': form}


'''
def index(request):
    """ QA landing page views. """
    user = request.user
    auth = user.is_authenticated()

    # parse the date request
    since = request.GET.get('since', DATE_FILTER[0]).lower()

    # set the last active tab
    sess.set_tab(tab)

    # get the numerical value for these posts
    post_type = POST_TYPE_MAP.get(tab, tab)

    # override the sort order if the content so requires
    sort_type = 'creation' if tab == 'recent' else sort_type

    # this here needs to be reworked TODO
    if tab == "best":
        sort_type = "votes"
        since = request.GET.get('since', 'this week')
        messages.info(request, "Most <b>upvoted</b> active posts of <b>%s!</b>" % since)

    elif tab == "bookmarked":
        sort_type = "bookmark"
        since = request.GET.get('since', 'this month')
        messages.info(request, "Most <b>bookmarked</b> active posts of <b>%s!</b>" % since)

    # the params object will carry
    layout = const.USER_PILL_BAR if auth else const.ANON_PILL_BAR

    # wether to show the type of the post
    show_type = post_type in ('all', 'recent')

    show_search = True

    if tab in VALID_PILLS:
        tab, pill = "posts", tab
    else:
        tab, pill = tab, ""

    params = html.Params(
        tab=tab,
        pill=pill,
        sort=sort_type,
        sort_choices=SORT_CHOICES,
        date_filter=DATE_FILTER,
        since=since,
        layout=layout,
        show_type=show_type,
        title="Bioinformatics Answers",
        show_search=show_search)

    # this will fill in the query (q) and the match (m)parameters
    params.parse(request)

    # returns the object manager that contains all or only visible posts
    posts = get_post_manager(request)

    # filter posts by type
    posts = filter_by_type(request=request, posts=posts, post_type=post_type)

    # apply date filtering
    posts = filter_by_date(request=request, posts=posts, since=since)

    # reduce SQL query count by preselecting data that will be displayed
    posts = posts.select_related('author', 'author__profile', 'lastedit_user', 'lastedit_user__profile')

    # sticky is not active on recent and all pages
    sticky = (tab != 'recent') and (pill not in ('all', "best", "bookmarked"))

    # order may change if it is invalid search
    posts = apply_sort(request=request, posts=posts, order=sort_type, sticky=sticky)

    # get the counts for the session
    counts = sess.get_counts(post_type)
    page = get_page(request, posts, per_page=const.POSTS_PER_PAGE)

    # save the session
    sess.save()

    # try to set a more informative title
    title_map = dict(
        questions="Bioinformatics Questions",
        unanswered="Unanswered Questions",
        tutorials="Bioinformatics Tutorials",
        jobs="Bioinformatics Jobs",
        videos="Bioinformatics Videos",
        news='Bioinformatics News',
        tools="Bioinformatics Tools",
        recent="Recent bioinformatics posts",
        planet="Bioinformatics Planet",
        galaxy="Galaxy on Biostar",
        bookmarked="Most bookmarked",
    )

    params.title = title_map.get(pill) or title_map.get(tab, params.title)

    return html.template(request, name='gqanda/index.html', page=page, params=params, counts=counts)
'''
