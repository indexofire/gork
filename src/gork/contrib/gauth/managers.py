# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class GUserManager(BaseUserManager):
    """
    GUser Manager for create user and superuser.

    You can use:
        u = self.model(...)
        password = u.make_random_password()
        u.set_password(password)
    to create a new password for users.
    """
    def create_user(self, username, email=None, password=None, nickname=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, password and nickname.
        """
        # to record user joined date.
        now = timezone.now()

        if not username:
            raise ValueError('The given username must be set')

        email = GUserManager.normalize_email(email)
        u = self.model(
            username=username,
            email=email,
            nickname=username,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        # use set_password to create password.
        u.set_password(password)
        u.save(using=self._db)
        return u

    def create_superuser(self, username, email, password, **extra_fields):
        """Create superuser"""
        u = self.create_user(username, email, password, **extra_fields)
        u.nickname = username
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class EmailConfirmationManager(models.Manager):

    def delete_expired_confirmations(self):
        for confirmation in self.all():
            if confirmation.key_expired():
                confirmation.delete()
