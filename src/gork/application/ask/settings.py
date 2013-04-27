# -*- coding: utf-8 -*-
import string
from datetime import timedelta
from django.conf import settings


# set question's render parser
ASK_CONTENT_DEFAULT_PARSER = (
    ('rst', 'resturctured text'),
    ('markdown', 'markdown'),
    ('texttile', 'texttile'),
)
ASK_CONTENT_PARSER = getattr(settings, 'ASK_CONTENT_DEFAULT_PARSER', ASK_CONTENT_DEFAULT_PARSER)

# The name of the editor group
MODERATOR_GROUP = 'mod_group'

# the minimal reputation needed to
MIN_REP = 1

# post/user score change during an upvote
POST_SCORE_CHANGE = 1
USER_SCORE_CHANGE = 1
# this is how many votes can be cast per session
MAX_VOTES_PER_SESSION = 1


# in seconds, the time intervals to reset vote limit
VOTE_SESSION_LENGTH = 60
VOTE_SESSION_LENGTH = timedelta(seconds=VOTE_SESSION_LENGTH)

FIRST_SESSION = 'first-session'
LASTSORT_SESSION = 'last-sort'

# Add at the end
POST_QUESTION, POST_ANSWER, POST_COMMENT, POST_TUTORIAL, POST_BLOG, POST_FORUM, POST_NEWS, POST_REVIEW, POST_TOOL, POST_FIXME, POST_VIDEO, POST_JOB, POST_PUBLICATION, POST_TIP, POST_OTHER = range(1, 16)

POST_TYPES = (
    (POST_ANSWER, 'Answer'),
    (POST_COMMENT, 'Comment'),
    (POST_QUESTION, 'Question'),
    (POST_TUTORIAL, 'Tutorial'),
    (POST_TIP, 'Tip'),
    (POST_BLOG, 'Blog'),
    (POST_FORUM, 'Forum'),
    (POST_NEWS, 'News'),
    (POST_REVIEW, 'Review'),
    (POST_TOOL, 'Tool'),
    (POST_VIDEO, 'Video'),
    (POST_FIXME, 'FixMe'),
    (POST_JOB, 'Job'),
    (POST_PUBLICATION, 'Research Paper'),
)

# direct mapping for quick lookups
POST_MAP = dict(POST_TYPES)

# reverse mapping for quick lookups
POST_REV_MAP = dict((y.lower(), x) for (x, y) in POST_MAP.items())

# entities that will be displayed on the navigation bar
POST_NAV_BAR = []
POST_NAV_BAR_LOWER = map(string.lower, POST_NAV_BAR)

# the valid sort orders
SORT_MAP = dict(
    rank="-rank", views="-views", creation="-creation_date",
    activity="-lastedit_date", votes="-full_score", answers="-answer_count",
)

# valid pill entries
VALID_PILLS = set("mytags all news questions unanswered tutorials tools \
    videos jobs planet".split())

# valid tab entries
VALID_TABS = set("recent planet sticky".split()) | VALID_PILLS

# posts that only have content, no title or tags
POST_CONTENT_ONLY = set([POST_ANSWER, POST_COMMENT])

# these posts must have parent
POST_SUBLEVEL = set([POST_ANSWER, POST_COMMENT])

# main level posts
POST_EXCLUDE = set([POST_ANSWER, POST_COMMENT, POST_BLOG])

# toplevel posts may stand alone and must have title and tags
POST_TOPLEVEL = set(POST_MAP.keys()) - POST_SUBLEVEL

# posts the will go under forum
POST_FORUMLEVEL = set((POST_FORUM, POST_NEWS, POST_REVIEW))

# the session key that stores new post counts
SESSION_POST_COUNT = 'session-post-count'
SESSION_VIEW_COUNT = 'view-count'

# the type of messages that the system maintains
NOTE_USER, NOTE_MODERATOR, NOTE_ADMIN, NOTE_AWARD, NOTE_SITE = range(1, 6)
NOTE_TYPES = (
    (NOTE_USER, 'User'),
    (NOTE_MODERATOR, 'Moderator'),
    (NOTE_ADMIN, 'Admin'),
    (NOTE_AWARD, 'Award'),
    (NOTE_SITE, "Site"),
)

# user types
USER_NEW, USER_MEMBER, USER_MODERATOR, USER_ADMIN, USER_BLOG, USER_SPECIAL, = range(1, 7)
USER_TYPES = (
    (USER_NEW, 'New'),
    (USER_MEMBER, 'Member'),
    (USER_MODERATOR, 'Moderator'),
    (USER_ADMIN, 'Administrator'),
    (USER_BLOG, 'Blog'),
    (USER_SPECIAL, 'Special'),
)

# user status types
USER_ACTIVE, USER_SUSPENDED, USER_BANNED = 1, 2, 3
USER_STATUS_TYPES = (
    (USER_ACTIVE, 'Active'),
    (USER_SUSPENDED, 'Suspended'),
    (USER_BANNED, 'Banned'),
)

# post status types
POST_OPEN, POST_CLOSED, POST_DELETED = 100, 200, 300
POST_STATUS_TYPES = (
    (POST_OPEN, 'Open'),
    (POST_CLOSED, 'Closed'),
    (POST_DELETED, 'Deleted'),
)

# the time between registering two post views
# from the same IP, in minutes
POST_VIEW_UPDATE = 30

# revision constants
REV_NONE, REV_CLOSE, REV_REOPEN, REV_DELETE, REV_UNDELETE = range(1000, 1005)
REV_ACTIONS = (
    (REV_NONE, ''), (REV_CLOSE, 'Close'), (REV_REOPEN, 'Reopen'),
    (REV_DELETE, 'Delete'), (REV_UNDELETE, 'Undelete')
)
REV_ACTION_MAP = dict(REV_ACTIONS)

# this stores the counts in the cache
CACHE_COUNT_KEY = "cache-count-key"

# moderation actions
USER_MODERATION, POST_MODERATION = 0, 1
USER_MOD_TYPES = [(USER_MODERATION, 'Usermod'), (POST_MODERATION, 'Postmod')]

# voting related constants
VOTE_UP, VOTE_DOWN, VOTE_ACCEPT, VOTE_BOOKMARK = range(1, 5)
VOTE_TYPES = (
    (VOTE_UP, 'Upvote'),
    (VOTE_DOWN, 'Downvote'),
    (VOTE_ACCEPT, 'Accept'),
    (VOTE_BOOKMARK, 'Bookmark'),
)
OPPOSING_VOTES = {VOTE_UP: VOTE_DOWN, VOTE_DOWN: VOTE_UP}

BADGE_BRONZE, BADGE_SILVER, BADGE_GOLD = 0, 1, 2
BADGE_TYPES = (
    (BADGE_BRONZE, 'bronze'),
    (BADGE_SILVER, 'silver'),
    (BADGE_GOLD, 'gold'),
)

BETA_TESTER_BADGE = "Beta Tester"

TARGET_COUNT_MAP = {
    POST_NEWS: "News",
    POST_QUESTION: "Question",
    POST_TOOL: "Tool",
    POST_TUTORIAL: "Tutorial",
    POST_JOB: "Job",
    POST_BLOG: "Blog",
    POST_VIDEO: "Video",
    "unanswered": "Unanswered",
}

MIN_POST_SIZE = 6
MAX_POST_SIZE = 250000

# google analytics tracker and domain
GOOGLE_TRACKER = ""
GOOGLE_DOMAIN = ""

# needs to be turned on explicitly
CONTENT_INDEXING = True

# rank gains expressed in hours
POST_UPVOTE_RANK_GAIN = 1
POST_VIEW_RANK_GAIN = 0.1
BLOG_VIEW_RANK_GAIN = 0.1

# if this is set together with the DEBUG mode allows test logins
# don't turn it on in production servers!
SELENIUM_TEST_LOGIN_TOKEN = None

# no external authentication by default
# dictionary keyed by name containing the tuple of (secret key, template)
EXTERNAL_AUTHENICATION = {

}

# setting the session for multiple servers
SESSION_COOKIE_DOMAIN = ""

MIN_POST_SIZE = 15
MAX_POST_SIZE = 20000

RECENT_VOTE_COUNT = 10
RECENT_TAG_COUNT = 30
# set the tag names are to be displayed on the main page
IMPORTANT_TAG_NAMES = "rna-seq chip-seq assembly snp metagenomics vcf cnv mirna indel bwa bowtie bedtools biopython bioperl".split()


# the interval specified in hours
# that user activity throttling is computed over
TRUST_INTERVAL = 3

# how many posts may a new user make in a trust interval
# new user means a user that joined within a trust interval time
TRUST_NEW_USER_MAX_POST = 3

# how many posts may a trusted user make withing a trust in
TRUST_USER_MAX_POST = 15

# TEMPLATE LAYOUT,
# One may override these variables from the settings file
#

# this data governs the layout of the PILL_BAR
# bar name, link url, link name, counter key
ANON_PILL_BAR = [
    ("all", "", "Show&nbsp;All", ""),
    ("best", "show/best", "Popular", "Popular"),
    ("bookmarked", "show/bookmarked", "Bookmarked", "Bookmarked"),
    ("questions", "show/questions/", "Questions", "Question"),
    ("unanswered", "show/unanswered/", "Unanswered", "Unanswered"),
    ("howto", "show/howto/", "How To", "How To"),
    ("galaxy", "show/galaxy/", "Galaxy", "Galaxy"),
    ("forum", "show/forum/", "Forum", "Forum"),
    ("jobs", "show/jobs/", "Jobs", "Job"),
    ("planet", "show/planet/", "Planet", "Blog"),
]

USER_PILL_BAR = list(ANON_PILL_BAR)
USER_PILL_BAR.insert(1, ("mytags", "show/mytags/", "My&nbsp;Tags", ""))

#
# remapping the templates to local versions
# a row is the way a post is rendered on a page
# list below the templates to be loaded for a post type
# to reduce clutter there is a default mapper that
# for missing types attempts to map each type to rows/row.type.html
# django template lookup rules apply
#
TEMPLATE_ROWS = {
    'job': "rows/row.job.html",
}

POSTS_PER_PAGE = 20


from django.conf import settings

__CURR_DIR = settings.PROJECT_ROOT
#HOME_DIR      = path(__CURR_DIR )
#DATABASE_DIR  = path(HOME_DIR, 'db')
#DATABASE_NAME = path(DATABASE_DIR, 'biostar.db')
#TEMPLATE_DIR  = path(HOME_DIR, 'main', 'templates')
#STATIC_DIR    = path(HOME_DIR, 'static')
EXPORT_DIR    = 'export'
#WHOOSH_INDEX  = path(HOME_DIR, 'db', 'index')
#PLANET_DIR    = path(HOME_DIR, 'db', 'planet')
