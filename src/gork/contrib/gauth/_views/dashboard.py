# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import app_reverse
from gbase.utils import class_view_decorator
from gauth.forms import GUserAdminForm


class DashboardIndex(TemplateView):
    template_name = 'gauth/gauth_index.html'


@class_view_decorator(login_required)
class DashboardUserList(ListView):
    """ Users index page. It list all registed users right now """
    model = get_user_model()
    template_name = 'gauth/gauth_user_list.html'

    def head(self, *args, **kwargs):
        return HttpResponse()


@class_view_decorator(login_required)
class DashboardUserDetail(DetailView):
    """ User's detailed information """
    model = get_user_model()
    template_name = 'gauth/gauth_user_detail.html'


@class_view_decorator(login_required)
class DashboardUserEdit(UpdateView):
    """ Edit user's profile in dashboard"""
    #form_class = get_user_model().ChangeForm
    form_class = GUserAdminForm
    template_name = 'gauth/gauth_user_edit.html'

    def form_valid(self, form):
        instance = super(DashboardUserEdit, self).form_valid(form)
        self.request.user.message_set.create(message=_('Your profile has been updated!'))
        return instance

    def get_context_data(self, **kwargs):
        context = super(DashboardUserEdit, self).get_context_data(**kwargs)
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


class DashboardTimeline(TemplateView):
    pass
