from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def has_group(user, group_names):
    # Separa os nomes dos grupos por vírgula
    group_names = group_names.split(',')

    # Obtém todos os grupos do usuário
    user_groups = user.groups.values_list('name', flat=True)

    # Verifica se o usuário é membro de pelo menos um dos grupos
    return any(group in user_groups for group in group_names)

