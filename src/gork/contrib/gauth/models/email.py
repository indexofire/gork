# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from gauth.managers import EmailConfirmationManager
from gauth import signals
from gauth.settings import *


class EmailConfirmation(models.Model):
    """
    Hash key for registered new users confirmation
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #email_address = user.email
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
        subject = render_to_string("auth/email/email_confirmation_subject.txt", ctx)

        # remove superfluous line breaks
        subject = "".join(subject.splitlines())
        message = render_to_string("auth/email/email_confirmation_message.txt", ctx)
        send_mail(subject, message, GAUTH_DEFAULT_FROM_EMAIL, [self.email_address.email])
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__, confirmation=self)
