# -*- coding: utf-8 -*-
import re
import pytz
import datetime
from django.conf import settings
from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from feincms.extensions import ExtensionsMixin
from gauth.managers import GUserManager, EmailConfirmationManager
from gauth.settings import *


class GUser(AbstractBaseUser, PermissionsMixin, ExtensionsMixin):
    """
    Extensible User models.

    Put `AUTH_USER_MODEL = 'gauth.GUser'` in your project's
    settings.py file. Then using profile extensions to extend
    user's profile. i.e:

    AUTH_USER_MODEL = 'gauth.GUser'
    AUTH_EXTENSIONS = (
        'gauth.extensions.avatar',
        'gauth.extensions.portfolio',
        ...
    )

    You can also add or delete the AUTH_EXTENSIONS by running
    `south migrate` to update database schema.
    """

    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
        db_index=True,
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ],
    )
    nickname = models.CharField(
        _('nickname'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('Showed in site. any characters will be valid'),
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        unique=True,
        db_index=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField(
        _('sign up date'),
        default=timezone.now,
    )

    objects = GUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        app_label = "gauth"
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __unicode__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(GUser, self).save(*args, **kwargs)

    def now(self):
        """
        Returns a timezone aware datetime localized to the user's timezone.
        """
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
        timezone = settings.TIME_ZONE if not self.timezone else self.timezone
        return now.astimezone(pytz.timezone(timezone))

    def localtime(self, value):
        """
        Given a datetime object as value convert it to the timezone of
        the account.
        """
        timezone = settings.TIME_ZONE if not self.timezone else self.timezone
        if value.tzinfo is None:
            value = pytz.timezone(settings.TIME_ZONE).localize(value)
        return value.astimezone(pytz.timezone(timezone))

    def get_full_name(self):
        """
        fake get_full_name to avoid some 3rd app can not find it.
        """
        if self.nickname:
            return self.nickname
        return self.username

    def get_short_name(self):
        """
        fack get_short_name to avoid some 3rd app can not find it.
        """
        if self.nickname:
            return self.nickname
        return self.username

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        return

    def get_absolute_url(self):
        return self.username

GUser.register_extensions(*GAUTH_USER_EXTENSIONS)


class EmailConfirmation(models.Model):
    """
    Hash key for registered new users confirmation
    """
    user = models.ForeignKey(GUser)
    #email_address = models.ForeignKey(EmailAddress)
    created = models.DateTimeField(default=timezone.now())
    sent = models.DateTimeField(null=True)
    key = models.CharField(max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def __unicode__(self):
        return u"confirmation for %s" % self.email_address

    @property
    def email_address(self):
        return self.user.email

    @classmethod
    def create(cls, email_address):
        key = random_token([self.email_address])
        return cls._default_manager.create(email_address=self.email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent + datetime.timedelta(days=GAUTH_EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def confirm(self):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()
            signals.email_confirmed.send(sender=self.__class__, email_address=email_address)
            return email_address

    def send(self, **kwargs):
        current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        activate_url = u"%s://%s%s" % (
            protocol,
            unicode(current_site.domain),
            reverse("account_confirm_email", args=[self.key])
        )
        ctx = {
            "email_address": self.email_address,
            "user": self.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": self.key,
        }
        subject = render_to_string("gauth/email/email_confirmation_subject.txt", ctx)

        # remove superfluous line breaks
        subject = "".join(subject.splitlines())
        message = render_to_string("gauth/email/email_confirmation_message.txt", ctx)
        send_mail(subject, message, GAUTH_DEFAULT_FROM_EMAIL, [self.email_address.email])
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__, confirmation=self)
