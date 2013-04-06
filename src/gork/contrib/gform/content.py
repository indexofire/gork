# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
#from django.shortcuts import get_object_or_404
from gform.models import Form, FormSubmission


class FormContent(models.Model):
    """
    It's a content type for feincms.module.page which render basic form
    HTML content in pages.
    Usage:
    Put these lines into anywhere of your app or project which would be
    invoke.
        from feincms.module.page.models import Page
        Page.create_content_type(FormContent)

    """

    FIELD_STYLE_CHOICES = (
        ('bootstrap', 'bootstrapform'),
        #('jqtransform', 'jqtransformplugin'),
    )
    template = 'gform/content.html'
    form = models.ForeignKey(
        Form,
        verbose_name=_('form'),
        related_name='%(app_label)s_%(class)s_related',
    )
    #form_description = models.TextField(blank=True, null=True)
    show_form_title = models.BooleanField(
        _('show form title'),
        default=True,
    )
    success_message = models.TextField(
        _('success message'),
        blank=True,
        help_text=_("Optional custom message to display after valid form is submitted"),
    )
    form_style = models.CharField(
        max_length=255,
        default='bootstrap',
        choices=FIELD_STYLE_CHOICES,
    )
    success_info = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        default=_('form submission successful'),
    )

    class Meta:
        abstract = True
        verbose_name = _('form content')
        verbose_name_plural = _('form contents')

    @property
    def media(self):
        if self.form_style == 'bootstrap':
            return forms.Media(
                css={'all': ('gform/datetimepicker/css/bootstrap-datetimepicker.min.css', )},
                js=('gform/datetimepicker/js/bootstrap-datetimepicker.min.js', ),
            )
        #if self.form_style == 'jqtransformplugin':
        #    return forms.Media(
        #        css={'all': ('js/jqtransformplugin/jqtransform.css', )},
        #        js=('js/jqtransformplugin/jquery.jqtransform.js', ),
        #        )

    def process_valid_form(self, request, form_instance, **kwargs):
        """
        Process form and return response (hook method).
        """
        process_result = self.form.process(form_instance, request)
        context = RequestContext(request, {
            'content': self,
            'message': self.success_message or process_result or u''})
        return render_to_string(self.template, context)

    def render(self, request, **kwargs):
        """
        Process form content block render
        """
        form_class = self.form.form()
        prefix = 'fc%d' % self.id
        if self.form_style == 'bootstrap':
            self.form_style = 'form-horizontal'

        # render page after post form.
        if request.method == 'POST':
            form_instance = form_class(request.POST, prefix=prefix)
            if form_instance.is_valid():
                return self.process_valid_form(request, form_instance, **kwargs)
        else:
            form_instance = form_class(prefix=prefix)
            try:
                form_submission_object = FormSubmission.objects.get(
                    path=request.path)
                if form_submission_object.sorted_data()['submitter'] == str(request.user):
                    context = RequestContext(request, {
                        'content': self,
                        'form': form_submission_object.formatted_data_html(),
                        'is_submitter': 0})
                    return render_to_string(self.template, context)
                else:
                    context = RequestContext(request, {
                        'content': self,
                        'form': form_instance,
                        'is_submitter': 1})
                    return render_to_string(self.template, context)
            except:
                context = RequestContext(request, {
                    'content': self,
                    'form': form_instance,
                    'test': '111'})
                return render_to_string(self.template, context)
