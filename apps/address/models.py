from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from localflavor.br.models import BRStateField, BRPostalCodeField
from django.contrib.gis.db import models as geo_models
import uuid


class Base(models.Model):
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)
    active = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True


class Address(Base):
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
    country = models.CharField('País', default='Brasil', max_length=155, null=True, blank=True)
    zipcode = BRPostalCodeField('CEP', null=True, blank=True)
    place = geo_models.PointField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        related_name='address_creator',
        on_delete=models.SET_NULL,
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

    def get_absolute_url(self):
        return reverse_lazy('address:address_detail', kwargs={'pk': self.pk})


    def __str__(self):
        return f"{self.street} {self.number} {self.complement} {self.neighborhood} {self.city} {self.state} {self.region} {self.country} {self.zipcode}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"


# class Visit(Base):
#     label = models.CharField(max_length=255, null=True, blank=True)
#     place = geo_models.PointField(max_length=255, null=True, blank=True)
#     datetime = models.DateTimeField('Quando')
#     updated_by = models.ForeignKey(
#         User,
#         related_name='visit_updater',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     created_by = models.ForeignKey(
#         User,
#         related_name='visit_creator',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     def get_absolute_url(self):
#         return reverse_lazy('address:visit_detail', kwargs={'pk': self.pk})

#     def soft_delete_policy_action(self, user, **kwargs):
#         # Insert here custom pre delete logic
#         self.deleted_by = user
#         super().soft_delete_policy_action(**kwargs)
#         # Insert here custom post delete logic

#     def __str__(self):
#         return f"{self.label} {self.place} {self.datetime}"

#     class Meta:
#         verbose_name = "Visita"
#         verbose_name_plural = "Visitas"
