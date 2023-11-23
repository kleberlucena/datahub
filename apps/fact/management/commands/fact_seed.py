from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.core.management.base import BaseCommand

from apps.fact import models

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
        # Relacionar o grupo e as permissões a a ser vinculadas 
        groups_to_create = {
            "fact:fact_basic": [],  # Coloque as permissões para fact_basic aqui
            "fact:fact_intermediate": []  # Coloque as permissões para fact_intermediate aqui
        }
        
        # Relacionar todos os modelos do app
        models_to_get = [
            models.FactType,
            models.Fact,
            models.FactImage,
            models.FactAddresses,
            models.FactVictims,
            models.FactSuspects,
            models.FactWitnesses,
        ]

        with transaction.atomic():
            for group_name, permissions_codenames in groups_to_create.items():
                self.assign_permissions_to_group(group_name, models_to_get, permissions_codenames)

    def handle(self, *args, **kwargs):
       self.create_groups()
