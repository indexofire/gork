# -*- coding: utf-8 -*-
from django import forms
from gform.models import BootstrapForm
from entrez.models import EntrezTerm


class AddTermForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = EntrezTerm
        exclude = ('owner', 'creation_date', 'lastedit_date', 'slug', 'unreads')
