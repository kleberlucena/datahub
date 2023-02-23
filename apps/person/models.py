import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo_models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
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
    addresses = models.ManyToManyField(
        Address,
        through='PersonAddresses',
        through_fields=('person', 'address'),
    )
    images = models.ManyToManyField(
        Image,
        through='PersonImages',
        through_fields=('person', 'image'),
    )
    documents = models.ManyToManyField(
        Document,
        through='PersonDocuments',
        through_fields=('person', 'document'),
    )
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

    @receiver(pre_delete, sender=Address)
    def delete_related_jobs(sender, instance, **kwargs):
        for address in instance.addresses.all():
            # No remaining projects
            if not address.persons.exclude(id=instance.id).count():
                address.delete()

    @receiver(pre_delete, sender=Document)
    def delete_related_jobs(sender, instance, **kwargs):
        for document in instance.documents.all():
            # No remaining projects
            if not document.persons.exclude(id=instance.id).count():
                document.delete()

    @receiver(pre_delete, sender=Address)
    def delete_related_jobs(sender, instance, **kwargs):
        for address in instance.addresses.all():
            # No remaining projects
            if not address.persons.exclude(id=instance.id).count():
                address.delete()

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
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"


class PersonAddresses(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    addressType = models.CharField(max_length=64, null=True, blank=True)


class PersonDocuments(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class PersonImages(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Nickname(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("Alcunha", max_length=255)
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
        verbose_name = "Alcunha"
        verbose_name_plural = "Alcunhas"


class Tattoo(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("descrição", max_length=255, blank=True, null=True)
    person = models.ForeignKey(Person, related_name='tattoos', on_delete=models.CASCADE)
    point = geo_models.PointField(null=True, blank=True)
    file = StdImageField(
        'Arquivo',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='tattoo_images',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        User,
        related_name='tattoo_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='tattoo_creator',
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
        verbose_name = "Atributo físico"
        verbose_name_plural = "Atributos físicos"


class Face(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file = StdImageField(
        'Imagem',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='faces_imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True
    )
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
        verbose_name = "Face"
        verbose_name_plural = "Faces"