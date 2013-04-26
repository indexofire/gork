# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from ask.views import main, ajax


urlpatterns = patterns('',
    url(r'^$', main.ask_index, name='ask-index'),
    url(r'^q/(?P<id>\d+)/$', main.show_post, name='ask-detail'),
    url(r'^q/ask/$', main.ask_question, name='ask-question'),
    url(r'^q/(?P<id>\d+)/reply/$', main.reply_question, name='ask-reply'),
    # vote question or answers by ajax
    url(r'^vote/$', ajax.vote, name="ask-vote"),
    url(r'^tag/(?P<tag>.+)/$', main.tag_post, name='tag-post'),
    #url(r'^a/(?P<pid>\d+)/$', main.post_answer, name="new-answer"),
    url(r'^q/(?P<id>\d+)/comment/$', main.comment_post, name='comment-post'),
)
