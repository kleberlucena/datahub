from django.core.management.base import BaseCommand
from apps.protect_network.models import *
from apps.portal.models import *
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType




class Command(BaseCommand):

    def create_groups(self):
        groups_to_create = [
            "profile:protect_network_basic", #user can
            "profile:protect_network_advanced", #user can
            "profile:protect_network_manager", #user can 
        ]

        permissions_to_assign_protect_network_basic = [
            #"view_spottype",
            "view_contactinfo",
            "view_openinghours",
            #"view_spot",
            "view_tag",
            "view_image",
            #"view_spotaddresses",
            #"view_spot",
            "view_networkresponsible",
            "view_openinghours",
            "view_qpp",
            "view_securitysurvey",

        ]

        permissions_to_assign_protect_network_advanced = [
            #"add_spottype",
            #"change_spottype",
            #"delete_spottype",
            #"view_spottype",
            "add_contactinfo",
            "change_contactinfo",
            "delete_contactinfo",
            "view_contactinfo",
            "add_openinghours",
            "change_openinghours",
            "delete_openinghours",
            "view_openinghours",
            #"add_spot",
            #"change_spot",
            #"delete_spot",
            #"view_spot",
            "add_tag",
            "change_tag",
            "delete_tag",
            "view_tag",
            "add_image",
            "change_image",
            "delete_image",
            "view_image",
            #"add_spotaddresses",
            #"change_spotaddresses",
            #"delete_spotaddresses",
            #"view_spotaddresses",
            #"add_spot",
           # "change_spot",
           # "delete_spot",
            #"view_spot",
            "view_networkresponsible",
            "add_openinghours",
            "change_openinghours",
            "delete_openinghours",
            "view_openinghours",
            "view_qpp",
            "add_securitysurvey",
            "change_securitysurvey",
            "delete_securitysurvey",
            "view_securitysurvey",
            "view_network",
        ]

        permissions_to_assign_protect_network_manager = [
           # "add_spottype",
           # "change_spottype",
           # "delete_spottype",
            #"view_spottype",
            "add_contactinfo",
            "change_contactinfo",
            "delete_contactinfo",
            "view_contactinfo",
            "add_openinghours",
            "change_openinghours",
            "delete_openinghours",
            "view_openinghours",
            #"add_spot",
           # "change_spot",
           # "delete_spot",
            #"view_spot",
            "add_tag",
            "change_tag",
            "delete_tag",
            "view_tag",
            "add_image",
            "change_image",
            "delete_image",
            "view_image",
            #"add_spotaddresses",
            #"change_spotaddresses",
            #"delete_spotaddresses",
            #"view_spotaddresses",
            #"add_spot",
            #"change_spot",
            #"delete_spot",
           # "view_spot",
            "add_networkresponsible",
            "change_networkresponsible",
            "delete_networkresponsible",
            "view_networkresponsible",
            "add_openinghours",
            "change_openinghours",
            "delete_openinghours",
            "view_openinghours",
            "add_qpp",
            "change_qpp",
            "delete_qpp",
            "view_qpp",
            "add_securitysurvey",
            "change_securitysurvey",
            "delete_securitysurvey",
            "view_securitysurvey",
            "add_network",
            "change_network",
            "delete_network",
            "view_network",
        ]

        models_to_get = [
           # SpotType,
            ContactInfo,
            OpeningHours,
            Spot,
            Tag,
            Image,
            #SpotAddresses,
            NetworkResponsible,
            Qpp,
            SecuritySurvey,
            Network,
        ]

            

        with transaction.atomic():
            for group_name in groups_to_create:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))

                # Assign permissions to "profile:protect_network_basic" group
                if group_name == "profile:protect_network_basic":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_protect_network_basic
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:protect_network_advanced" group
                if group_name == "profile:protect_network_advanced":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_protect_network_advanced
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:protect_network_manager" group
                if group_name == "profile:protect_network_manager":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_protect_network_manager
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

    def handle(self, *args, **kwargs):
        self.create_groups()
