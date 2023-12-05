from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.bnmp import models

class Command(BaseCommand):

    def assign_permissions_to_group(self, group_name, models, permissions_codenames):
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists.'))

        permissions = []
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            model_permissions = Permission.objects.filter(content_type=content_type, codename__in=permissions_codenames)
            permissions.extend(model_permissions)
        group.permissions.add(*permissions)

    def create_groups(self):
        # Todas os grupos e respectivas permissões devem ser declarados aqui
        groups_to_create = {
            # "profile:alert_advanced": [
            #     'view_alertcortex', 
            #     'view_personalertcortex', 
            #     'view_vehiclealertcortex'
            # ],
        }
        
        # Todos os modelos relacionados devem ser listado abaixo.
        models_to_get = [models.PersonBNMP, models.MandadoPrisao, models.RegistryBNMP]

        with transaction.atomic():
            for group_name, permissions_codenames in groups_to_create.items():
                self.assign_permissions_to_group(group_name, models_to_get, permissions_codenames)

    def handle(self, *args, **kwargs):
       self.create_groups()
