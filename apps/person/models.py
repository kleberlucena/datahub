import uuid
from django.db import models
from django.conf import settings
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend

from apps.address.models import Address
from apps.image.models import Image
from apps.document.models import Document


class Base(models.Model):
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class Person(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    addresses = models.ManyToManyField(Address)
    images = models.ManyToManyField(Image)
    documents = models.ManyToManyField(Document)

    def __str__(self):
        return f"{self.uuid}"
    
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"


class Nickname(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nickname = models.CharField("Alcunha", max_length=255)
    person = models.ForeignKey(Person, related_name='nicknames', on_delete=models.CASCADE)


class Tatoo(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("descrição", max_length=255)
    person = models.ForeignKey(Person, related_name='tatoos', on_delete=models.CASCADE)
    file = StdImageField(
        'Arquivo',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='tatoo_images',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 64, 'height': 64, 'crop': True},
        }, delete_orphans=True, null=True, blank=True)


class Physical(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("descrição", max_length=255)
    value = models.CharField("valor", max_length=255)
    person = models.ForeignKey(Person, related_name='physicals', on_delete=models.CASCADE)


class Face(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ForeignKey(Image, related_name="faces", on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='faces', on_delete=models.CASCADE)

