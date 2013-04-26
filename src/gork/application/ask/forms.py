# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
#from feincms.contrib.richtext import RichTextFormField
from gform.models import BootstrapForm
from ask.settings import POST_TYPES, MIN_POST_SIZE, MAX_POST_SIZE


P_TITLE, P_CONTENT, P_TAG = _('Post title'), _('Post content'), _('Post tags')


def valid_title(text):
    """Validates form input for title"""
    if text == P_TITLE:
        raise ValidationError('Please change the default title.')
    if len(text) < 5:
        raise ValidationError('Your title appears to be shorter than the minimum of five characters.')
    if len(text) > 150:
        raise ValidationError('Your title appears to be longer than the maximum of 150 characters.')


def valid_content(text):
    """Validates form input for content"""
    # text size, min size, max size
    text = text.strip()
    ts, mi, mx = len(text), MIN_POST_SIZE, MAX_POST_SIZE
    if not(text):
        raise ValidationError('Content appears to be whitespace')
    if text == P_CONTENT:
        raise ValidationError('Please change the default content')
    if ts < mi:
        raise ValidationError('Your content is only %d charactes long. The minimum is %d.' % (ts, mi))
    if ts > mx:
        raise ValidationError('Your content  is too long %d characters. The maximum is %d .' % (ts, mx))


def valid_tag(text):
    """Validates form input for tags"""

    if not text:
        raise ValidationError('Please enter at least one tag')

    if text == P_TAG:
        raise ValidationError('Please change the default tag')

    if len(text) > 300:
        raise ValidationError('Tag line is too long')

    words = text.split()

    if len(words) > 7:
        raise ValidationError('You have too many tags, please use at most seven tags')


class QuestionForm(forms.Form, BootstrapForm):
    """
    A form representing a new question
    """

    error_css_class = 'error'
    required_css_class = 'required'

    title = forms.CharField(
        max_length=250,
        initial='',
        validators=[valid_title],
        widget=forms.TextInput(attrs={'class': '', 'placeholder': P_TITLE}),
    )

    content = forms.CharField(
        max_length=15000,
        initial='',
        validators=[valid_content],
        widget=forms.Textarea(attrs={'cols': '80', 'rows': '15', 'id': 'editor', 'placeholder': P_CONTENT}),
    )

    tags = forms.CharField(
        max_length=250,
        initial='',
        validators=[valid_tag],
        widget=forms.TextInput(attrs={'class': '', 'placeholder': P_TAG}),
    )

    #context = forms.CharField(
    #    max_length=1000,
    #    required=False,
    #    initial='',
    #)

    type = forms.ChoiceField(
        choices=POST_TYPES[2:],
    )


class AnswerForm(forms.Form, BootstrapForm):
    content = forms.CharField(
        max_length=10000,
        validators=[valid_content],
        widget=forms.Textarea(attrs={'cols': '80', 'rows': '15', 'id': 'editor'}),
    )
    tags = forms.CharField(
        max_length=250,
        initial='',
        validators=[valid_tag],
        widget=forms.TextInput(attrs={'class': '', 'placeholder': P_TAG}),
    )
