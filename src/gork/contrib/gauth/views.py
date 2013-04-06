# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.views.generic import DetailView, UpdateView, ListView
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from feincms.content.application.models import app_reverse
from gbase.utils import class_view_decorator, default_redirect
from gauth.forms import *
from gauth.signals import *
from gauth.models import EmailConfirmation
from gauth.admin import GUserAdminForm
from gauth import settings


@class_view_decorator(login_required)
class AccountIndex(ListView):
    """
    Account index page. It list all registed users right now.
    """
    model = get_user_model()
    template_name = 'gauth/gauth_index.html'

    def head(self, *args, **kwargs):
        return HttpResponse()


class AccountDetail(DetailView):
    """
    User's detailed information.
    """
    model = get_user_model()
    template_name = 'gauth/gauth_detail.html'


@class_view_decorator(login_required)
class AccountEdit(UpdateView):
    """
    Edit user's profile.
    """
    #form_class = get_user_model()ChangeForm
    form_class = GUserAdminForm
    template_name = 'gauth/gauth_edit.html'

    def form_valid(self, form):
        instance = super(AccountEdit, self).form_valid(form)
        self.request.user.message_set.create(message='Your profile has been updated.')
        return instance

    def get_context_data(self, **kwargs):
        context = super(AccountEdit, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        return context

    def get_object(self):
        model = get_user_model()
        if isinstance(self.request.user, model):
            return self.request.user
        return self.request.user

    def get_success_url(self):
        #return self.request.GET.get('next', reverse('profile'))
        return self.request.GET.get('next', app_reverse('gauth-detail'))


class SignupView(FormView):
    """
    Default sign up view.
    """
    template_name = "gauth/gauth_signup.html"
    template_name_email_confirmation_sent = "gauth/gauth_signupemail_confirmation_sent.html"
    template_name_signup_closed = "gauth/gauth_signup_closed.html"
    form_class = SignupForm
    form_kwargs = {}
    redirect_field_name = "next"
    messages = {
        "email_confirmation_sent": {
            "level": messages.INFO,
            "text": _("Confirmation email sent to %(email)s.")
        },
        "invalid_signup_code": {
            "level": messages.WARNING,
            "text": _("The code %(code)s is invalid.")
        }
    }

    def __init__(self, *args, **kwargs):
        self.created_user = None
        kwargs["signup_code"] = None
        super(SignupView, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(default_redirect(self.request, settings.GAUTH_LOGIN_REDIRECT_URL))
        if not self.is_open():
            return self.closed()
        return super(SignupView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.is_open():
            return self.closed()
        return super(SignupView, self).post(*args, **kwargs)

    def get_initial(self):
        initial = super(SignupView, self).get_initial()
        if self.signup_code:
            initial["code"] = self.signup_code.code
            if self.signup_code.email:
                initial["email"] = self.signup_code.email
        return initial

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.REQUEST.get(redirect_field_name),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(SignupView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        user_sign_up_attempt.send(
            sender=SignupForm,
            username=form.data.get("username"),
            email=form.data.get("email"),
            result=form.is_valid()
        )
        return super(SignupView, self).form_invalid(form)

    def form_valid(self, form):
        self.created_user = self.create_user(form, commit=False)
        if settings.GAUTH_EMAIL_CONFIRMATION_REQUIRED:
            self.created_user.is_active = False
        # prevent User post_save signal from creating an Account instance
        # we want to handle that ourself.
        self.created_user._disable_gauth_creation = True
        #from question.extensions.user import make_uuid
        #self.created_user.uuid = make_uuid()
        self.created_user.nickname = self.created_user.username
        self.created_user.save()
        #self.create_gauth(form)
        email_kwargs = {"primary": True, "verified": False}
        if self.signup_code:
            self.signup_code.use(self.created_user)
            if self.signup_code.email and self.created_user.email == self.signup_code.email:
                email_kwargs["verified"] = True
        #email_address = EmailAddress.objects.add_email(self.created_user, self.created_user.email, **email_kwargs)
        self.after_signup(form)
        if settings.GAUTH_EMAIL_CONFIRMATION_EMAIL and not email_kwargs["verified"]:
            email_address.send_confirmation()
        if settings.GAUTH_EMAIL_CONFIRMATION_REQUIRED and not email_kwargs["verified"]:
            response_kwargs = {
                "request": self.request,
                "template": self.template_name_email_confirmation_sent,
                "context": {
                    "email": self.created_user.email,
                    "success_url": self.get_success_url(),
                }
            }
            return self.response_class(**response_kwargs)
        else:
            show_message = [
                settings.GAUTH_EMAIL_CONFIRMATION_EMAIL,
                self.messages.get("email_confirmation_sent"),
                not email_kwargs["verified"]
            ]
            if all(show_message):
                messages.add_message(
                    self.request,
                    self.messages["email_confirmation_sent"]["level"],
                    self.messages["email_confirmation_sent"]["text"] % {
                        "email": form.cleaned_data["email"]
                    }
                )
            self.login_user()
        return redirect(self.get_success_url())

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.GAUTH_SIGNUP_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def create_user(self, form, commit=True, **kwargs):
        user = get_user_model()(**kwargs)
        username = form.cleaned_data.get("username")
        if username is None:
            username = self.generate_username(form)
        user.username = username
        user.email = form.cleaned_data["email"].strip()
        password = form.cleaned_data.get("password")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    #def create_gauth(self, form):
    #    return Account.create(request=self.request, user=self.created_user, create_email=False)

    def generate_username(self, form):
        raise NotImplementedError("Unable to generate username by default. \
            Override SignupView.generate_username in a subclass.")

    def after_signup(self, form):
        user_signed_up.send(sender=SignupForm, user=self.created_user, form=form)

    def login_user(self):
        # set backend on User object to bypass needing to call auth.authenticate
        self.created_user.backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, self.created_user)
        self.request.session.set_expiry(0)

    def is_open(self):
        code = self.request.REQUEST.get("code")
        if code:
            try:
                self.signup_code = SignupCode.check(code)
            except SignupCode.InvalidCode:
                if not settings.GAUTH_OPEN_SIGNUP:
                    return False
                else:
                    if self.messages.get("invalid_signup_code"):
                        messages.add_message(
                            self.request,
                            self.messages["invalid_signup_code"]["level"],
                            self.messages["invalid_signup_code"]["text"] % {
                                "code": code
                            }
                        )
                    return True
            else:
                return True
        else:
            return settings.GAUTH_OPEN_SIGNUP

    def closed(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_signup_closed,
        }
        return self.response_class(**response_kwargs)


class LoginView(FormView):
    """
    Default sign in views.
    """
    template_name = "gauth/gauth_login.html"
    form_class = SigninUsernameForm
    form_kwargs = {}
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        # method inherit from ProcessFormView's get() which define process status
        # original get method is:
        # def get(self, request, *args, **kwargs):
        #     form_class = self.get_form_class()
        #     form = self.get_form(form_class)
        #     return self.render_to_response(self.get_context_data(form=form))
        if self.request.user.is_authenticated():
            # check if the user is log in, if so redirect to get_success_url()
            # if not, render_to_response(self.get_context_data(form=form))
            return redirect(self.get_success_url())
        return super(LoginView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            # redirect_field_* attr were used to define redirect url in forms
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.REQUEST.get(redirect_field_name),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        user_login_attempt.send(
            sender=LoginView,
            username=form.data.get(form.identifier_field),
            result=form.is_valid()
        )
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        self.login_user(form)
        self.after_login(form)
        return redirect(self.get_success_url())

    def after_login(self, form):
        user_logged_in.send(sender=LoginView, user=form.user, form=form)

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.GAUTH_LOGIN_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def login_user(self, form):
        # log in user and set user login status expiry period in session
        login(self.request, form.user)
        expiry = settings.GAUTH_REMEMBER_ME_EXPIRY if form.cleaned_data.get("remember") else 0
        self.request.session.set_expiry(expiry)


class LogoutView(TemplateResponseMixin, View):
    """
    Default log out views.
    """
    template_name = "gauth/gauth_logout.html"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.REQUEST.get(redirect_field_name),
        })
        return ctx

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.GAUTH_LOGOUT_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


class PasswordResetView(FormView):
    """
    """
    template_name = "gauth/gauth_password_reset.html"
    template_name_sent = "gauth/gauth_password_reset_sent.html"
    form_class = PasswordResetForm
    token_generator = default_token_generator

    def get_context_data(self, **kwargs):
        context = kwargs
        if self.request.method == "POST" and "resend" in self.request.POST:
            context["resend"] = True
        return context

    def form_valid(self, form):
        self.send_email(form.cleaned_data["email"])
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }
        return self.response_class(**response_kwargs)

    def send_email(self, email):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        for user in get_user_model().objects.filter(email__iexact=email):
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            password_reset_url = u"%s://%s%s" % (
                protocol,
                unicode(current_site.domain),
                reverse("gauth_password_reset_token", kwargs=dict(uidb36=uid, token=token))
            )
            ctx = {
                "user": user,
                "current_site": current_site,
                "password_reset_url": password_reset_url,
            }
            subject = render_to_string("gauth/email/password_reset_subject.txt", ctx)
            subject = "".join(subject.splitlines())
            message = render_to_string("gauth/email/password_reset.txt", ctx)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    def make_token(self, user):
        return self.token_generator.make_token(user)


class ConfirmEmailView(TemplateResponseMixin, View):

    messages = {
        "email_confirmed": {
            "level": messages.SUCCESS,
            "text": _("You have confirmed %(email)s.")
        }
    }

    def get_template_names(self):
        return {
            "GET": ["gauth/gauth_email_confirm.html"],
            "POST": ["gauth/gauth_email_confirmed.html"],
        }[self.request.method]

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm()
        user = confirmation.email_address.user
        user.is_active = True
        user.save()
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        if self.messages.get("email_confirmed"):
            messages.add_message(
                self.request,
                self.messages["email_confirmed"]["level"],
                self.messages["email_confirmed"]["text"] % {
                    "email": confirmation.email_address.email
                }
            )
        return redirect(redirect_url)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except EmailConfirmation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        qs = EmailConfirmation.objects.all()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        return ctx

    def get_redirect_url(self):
        if self.request.user.is_authenticated():
            if not settings.GAUTH_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL:
                return settings.GAUTH_LOGIN_REDIRECT_URL
            return settings.GAUTH_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
        else:
            return settings.GAUTH_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL


class ChangePasswordView(FormView):

    template_name = "gauth/gauth_password_change.html"
    form_class = ChangePasswordForm
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _(u"Password successfully changed.")
        }
    }

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect("gauth_password_reset")
        return super(ChangePasswordView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(ChangePasswordView, self).post(*args, **kwargs)

    def change_password(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data["password_new"])
        user.save()

    def after_change_password(self):
        user = self.request.user
        password_changed.send(sender=ChangePasswordView, user=user)
        if settings.GAUTH_NOTIFY_ON_PASSWORD_CHANGE:
            self.send_email(user)
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"]
            )

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {"user": self.request.user, "initial": self.get_initial()}
        if self.request.method in ["POST", "PUT"]:
            kwargs.update({
                "data": self.request.POST,
                "files": self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        self.change_password(form)
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.REQUEST.get(redirect_field_name),
        })
        return ctx

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.GAUTH_PASSWORD_CHANGE_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def send_email(self, user):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        ctx = {
            "user": user,
            "protocol": protocol,
            "current_site": current_site,
        }
        subject = render_to_string("gauth/email/password_change_subject.txt", ctx)
        subject = "".join(subject.splitlines())
        message = render_to_string("gauth/email/password_change.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def login_ajax(request, tpl=None):
    """
    ajax login view used in site.
    """
    form_class = SigninUsernameForm
    template_name = tpl or "gauth/gauth_login.html"

    if request.method == 'GET':
        form = form_class()
    else:
        form = form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                response = {'success': True, 'next': '/'}
        else:
            response = form.errors_as_json()
        return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')
    return render(request, template_name, {'form': form})


def activate_user(request):
    pass
