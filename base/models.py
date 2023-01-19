import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager

from apps.person.models import Person


class Base(models.Model):
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class Registry(Base, PolymorphicModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    person = models.ForeignKey(Person, related_name='registers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"
