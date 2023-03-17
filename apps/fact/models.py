import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend

from base.models import Base, SoftDelete, Registry
from apps.address.models import Address
from apps.person.models import Person
from apps.portal.models import Entity


class Fact(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("Descrição", max_length=255)
    description = models.TextField("Relato", null=True, blank=True)
    start_time = models.DateTimeField("Início")
    end_time = models.DateTimeField("Término", null=True, blank=True)
    addresses = models.ManyToManyField(
        Address,
        through='FactAddresses',
        through_fields=('fact', 'address'),
    )
    victims = models.ManyToManyField(
        Person,
        through='FactVictims',
        through_fields=('fact', 'victim'),
    )
    suspects = models.ManyToManyField(
        Person,
        through='FactSuspects',
        through_fields=('fact', 'suspect'),
    )
    witnesses = models.ManyToManyField(
        Person,
        through='FactWitnesses',
        through_fields=('fact', 'witness'),
    )
    updated_by = models.ForeignKey(
        User,
        related_name='fact_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='fact_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    entity = models.ForeignKey(
        Entity, 
        related_name='fact_entity', 
        on_delete=models.PROTECT,
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
        verbose_name = "Fato"
        verbose_name_plural = "Fatos"


class FactImage(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("Descrição", max_length=255, blank=True, null=True)
    fact = models.ForeignKey(Fact, related_name='images', on_delete=models.RESTRICT)
    file = StdImageField(
        'Arquivo',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='fact_images',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, null=True, blank=True)
    entity = models.ForeignKey(
        Entity, 
        related_name='image_fact_entity', 
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='image_fact_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='image_fact_creator',
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
        verbose_name = "Imagem de Fato"
        verbose_name_plural = "Imagens de Fato"


class FactAddresses(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.RESTRICT)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)


class FactVictims(models.Model):
    victim = models.ForeignKey(Person, on_delete=models.CASCADE)
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)


class FactSuspects(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    suspect = models.ForeignKey(Person, on_delete=models.CASCADE)


class FactWitnesses(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    witness = models.ForeignKey(Person, on_delete=models.CASCADE)