# -*- coding: utf-8 -*-
import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#from django.utils.safestring import mark_safe
from django.template.defaultfilters import striptags
from gauth.models import GUser
from gauth.settings import GAUTH_EMAIL_UNIQUE
from gform.models import BootstrapForm


alnum_re = re.compile(r"^\w+$")


class AjaxBaseForm(forms.BaseForm):
    """
    Ajax base form in order to return json
    """
    def errors_as_json(self, strip_tags=False):
        error_summary = {}
        errors = {}
        for error in self.errors.iteritems():
            errors.update({error[0]: unicode(striptags(error[1]) if strip_tags else error[1])})
        error_summary.update({'errors': errors})
        return error_summary


class AjaxModelForm(AjaxBaseForm, forms.ModelForm):
    """Ajax Form class for ModelForms"""
    pass


class AjaxForm(AjaxBaseForm, forms.Form):
    """Ajax Form class for Forms"""
    pass


class GUserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"),
        max_length=30,
        regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = GUser

    def __init__(self, *args, **kwargs):
        super(GUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class SignupForm(forms.Form, BootstrapForm):
    """
    Sign up form for registeration
    """
    username = forms.CharField(
        label=_("Username"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )
    email = forms.EmailField(widget=forms.TextInput(), required=True)
    #code = forms.CharField(
    #    label=_("Verify code"),
    #    max_length=64,
    #    required=False,
    #    widget=forms.HiddenInput()
    #)

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        qs = get_user_model().objects.filter(username__iexact=self.cleaned_data["username"])
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = get_user_model().objects.filter(email__iexact=value)
        if not qs.exists() or not GAUTH_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data


#class LoginForm(AjaxForm):
class LoginForm(forms.Form):
    """
    User Login Form, the only checked field is pasword. Child inherit from this
    class will add other field
    """
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    #remember = forms.BooleanField(
    #    label=_("Remember Me"),
    #    required=False,
    #)
    user = None

    def clean(self):
        if self._errors:
            return
        from django.contrib.auth import authenticate
        user = authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(self.authentication_inactive_message)
        else:
            raise forms.ValidationError(self.authentication_fail_message)
        return self.cleaned_data

    def user_credentials(self):
        return {
            "username": self.cleaned_data[self.identifier_field],
            "password": self.cleaned_data["password"],
        }


class SigninUsernameForm(LoginForm, BootstrapForm):
    """
    Use username as login
    """
    username = forms.CharField(label=_("Username"), max_length=30)
    authentication_fail_message = _("The username and/or password you specified are not correct.")
    authentication_inactive_message = _("This account is inactive.")
    identifier_field = "username"

    def __init__(self, *args, **kwargs):
        super(SigninUsernameForm, self).__init__(*args, **kwargs)
        #self.fields.keyOrder = ["username", "password", "remember"]
        self.fields.keyOrder = ["username", "password"]


class PasswordResetForm(forms.Form):
    """
    Reset password form.
    """
    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if not GUser.objects.filter(email__iexact=value):
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class ChangePasswordForm(forms.Form):

    password_current = forms.CharField(
        label=_("Current Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get("password_current")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["password_current"]

    def clean_password_new_confirm(self):
        if "password_new" in self.cleaned_data and "password_new_confirm" in self.cleaned_data:
            if self.cleaned_data["password_new"] != self.cleaned_data["password_new_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_new_confirm"]


class GUserEditForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = GUser
        exclude = (
            'user_permissions',
            'groups',
            'password',
            'username',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
            'is_active',
            'qa_score',
            'user_type',
            'about_me_html',
            'bronze_badges',
            'silver_badges',
            'gold_badges',
            'new_messages',
        )


