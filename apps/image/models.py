from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy
from django.db import models
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend
import uuid


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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
    created_by = models.ForeignKey(
        User,
        related_name='image_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)
    
    def __str__(self):
        return f"{self.id}"

    def get_absolute_url(self):
        return reverse_lazy('image:image_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"



    
