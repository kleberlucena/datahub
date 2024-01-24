from django.core.management.base import BaseCommand
from apps.georeference.models import *
from apps.portal.models import *
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



class Command(BaseCommand):

    def create_groups(self):
        groups_to_create = [
            "profile:georeference_area_basic", #user can list areas and categories
            "profile:georeference_area_advanced", #user can list/create/update areas and categories
            "profile:georeference_area_manager", #user can list/create/delete areas and categories
            "profile:georeference_spot_basic", #user can list spottypes, spots and spotaddresses
            "profile:georeference_spot_advanced", #user can list/create/update spottypes, spots and spotaddresses
            "profile:georeference_spot_manager", #user can list/create/delete spottypes, spots and spotaddresses
        ]

        permissions_to_assign_area_basic = [
            "view_area",
            "view_category"
        ]

        permissions_to_assign_area_advanced = [
            "view_area",
            "add_area",
            "change_area",
            "view_category",
            "add_category",
            "change_category",
        ]

        permissions_to_assign_area_manager = [
            "view_area",
            "add_area",
            "change_area",
            "delete_area",
            "view_category",
            "add_category",
            "change_category",
            "delete_category",
        ]

        permissions_to_assign_spot_basic = [
            "view_spottype",
            "view_spotaddresses",
            "view_spot",
        ]

        permissions_to_assign_spot_advanced = [
            "view_spottype",
            "view_spotaddresses",
            "view_spot",
            "add_spottype",
            "add_spotaddresses",
            "add_spot",
            "change_spottype",
            "change_spotaddresses",
            "change_spot",
        ]

        permissions_to_assign_spot_manager = [
            "view_spottype",
            "view_spotaddresses",
            "view_spot",
            "add_spottype",
            "add_spotaddresses",
            "add_spot",
            "change_spottype",
            "change_spotaddresses",
            "change_spot"
            "delete_spottype",
            "delete_spotaddresses",
            "delete_spot",
        ]

        models_to_get = [Area, Category]

        with transaction.atomic():
            for group_name in groups_to_create:
                group, created = Group.objects.get_or_create(name=group_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created successfully.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))

                # Assign permissions to "profile:georeference_area_basic" group
                if group_name == "profile:georeference_area_basic":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_area_basic
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:georeference_area_advanced" group
                if group_name == "profile:georeference_area_advanced":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_area_advanced
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:georeference_area_manager" group
                if group_name == "profile:georeference_area_manager":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_area_manager
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:georeference_spot_basic" group
                if group_name == "profile:georeference_spot_basic":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_spot_basic
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:georeference_spot_advanced" group
                if group_name == "profile:georeference_spot_advanced":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_spot_advanced
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

                # Assign permissions to "profile:georeference_spot_manager" group
                if group_name == "profile:georeference_spot_manager":
                    permissions = []
                    for model in models_to_get:
                        content_type = ContentType.objects.get_for_model(model)
                        model_permissions = Permission.objects.filter(
                            content_type=content_type, codename__in=permissions_to_assign_area_manager
                        )
                        permissions.extend(model_permissions)
                    group.permissions.add(*permissions)

    def handle(self, *args, **kwargs):
        self.create_groups()
