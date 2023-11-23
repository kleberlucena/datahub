
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ImproperlyConfigured


from django.shortcuts import render, redirect
from base.views import *


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None
    login_url = 'base:authorization_error_view'

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return redirect(self.login_url)
        return super().handle_no_permission()

    def test_func(self):
        if self.group_required is None:
            raise ImproperlyConfigured(
                "{0} is missing the group_required attribute".format(
                    self.__class__.__name__)
            )

        if isinstance(self.group_required, str):
            self.group_required = [self.group_required]

        return any(group in [g.name for g in self.request.user.groups.all()] for group in self.group_required)


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='base:authorization_error_view')
