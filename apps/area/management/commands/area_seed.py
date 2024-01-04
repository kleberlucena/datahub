from django.core.management.base import BaseCommand
from apps.area.models import *
from apps.portal.models import *
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



class Command(BaseCommand):

    def create_groups(self):
        groups_to_create = [
            "profile:area_basic", #user can list areas and categories
            "profile:area_advanced", #user can list/create/update areas and categories
            "profile:area_manager", #user can list/create//delete areas and categories
        ]

        permissions_to_assign_basic = [
            "view_area",
            "view_category"
        ]

        permissions_to_assign_advanced = [
            "view_area",
            "add_area",
            "change_area",
            "view_category",
            "add_category",
            "change_category",
        ]

        permissions_to_assign_manager = [
            "view_area",
            "add_area",
            "change_area",
            "delete_area",
            "view_category",
            "add_category",
            "change_category",
            "delete_category",
        ]


        models_to_get = [Area, Category]

        with transaction.atomic():
            for group_name in groups_to_create:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))

                # Assign permissions to "profile:area_basic" group
                if group_name == "profile:area_basic":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_basic
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:area_advanced" group
                if group_name == "profile:area_advanced":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_advanced
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:area_manager" group
                if group_name == "profile:area_manager":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_manager
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

    def handle(self, *args, **kwargs):
        self.create_groups()
