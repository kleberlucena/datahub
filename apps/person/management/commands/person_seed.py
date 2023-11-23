from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.core.management.base import BaseCommand

from apps.person import models

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

    def create_groups(self): # TODO: Verificar  permissões de modelos nos grupos.
        # Relacionar o grupo e as permissões a a ser vinculadas 
        groups_to_create = {
                "profile:person_basic": [
                'add_endereco', 'change_endereco', 'view_endereco', 'delete_endereco',
                'add_sugestao', 'change_sugestao', 'view_sugestao', 'delete_sugestao',
                'add_personcortex', 'change_personcortex', 'view_personcortex', 'delete_personcortex',
                'add_registocortex', 'change_registocortex', 'view_registocortex', 'delete_registocortex',
                'add_documento', 'change_documento', 'view_documento', 'delete_documento',
                'add_documentimage', 'change_documentimage', 'view_documentimage', 'delete_documentimage',
                'add_documenttype', 'change_documenttype', 'view_documenttype', 'delete_documenttype',
                'add_imagem', 'change_imagem', 'view_imagem', 'delete_imagem',
                'add_face', 'change_face', 'view_face', 'delete_face',
                'add_alcunha', 'change_alcunha', 'view_alcunha', 'delete_alcunha',
                'add_pessoa', 'change_pessoa', 'view_pessoa', 'delete_pessoa',
                'add_personaddresses', 'change_personaddresses', 'view_personaddresses', 'delete_personaddresses',
                'add_persondocuments', 'change_persondocuments', 'view_persondocuments', 'delete_persondocuments',
                'add_personimages', 'change_personimages', 'view_personimages', 'delete_personimages',
                'add_atributofisico', 'change_atributofisico', 'view_atributofisico', 'delete_atributofisico',
                'add_tatuagem', 'change_tatuagem', 'view_tatuagem', 'delete_tatuagem',
                'add_veiculocortex', 'change_veiculocortex', 'view_veiculocortex', 'delete_veiculocortex',
                'add_registoveiculocortex', 'change_registoveiculocortex', 'view_registoveiculocortex', 'delete_registoveiculocortex',
                'view_marktemplates', 'view_temporaryurl', 'view_marcaaguausuario',
            ],
            "profile:person_intermediate": [
                'add_endereco', 'change_endereco', 'view_endereco', 
                'add_documento', 'change_documento', 'view_documento', 
                'add_documentimage', 'change_documentimage', 'view_documentimage', 
                'add_imagem', 'change_imagem', 'view_imagem',
                'add_face', 'change_face', 'view_face',
                'add_alcunha', 'change_alcunha', 'view_alcunha',
                'add_pessoa', 'change_pessoa', 'view_pessoa',
                'add_personaddresses', 'change_personaddresses', 'view_personaddresses',
                'add_persondocuments', 'change_persondocuments', 'view_persondocuments',
                'add_personimages', 'change_personimages', 'view_personimages',
                'add_atributofisico', 'change_atributofisico', 'view_atributofisico',
                'add_tatuagem', 'change_tatuagem', 'view_tatuagem',
                'add_registro', 'change_registro', 'view_registro',
            ],
            "profile:person_advanced": [
                'add_endereco', 'change_endereco', 'view_endereco', 
                'add_personcortex', 'view_personcortex', 
                'add_registocortex', 'view_registocortex', 
                'add_documento', 'change_documento', 'view_documento', 
                'add_documentimage', 'change_documentimage', 'view_documentimage',
                'add_documenttype', 'change_documenttype', 'view_documenttype',
                'add_imagem', 'change_imagem', 'view_imagem',
                'add_face', 'change_face', 'view_face',
                'add_alcunha', 'change_alcunha', 'view_alcunha',
                'add_pessoa', 'change_pessoa', 'view_pessoa',
                'add_personaddresses', 'change_personaddresses', 'view_personaddresses',
                'add_persondocuments', 'change_persondocuments', 'view_persondocuments',
                'add_personimages', 'change_personimages', 'view_personimages',
                'add_atributofisico', 'change_atributofisico', 'view_atributofisico',
                'add_tatuagem', 'change_tatuagem', 'view_tatuagem',
            ],
        }
        
        # Relacionar todos os modelos do app
        models_to_get = [
            models.Person,
            models.PersonAddresses,
            models.PersonDocuments,
            models.PersonImages,
            models.Nickname,
            models.Tattoo,
            models.Physical,
            models.Face,
        ]

        with transaction.atomic():
            for group_name, permissions_codenames in groups_to_create.items():
                self.assign_permissions_to_group(group_name, models_to_get, permissions_codenames)

    def handle(self, *args, **kwargs):
       self.create_groups()
