import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy
from django.db import models
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

from apps.portal.models import Entity


class Base(models.Model):
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class SoftDelete(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class Image(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("descrição", max_length=255, blank=True, null=True)
    file = StdImageField(
        'Imagem', 
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True
    )
    entity = models.ForeignKey(
        Entity, 
        related_name='images_entity', 
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='image_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='image_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def soft_delete_cascade_policy_action(self, **kwargs):
        # Insert here custom pre delete logic
        user = kwargs['deleted_by']
        if user is not None:
            self.deleted_by = user
        super().soft_delete_cascade_policy_action()
        # Insert here custom post delete logic
    
    def __str__(self):
        return f"{self.uuid}"

    def get_absolute_url(self):
        return reverse_lazy('image:image_detail', kwargs={'uuid': self.uuid})

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"



    
