# -*- coding: utf-8 -*-
from django import forms


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Request

    def clean_url(self):
        url = self.cleaned_data['url']
        try:
            Request.objects.get(url=url)
        except Request.DoesNotExist:
            return url
        else:
            raise forms.ValidationError(_('This address has been already submitted.'))
