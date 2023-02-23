import catch as catch
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in
import logging
from allauth.socialaccount.models import SocialAccount


logger = logging.getLogger(__name__)


def synchronize_permissions(user, mapa_of_permissions):
    try:
        clients = list(mapa_of_permissions.keys())  # get the first key in the dictionary which is the client
        if 'bacinf' in clients:
            roles_oidc = mapa_of_permissions['bacinf']['roles']
        else:
            roles_oidc = []
        roles_oidc_to_analyze = []  # list of roles not existing in user
        groups_all = [group.name for group in Group.objects.all()]  # groups from system local
        groups_user = user.groups.all()

        groups_analytics = {group.name: False for group in groups_user}  # temp list from user groups

        # Analyze current user groups
        for role in roles_oidc:
            if role in groups_analytics.keys():
                groups_analytics[role] = True
            else:
                roles_oidc_to_analyze.append(role)

        # Remove divergent groups
        for role_tuple in groups_analytics.items():
            if not role_tuple[1]:
                group = Group.objects.get(name=role_tuple[0])
                user.groups.remove(group)
        # Check if new groups are compatible with the system
        for role in roles_oidc_to_analyze:
            if role in groups_all:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            else:
                logger.warning("Attempt to enter permissions that do not exist in the system.", role)

        logger.info("[synchronize_oidc_permission] - sync permissions")

    except Exception as err:
        logger.error(f"Failed when trying to sync permissions: {err}")


def synchronize_oidc_permission(sender, user, request, **kwargs):
    try:
        data = SocialAccount.objects.get(user_id=user.id).extra_data['resource_access']
        synchronize_permissions(user, data)
    except Exception as err:
        logger.error(f"Failed when trying to sync permissions with provider: {err}", exc_info=True)
        
        
user_logged_in.connect(synchronize_oidc_permission)