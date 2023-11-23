from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def has_group(user, group_names):
    group_names = group_names.split(',')
    user_groups = user.groups.values_list('name', flat=True)
    return any(group in user_groups for group in group_names)

