# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from know.plugins.images.models import Image, ImageRevision


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            revisions = ImageRevision.objects.filter(plugin=self.instance)
            self.fields['current_revision'].queryset = revisions
        else:
            self.fields['current_revision'].queryset = ImageRevision.objects.get_empty_query_set()
            self.fields['current_revision'].widget = forms.HiddenInput()


class ImageRevisionInline(admin.TabularInline):
    model = ImageRevision
    extra = 1
    fields = ('image', 'locked', 'deleted')


class ImageAdmin(admin.ModelAdmin):
    form = ImageForm
    inlines = (ImageRevisionInline,)

admin.site.register(Image, ImageAdmin)
