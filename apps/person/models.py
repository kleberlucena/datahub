import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

from apps.address.models import Address
from apps.image.models import Image
from apps.document.models import Document


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


class Person(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    addresses = models.ManyToManyField(Address)
    images = models.ManyToManyField(Image)
    documents = models.ManyToManyField(Document)
    updated_by = models.ForeignKey(
        User,
        related_name='person_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='person_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def soft_delete_policy_action(self, user, **kwargs):
        # Insert here custom pre delete logic
        self.deleted_by = user
        super().soft_delete_policy_action(**kwargs)
        # Insert here custom post delete logic

    def __str__(self):
        return f"{self.uuid}"
    
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"


class Nickname(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nickname = models.CharField("Alcunha", max_length=255)
    person = models.ForeignKey(Person, related_name='nicknames', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User,
        related_name='nickname_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='nickname_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def soft_delete_policy_action(self, user, **kwargs):
        # Insert here custom pre delete logic
        self.deleted_by = user
        super().soft_delete_policy_action(**kwargs)
        # Insert here custom post delete logic

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Alcunha"
        verbose_name_plural = "Alcunhas"


class Tatoo(Base, SoftDelete):
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
    updated_by = models.ForeignKey(
        User,
        related_name='tatoo_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='tatoo_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def soft_delete_policy_action(self, user, **kwargs):
        # Insert here custom pre delete logic
        self.deleted_by = user
        super().soft_delete_policy_action(**kwargs)
        # Insert here custom post delete logic

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Tatuagem"
        verbose_name_plural = "Tatuagens"


class Physical(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("descrição", max_length=255)
    value = models.CharField("valor", max_length=255)
    person = models.ForeignKey(Person, related_name='physicals', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User,
        related_name='physical_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='physical_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def soft_delete_policy_action(self, user, **kwargs):
        # Insert here custom pre delete logic
        self.deleted_by = user
        super().soft_delete_policy_action(**kwargs)
        # Insert here custom post delete logic

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Atributo físico"
        verbose_name_plural = "Atributos físicos"


class Face(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ForeignKey(Image, related_name="faces", on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='faces', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User,
        related_name='face_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='face_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def soft_delete_policy_action(self, user, **kwargs):
        # Insert here custom pre delete logic
        self.deleted_by = user
        super().soft_delete_policy_action(**kwargs)
        # Insert here custom post delete logic

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Face"
        verbose_name_plural = "Faces"

