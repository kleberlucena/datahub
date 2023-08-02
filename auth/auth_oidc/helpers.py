import catch as catch
from django.contrib.auth.models import Group
import logging
from allauth.socialaccount.models import SocialAccount


logger = logging.getLogger(__name__)


def synchronize_oidc_permission(user, request, **kwargs):
    try:
        data = SocialAccount.objects.get(
            user_id=user.id).extra_data['resource_access']
        # get the first key in the dictionary which is the client
        clients = list(data.keys())
        if 'bacinf' in clients:
            roles_oidc = data['bacinf']['roles']
        else:
            roles_oidc = []
        roles_oidc_to_analyze = []  # list of roles not existing in user
        # groups from system local
        groups_all = [group.name for group in Group.objects.all()]
        groups_user = user.groups.all()

        # temp list from user groups
        groups_analytics = {group.name: False for group in groups_user}

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
                logger.warning(
                    "Attempt to enter permissions that do not exist in the system.", role)

        logger.info("[synchronize_oidc_permission] - sync permissions")

    except SocialAccount.DoesNotExist as e:
        logger.error(
            f"Failed when trying to sync permissions with SocialAccount: {e}")

    except Exception as err:
        logger.error(
            f"Failed when trying to sync permissions with provider: {err}")
