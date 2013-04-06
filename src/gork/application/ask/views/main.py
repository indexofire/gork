# -*- coding: utf-8 -*-
#from django.shortcuts import render
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
from gtag.models import Tag
from ask.models import Post


def tag_list():
    return Tag.objects.all()


def ask_index(request):
    qs = Post.objects.filter(level=0)
    return 'ask/ask_index.html', {
        'qs': qs,
        'tags': tag_list(),
    }


def show_post(request, id):
    q = Post.objects.select_related().get(id=id)
    if request.user.has_perm('can_view', q):
        answers = q.get_descendants().select_related()
        return 'ask/ask_detail.html', {
            'q': q,
            'nodes': answers,
            'tags': tag_list(),
        }
    else:
        return 'ask/ask_no_permission.html', {
            'error': _(u"You have no permission to view the question.")
        }


class PostListView(ListView):
    model = Post
    template_name = 'ask/ask_index.html'

    def get_queryset(self):
        return Post.objects.all()


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