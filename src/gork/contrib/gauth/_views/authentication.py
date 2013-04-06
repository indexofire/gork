# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateResponseMixin, View
from gbase.utils import default_redirect
from gauth import signals
from gauth import settings
from gauth.forms import SigninUsernameForm


class LoginView(FormView):
    """ Default login views """
    template_name = "gauth/gauth_login.html"
    form_class = SigninUsernameForm
    #form_class = settings.GAUTH_FORM_CLASS
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
        """get login context"""
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
        signals.user_login_attempt.send(
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
        signals.user_logged_in.send(
            sender=LoginView,
            user=form.user,
            form=form
        )

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
    """ Default log out views """
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


def login_view_ajax(request):
    """ Ajax login view used in site """
    import json

    form_class = settings.GAUTH_FORM_CLASS
    template_name = "gauth/gauth_login_ajax.html"

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
        #return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')
        return HttpResponse(
            json.dumps(response, ensure_ascii=False),
            content_type='application/json; charset=UTF-8'  # IE need charset=UTF-8
        )
    return render(request, template_name, {'form': form})
