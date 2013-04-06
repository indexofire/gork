# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class(
            'menu_additional_class',
            models.CharField(
                _('Menu Additional Class'),
                blank=True,
                null=True,
                max_length=50,
                default='',
            ),
        )
        self.model.add_to_class(
            'menu_additional_img',
            models.ImageField(
                _('Menu Additional Image'),
                blank=True,
                null=True,
                upload_to='%s/img/' % settings.MEDIA_URL
            ),
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(_('Menu Additional Class'), {
            'fields': ('menu_additional_class', 'menu_additional_img'),
            'classes': ('collapse', ), }
        )
