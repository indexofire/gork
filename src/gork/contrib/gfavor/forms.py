# -*- coding: utf-8 -*-
from django import forms
from gfavor.models import Favorite


class DeleteFavoriteForm(forms.ModelForm):
    """
    base class for deleting favorite instance

    you may extend this form to provide additional
    validation rules (checkboxes, captcha, etc...)
    """

    class Meta:
        model = Favorite
        fields = ('id',)

    def save(self, commit=True):
        """
        Simply deletes bound instance and returns instance.
        If commit is set to False, does nothing.
        """

        if commit:
            self.instance.delete()
        return self.instance
