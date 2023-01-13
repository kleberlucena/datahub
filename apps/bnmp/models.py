import uuid
# from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
""" from stdimage.models import StdImageField
from django_minio_backend import MinioBackend """


class Base(models.Model):
    created_at = models.DateTimeField('Criado', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado', auto_now=True)

    class Meta:
        abstract = True


class PersonBNMP(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    idpessoa = models.IntegerField(null=True, blank=True)
    numeroCPF = models.CharField(max_length=14, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    alcunha = models.CharField(max_length=255, editable=True)
    nomeMae = models.CharField(max_length=255, blank=True, null=True)
    nomePai = models.CharField(max_length=255, blank=True, null=True)
    dataNascimento = models.DateTimeField(null=True, blank=True)
    sexo = models.CharField(max_length=255, blank=True, null=True)
    naturalidade = models.CharField(max_length=255, blank=True, null=True)
    statusPessoa = models.CharField(max_length=255, blank=True, null=True)
    indiceAssertividade = models.IntegerField(null=True, blank=True)
    tipoBuscaCPF = models.CharField(max_length=255, blank=True, null=True)
    
    updated_by = models.ForeignKey(
        User,
        related_name='bnmp_consult_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='bnmp_consult_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Pessoa BNMP"
        verbose_name_plural = "Pessoas BNMP"




