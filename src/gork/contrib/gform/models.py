# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.fields import BLANK_CHOICE_DASH
from django.template.defaultfilters import slugify
from django.utils.datastructures import SortedDict
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from captcha.fields import CaptchaField
from gform.utils import JSONFieldDescriptor
from gform.widgets import BootstrapDatePickerWidget, BootstrapDateTimePickerWidget


def create_form_submission(model_instance, form_instance, request, **kwargs):
    """
    Create submission of form
    """
    return FormSubmission.objects.create(
        form=model_instance,
        data=repr(form_instance.cleaned_data), path=request.path,
        submit_user=request.user,
    )


def send_as_mail(model_instance, form_instance, request, config, **kwargs):
    """
    Return the FormSubmission objects record if submitted and send a email to
    the user.
    """
    submission = create_form_submission(
        model_instance,
        form_instance,
        request,
        **kwargs)

    send_mail(
        model_instance.title,
        submission.formatted_data(),
        settings.DEFAULT_FROM_EMAIL,
        [config['email']],
        fail_silently=True
    )
    return _('Thank you, your input has been received.')


#def send_as_message(model_instance, form_instance, request, config, **kwargs):
#    """
#    Return the FormSubmission objects record by sending a site messages to the
#    user.
#    """
#    from django.contrib import messages
#    #submission = create_form_submission(model_instance, form_instance, request, **kwargs)
#    return messages.add_message(request, SUCCESS, 'You submission is successful.')


class BootstrapForm(object):
    """
    Inherit with forms.Form or forms.ModelForm
    For example:
        class AnyForm(forms.Form, BootstrapForm):
            pass

        class AnyModelForm(forms.ModelForm, BootstrapForm):
            pass
    """

    def render_errors(self):
        if not self.errors:
            return ""
        output = []
        output.append(u'<div class="alert-message block-message error">')
        output.append(u'<a class="close" href="#">×</a>')
        output.append(u'<p><strong>%s</strong></p><ul>' % _('You got an error!'))
        for field, error in self.errors.items():
            output.append(u'<li><strong>%s</strong> %s</li>' % (field.title(), error[0]))
        output.append(u'</ul></div>')
        return mark_safe(u'\n'.join(output))

    def as_bootstrap(self):
        output = []
        #see original Form class __iter__ method
        for boundfield in self:
            row_template = u'''
            <div class="%(div_class)s %(required_label)s">
              %(label)s
              <div class="controls">
                %(field)s
                <span class="help-block">%(help_text)s</span>
              </div>
            </div>
            '''
            row_dict = {
                "div_class": "control-group",
                "required_label": boundfield.css_classes(),
                "field": boundfield.as_widget(),
                "label": boundfield.label_tag(attrs={'class': 'control-label', }),
                "help_text": boundfield.help_text,
            }

            if boundfield.errors:
                row_dict["div_class"] = "error"
                boundfield.field.widget.attrs["class"] = "error"

            output.append(row_template % row_dict)
        return mark_safe(u'\n'.join(output))


class Form(models.Model):
    """
    Basic form models
    """
    CONFIG_OPTIONS = [
        ('save_fs', {
            'title': _('Save form submission'),
            'process': create_form_submission}),
        ('email', {
            'title': _('E-mail'),
            'form_fields': [
                ('email', forms.EmailField(_('e-mail address')))],
            'process': send_as_mail}),
        #('message', {
        #    'title': _('Send site messages'),
        #    'process': send_as_message,
        #    }
        #),
    ]
    title = models.CharField(
        _('title'),
        max_length=100,
    )
    config_json = models.TextField(
        _('config'),
        blank=True,
    )
    config = JSONFieldDescriptor(
        'config_json',
    )
    designer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('gform_designer'),
        related_name='gform_designer',
    )
    num_allow = models.PositiveIntegerField(
        _('submit numbers allowed'),
        help_text=_('numbers of forms submit times'),
        default=1,
    )

    class Meta:
        verbose_name = _('form')
        verbose_name_plural = _('forms')

    def __unicode__(self):
        return self.title

    def form(self):
        fields = SortedDict((
            ('required_css_class', 'required'),
            ('error_css_class', 'error')))

        for field in self.fields.all():
            field.add_formfield(fields, self)

        #return type('Form%s' % self.pk, (forms.Form,), fields)
        return type('Form%s' % self.pk, (forms.Form, BootstrapForm), fields)

    def process(self, form, request):
        ret = {}
        cfg = dict(self.CONFIG_OPTIONS)

        for key, config in self.config.items():
            try:
                process = cfg[key]['process']
            except KeyError:
                # ignore configs without process methods
                continue

            ret[key] = process(
                model_instance=self,
                form_instance=form,
                request=request,
                config=config
            )
        return ret

    @property
    def export(self):
        pass


class FormField(models.Model):
    """
    Form field for custom dynamic form.
    """
    FIELD_TYPES = [
        ('text', 'text', forms.CharField),
        ('longtext', 'long text', curry(forms.CharField, widget=forms.Textarea)),
        ('email', 'e-mail address', forms.EmailField),
        ('date', 'date', curry(forms.DateField, widget=BootstrapDatePickerWidget)),
        ('datetime', 'datetime', curry(forms.DateTimeField, widget=BootstrapDateTimePickerWidget)),
        ('checkbox', 'checkbox', curry(forms.BooleanField, required=False)),
        ('select', 'select', curry(forms.ChoiceField, required=False)),
        ('radio', 'radio', curry(forms.ChoiceField, widget=forms.RadioSelect)),
        ('multiple-select', 'multiple select', forms.MultipleChoiceField),
        ('hidden', 'hidden', curry(forms.CharField, widget=forms.widgets.HiddenInput)),
        ('captcha', 'captcha', curry(CaptchaField)),
    ]

    form = models.ForeignKey(
        Form,
        related_name='fields',
        verbose_name=_('form'),
    )
    ordering = models.IntegerField(
        _('ordering'),
        default=0,
    )
    title = models.CharField(
        _('title'),
        max_length=100,
    )
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    field_type = models.CharField(
        _('field type'),
        max_length=20,
        choices=[r[:2] for r in FIELD_TYPES],
    )
    choices = models.CharField(
        _('choices'),
        max_length=1024,
        blank=True,
        help_text=_('Comma-separated'),
    )
    default_value = models.CharField(
        _('default value'),
        max_length=100,
        blank=True,
        help_text=_('Default value for this field'),
    )
    help_text = models.CharField(
        _('help text'),
        max_length=1024,
        blank=True,
        help_text=_('Optional extra explanatory text beside the field'),
    )
    is_required = models.BooleanField(
        _('is required'),
        default=True,
    )

    class Meta:
        ordering = ['ordering', 'id']
        unique_together = (('form', 'name'),)
        verbose_name = _('form field')
        verbose_name_plural = _('form fields')

    def __unicode__(self):
        return self.title

    def clean(self):
        if self.choices and not isinstance(self.get_type(), forms.ChoiceField):
            raise forms.ValidationError(
                _("You can't specify choices for %s fields") % self.field_type
            )

    def get_choices(self):
        get_tuple = lambda value: (slugify(value.strip()), value.strip())
        choices = [get_tuple(value) for value in self.choices.split(',')]
        if not self.is_required and self.field_type == 'select':
            choices = BLANK_CHOICE_DASH + choices
        return tuple(choices)

    def get_type(self, **kwargs):
        types = dict((r[0], r[2]) for r in self.FIELD_TYPES)
        return types[self.field_type](**kwargs)

    def add_formfield(self, fields, form):
        fields[self.name] = self.formfield()

    def formfield(self):
        kwargs = dict(label=self.title, required=self.is_required, initial=self.default_value)
        if self.choices:
            kwargs['choices'] = self.get_choices()
        if self.help_text:
            kwargs['help_text'] = self.help_text
        return self.get_type(**kwargs)


class FormSubmission(models.Model):
    """
    FormSubmission Models contain all data of forms submitted by users.
    """
    form = models.ForeignKey(
        Form,
        verbose_name=_('form'),
        related_name='submissions',
    )
    data = models.TextField()
    path = models.CharField(
        max_length=255,
    )
    submit_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('form_submit_user'),
        related_name='form_submit_user',
    )
    submit_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-submit_date',)
        verbose_name = _('form submission')
        verbose_name_plural = _('form submissions')

    def sorted_data(self, include=()):
        """
        Return SortedDict by field ordering and using titles as keys.

        `include` can be a tuple containing any or all of 'date', 'time',
        'datetime', or 'path' to include additional meta data.
        """
        data_dict = eval(self.data)
        data = SortedDict()
        field_names = []
        for field in self.form.fields.all():
            data[field.title] = data_dict.get(field.name)
            field_names.append(field.name)
        # append any extra data (form may have changed since submission, etc)
        for field_name in data_dict:
            if not field_name in field_names:
                data[field_name] = data_dict[field_name]
        if 'datetime' in include:
            data['submit_date'] = self.submit_date
        if 'date' in include:
            data['date submit_date'] = self.submit_date.date()
        if 'time' in include:
            data['time submit_date'] = self.submit_date.time()
        if 'path' in include:
            data['form path'] = self.path
        return data

    def formatted_data(self, html=False):
        html = True
        formatted = ""
        for key, value in self.sorted_data().items():
            if html:
                formatted += "<tr><th>%s</th><td>%s</td></tr>\n" % (key, value)
            else:
                formatted += "%s: %s\n" % (key, value)
        return formatted if not html else "<table>%s</table>" % formatted

    def formatted_data_html(self):
        return self.formatted_data(html=True)
