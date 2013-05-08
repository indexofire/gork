# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from gauth.views import *


urlpatterns = patterns(
    '',
    url(r'^$', AccountIndex.as_view(), name='gauth-index'),
    url(r'^(?P<pk>\d+)/$', AccountDetail.as_view(), name='gauth-detail'),
    url(r'^(?P<pk>\d+)/edit/$', AccountEdit.as_view(), name='gauth-edit'),
    #url(r'^(?P<pk>\d+)/delete/$', AccountDelete.as_view(), name='gauth-delete'),
    url(r'^signup/$', SignupView.as_view(), name='gauth-signup'),
    url(r'^login/$', LoginView.as_view(), name='gauth-login'),
    #url(r'^login/weibo/$', weibo_login, name='gauth-weibo-login'),
    #url(r"^login/$", login_ajax, name="gauth-login"),
    url(r"^logout/$", LogoutView.as_view(), name="gauth-logout"),
    url(r"^confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="gauth-confirm-email"),
    url(r"^password/change/$", ChangePasswordView.as_view(), name="gauth-password-change"),
    url(r"^password/reset/$", PasswordResetView.as_view(), name="gauth-password-reset"),
    url(r"^activate/$", activate_user, name="gauth-activate-user"),
    #url(r"^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$",
    #    PasswordResetTokenView.as_view(), name="gauth-password-reset-token"),
    #url(r"^settings/$", SettingsView.as_view(), name="gauth_settings"),
    #url(r"^delete/$", DeleteView.as_view(), name="gauth_delete"),
)
