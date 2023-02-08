
from django.db import models
from django_minio_backend import MinioBackend
from stdimage.models import StdImageField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid


from . import helpers

"""
TemporaryURL - Classe para definição de url temporária usada em disponibilidade de imagem com marca d`água
"""


class TemporaryURL(models.Model):
    uuid = models.UUIDField()
    temporary_url = models.URLField()
    expiration_date = models.DateTimeField()
    photo = StdImageField(
        "Marca d'agua",
        storage=MinioBackend(bucket_name='bacinf-private'),
        upload_to='watermark',
        delete_orphans=True,
        blank=True,
        null=True
    )
    
    
class MarkTemplates(models.Model):
    uuid_user_mark = models.UUIDField(unique=True)
    mark_128 = StdImageField(
        "Marca 128",
        storage=MinioBackend(bucket_name='bacinf-private'),
        upload_to='user_watermark_128',
        delete_orphans=True,
        blank=True,
        null=True
    )
    mark_480 = StdImageField(
        "Marca 480",
        storage=MinioBackend(bucket_name='bacinf-private'),
        upload_to='user_watermark_480',
        delete_orphans=True,
        blank=True,
        null=True
    )
    mark_720 = StdImageField(
        "Marca 720",
        storage=MinioBackend(bucket_name='bacinf-private'),
        upload_to='user_watermark_720',
        delete_orphans=True,
        blank=True,
        null=True
    )
    
    
class UserMark(models.Model):
    uuid = models.UUIDField(unique=True)
    active = models.BooleanField("Validade", default=True)
    mark_text = models.CharField("Marca d'água", max_length=6)
    created_at = models.DateField('Criado', auto_now_add=True)
    updated_at = models.DateField('Atualizado', auto_now=True)
    user = models.ForeignKey(User, related_name='user_mark', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Marca d'água de usuário"
        verbose_name_plural = "Marcas d'água de usuários"
        ordering = ['-created_at']

    def __str__(self):
        return self.mark_text
    

@receiver(pre_save, sender=UserMark)
def generate_mark_templates(sender, instance, **kwargs):
    if instance._state.adding:
        instance.uuid = uuid.uuid4()
        template = MarkTemplates(uuid_user_mark=instance.uuid)
        image_name, image_file = helpers.create_watermark_template_user(instance.mark_text, 128, 128)
        template.mark_128.save(image_name, image_file, save=False)
        image_name, image_file = helpers.create_watermark_template_user(instance.mark_text, 480, 480)
        template.mark_480.save(image_name, image_file, save=False)
        image_name, image_file = helpers.create_watermark_template_user(instance.mark_text, 720, 720)
        template.mark_720.save(image_name, image_file, save=False)
        template.save()
        

pre_save.connect(generate_mark_templates, sender=UserMark)

