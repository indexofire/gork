# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions
from ask.settings import USER_TYPES, USER_NEW


class Extension(extensions.Extension):
    """
    Appication Extension of Q and A.
    """
    def handle_model(self):
        self.model.add_to_class(
            'qa_score',
            models.IntegerField(
                _('Q&A Score'),
                blank=True,
                default=0,
            ),
        )
        self.model.add_to_class(
            'date_visited',
            models.DateTimeField(
                _('Last visited'),
                auto_now_add=True,
                blank=True,
                null=True,
            ),
        )
        self.model.add_to_class(
            'scholar',
            models.TextField(
                default='',
                null=True,
                max_length=50,
                blank=True,
            ),
        )
        self.model.add_to_class(
            'user_type',
            models.IntegerField(
                choices=USER_TYPES,
                default=USER_NEW,
            ),
        )
        self.model.add_to_class(
            'about_me',
            models.TextField(
                null=True,
                blank=True,
                default='',
            ),
        )
        self.model.add_to_class(
            'about_me_html',
            models.TextField(
                null=True,
                blank=True,
                default='',
            ),
        )
        self.model.add_to_class(
            'bronze_badges',
            models.IntegerField(
                default=0,
            ),
        )
        self.model.add_to_class(
            'silver_badges',
            models.IntegerField(
                default=0,
            ),
        )
        self.model.add_to_class(
            'gold_badges',
            models.IntegerField(
                default=0,
            ),
        )
        self.model.add_to_class(
            'new_messages',
            models.IntegerField(
                default=0,
            ),
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(_('Q&A'), {
            'fields': ('qa_score', 'scholar', 'user_type', 'about_me'),
            'classes': ('collapse', )}
        )



