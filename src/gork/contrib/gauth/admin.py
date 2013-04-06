# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.db import transaction
from django.contrib import admin
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm, AdminPasswordChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.template.response import TemplateResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.html import escape
from mptt.admin import FeinCMSModelAdmin
from feincms.extensions import ExtensionModelAdmin
from gauth.models import GUser, Role
#from gauth.forms import GUserChangeForm


csrf_protect_m = method_decorator(csrf_protect)


class GUserAdminForm(forms.ModelForm):
    """ Custom User Form used in admin """
    username = forms.RegexField(
        label=_("Username"),
        max_length=30,
        regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and \
            @/./+/-/_ only."),
        error_messages={'invalid': _("This value may contain only letters, \
            numbers and @/./+/-/_ characters."), },
    )
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see \
            this user's password, but you can change the password using \
            <a href=\"password/\">this form</a>."),
    )

    class Meta:
        model = GUser

    def __init__(self, *args, **kwargs):
        super(GUserAdminForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        print f
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GUserAdmin(ExtensionModelAdmin):
    """
    GUser model admin inhert from ExtensionModelAdmin which support
    extensible fields insert and display in admin.
    """
    # template setting
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None

    # default fieldsets in user form
    fieldsets = [
        (_('Auth info'), {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                            'classes': ('collapse', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined'), 'classes': ('collapse', )}),
    ]
    #add_fieldsets = (
    #    (None, {
    #        'classes': ('wide',),
    #        'fields': ('username', 'password1', 'password2')},),
    #)
    #form = GUserChangeForm

    # user add form
    add_form = UserCreationForm

    # user password change form
    change_password_form = AdminPasswordChangeForm

    # list colum displayed in admin
    list_display = ('username', 'email', 'nickname', 'is_staff', 'date_joined', )

    # filter in admin
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # fields which could be searched
    search_fields = ('username', 'nickname', 'email')

    # default ordering
    ordering = ('username',)

    # filter in horizontal
    filter_horizontal = ('groups', 'user_permissions',)

    # custom fieldset insert start point which could change the ordering of
    # fieldset in admin
    fieldset_insertion_index = 4

    # required fields used in form
    required_fields = ['email']

    def get_form(self, request, obj=None, **kwargs):
        # add extended fields in admin form
        if not issubclass(self.form, GUserAdminForm):
            # Delay setting the ProfileAdminForm.
            # If form is added to the ProfileAdmin class then it cause
            # validation error due to the form fields and admin fieldsets
            # not being consistent.
            self.form = GUserAdminForm

            # Delay adding the password fields until the form is set.
            #fields = self.fieldsets[0][1]['fields']
            #try:
            #    index = fields.index('email') + 1
            #except ValueError:
            #    index = len(fields)
            #if not 'password1' in fields:
            #    fields[index:index] = ['password1', 'password2']

        # Create the form
        form = super(GUserAdmin, self).get_form(request, obj=obj, **kwargs)

        # Set required fields
        for fname in self.required_fields:
            form.base_fields[fname].required = True

        return form

    def get_urls(self):
        """
        Add change password url in user form.
        """
        from django.conf.urls import patterns
        return patterns('', (r'^(\d+)/password/$',
                        self.admin_site.admin_view(self.user_change_password),)
                        ) + super(GUserAdmin, self).get_urls()

    @sensitive_post_parameters()
    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super(GUserAdmin, self).add_view(request, form_url, extra_context)

    @sensitive_post_parameters()
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.queryset(request), pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        return TemplateResponse(
            request,
            self.change_user_password_template or 'admin/auth/user/change_password.html',
            context, current_app=self.admin_site.name,
        )

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(GUserAdmin, self).response_add(request, obj, post_url_continue)


class PermissionRoleAdmin(FeinCMSModelAdmin):
    """
    Permission Role Admin
    """
    fieldsets = (
        (None, {'fields': ('name', 'codename', 'description')}),
        (_('Roles'), {'fields': ('parent',)}),
        (_('Permissions'), {'fields': ((
            '_permissions', 'list_of_permissions', 'inherited_permissions'),)}),
        (_('Users'), {'fields': (('_users', 'list_of_users', 'inherited_users'),)}),
    )
    filter_horizontal = ('_permissions', '_users',)
    list_display = ('name', 'codename', 'description',)
    list_filter = ('_permissions__codename',)
    readonly_fields = (
        'children_roles',
        'list_of_permissions', 'list_of_users',
        'inherited_permissions', 'inherited_users',)
    search_fields = (
        'codename', '_permissions__app_label', '_permissions__codename',
        '_users__username', '_users__email'
    )

    def children_roles(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        roles = obj.get_descendants()
        for role in roles.iterator():
            row.append(li % role)
        return ul % "\n".join(row)
    children_roles.allow_tags = True
    children_roles.short_description = _('Children roles')

    def inherited_permissions(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        self_permission_pks = obj._permissions.values_list('id', flat=True)
        permissions = obj.permissions.exclude(pk__in=self_permission_pks)
        for perm in permissions.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    inherited_permissions.allow_tags = True
    inherited_permissions.short_description = _('Inherited permissions')

    def inherited_users(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        self_permission_pks = obj._users.values_list('id', flat=True)
        users = obj.users.exclude(pk__in=self_permission_pks)
        for perm in users.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    inherited_users.allow_tags = True
    inherited_users.short_description = _('Inherited users')

    def list_of_permissions(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        permissions = obj.permissions
        for perm in permissions.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    list_of_permissions.allow_tags = True
    list_of_permissions.short_description = _('Current permissions')

    def list_of_users(self, obj):
        li = u"<li>%s</li>"
        ul = u"<ul>\n%s\n</ul>"
        row = []
        users = obj.users
        for perm in users.iterator():
            row.append(li % perm)
        return ul % "\n".join(row)
    list_of_users.allow_tags = True
    list_of_users.short_description = _('Current users')


class ProxyGUser(GUser):
    """
    A proxy model combined with django.contrib.auth in admin
    """
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = GUser._meta.verbose_name
        verbose_name_plural = GUser._meta.verbose_name_plural


class ProxyRole(Role):
    """
    A proxy model combined with gauth.models.Role in admin
    """
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = Role._meta.verbose_name
        verbose_name_plural = Role._meta.verbose_name_plural


admin.site.register(ProxyGUser, GUserAdmin)
admin.site.register(ProxyRole, PermissionRoleAdmin)
