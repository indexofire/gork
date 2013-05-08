# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth import authenticate
#from django.utils.encoding import force_text
from gauth.settings import SOCIAL_CHOICES


class SocialApp(models.Model):
    provider = models.CharField(max_length=30, choices=SOCIAL_CHOICES)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=100, help_text='App ID, or consumer key')
    key = models.CharField(max_length=100, blank=True, help_text='API Key')
    secret = models.CharField(max_length=100,help_text='API secret, client secret, or consumer secret')

    def __str__(self):
        return self.name

class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    provider = models.CharField(max_length=30, choices=SOCIAL_CHOICES)
    # Just in case you're wondering if an OpenID identity URL is going
    # to fit in a 'uid':
    #
    # Ideally, URLField(max_length=1024, unique=True) would be used
    # for identity.  However, MySQL has a max_length limitation of 255
    # for URLField. How about models.TextField(unique=True) then?
    # Well, that won't work either for MySQL due to another bug[1]. So
    # the only way out would be to drop the unique constraint, or
    # switch to shorter identity URLs. Opted for the latter, as [2]
    # suggests that identity URLs are supposed to be short anyway, at
    # least for the old spec.
    #
    # [1] http://code.djangoproject.com/ticket/2495.
    # [2] http://openid.net/specs/openid-authentication-1_1.html#limits

    uid = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    extra_data = JSONField(default='{}')

    class Meta:
        unique_together = ('provider', 'uid')

    def authenticate(self):
        return authenticate(account=self)

    def __unicode__(self):
        return self.user.nickname

    def get_profile_url(self):
        return self.user.get_absolute_url()

    def get_avatar_url(self):
        return self.user.avatar
