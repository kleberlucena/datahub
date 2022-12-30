import uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


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


class DocumentType(Base, SoftDelete):
    emitter_department = models.CharField(max_length=255, null=True, blank=True, editable=True)
    label = models.CharField(max_length=255, editable=True)
    updated_by = models.ForeignKey(
        User,
        related_name='document_type_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='document_type_creator',
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
        return f"{self.id}"

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"


class Document(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    mother = models.CharField("mãe", max_length=255, blank=True, null=True)
    father = models.CharField("pai", max_length=255, blank=True, null=True)
    type = models.ForeignKey(DocumentType, related_name='emitidos', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        User,
        related_name='document_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='document_creator',
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

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"


class DocumentImage(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("descrição", max_length=255, blank=True, null=True)
    file = StdImageField(
        'Arquivo',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='document_images',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 64, 'height': 64, 'crop': True},
        }, delete_orphans=True, null=True, blank=True)
    document = models.ForeignKey(Document, related_name='images', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(
        User,
        related_name='document_image_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='document_image_updater',
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
        return f"{self.file.url}"

    class Meta:
        verbose_name = "Imagem de documento"
        verbose_name_plural = "Imagens de documento"

