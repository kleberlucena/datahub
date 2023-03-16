import uuid
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from localflavor.br.models import BRStateField, BRPostalCodeField
from django.contrib.gis.db import models as geo_models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE

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


class Address(Base, SoftDelete):
    REGION = (
        ('CO', 'Centro-Oeste'),
        ('N', 'Norte'),
        ('NE', 'Nordeste'),
        ('S', 'Sul'),
        ('SE', 'Sudeste')
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    street = models.CharField('Logradouro', max_length=255, null=True, blank=True)
    number = models.CharField('Número', max_length=9, null=True, blank=True)
    complement = models.CharField('Complemento', max_length=255, null=True, blank=True)
    neighborhood = models.CharField('Bairro', max_length=155, null=True, blank=True)
    city = models.CharField('Cidade', max_length=155, null=True, blank=True)
    state = BRStateField('Estado', default='PB', null=True, blank=True)
    region = models.CharField('Região', max_length=2, choices=REGION, default='NE', null=True, blank=True)
    country = models.CharField('País', max_length=155, default='Brasil', null=True, blank=True)
    zipcode = BRPostalCodeField('CEP', null=True, blank=True)
    place = geo_models.PointField(srid=4326, null=True, blank=True)
    entity = models.ForeignKey(
        Entity, 
        related_name='addresses_entity', 
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='address_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='address_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    """ def get_absolute_url(self):
        return reverse_lazy('address:address_detail', kwargs={'uuid': self.uuid}) """

    def soft_delete_cascade_policy_action(self, **kwargs):
        # Insert here custom pre delete logic
        user = kwargs['deleted_by']
        if user is not None:
            self.deleted_by = user
        super().soft_delete_cascade_policy_action()
        # Insert here custom post delete logic

    def __str__(self):
        return f"{self.uuid} {self.street} {self.number} {self.complement} {self.neighborhood} {self.city}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"