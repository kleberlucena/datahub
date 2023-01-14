import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
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


class PersonCortex(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    numeroCPF = models.CharField(max_length=11, unique=True)
    nomeCompleto = models.CharField(max_length=255, null=True, blank=True)
    nomeMae = models.CharField(max_length=255, null=True, blank=True)
    dataNascimento = models.DateField(null=True, blank=True)
    situacaoCadastral = models.CharField(max_length=50, null=True, blank=True)
    identificadorResidenteExterior = models.CharField(max_length=50, null=True,
                                                   blank=True)
    paisResidencia = models.CharField(max_length=50, null=True, blank=True)
    sexo = models.CharField(max_length=50, null=True, blank=True)
    naturezaOcupacao = models.CharField(max_length=255, null=True, blank=True)
    ocupacaoPrincipal = models.CharField(max_length=255, null=True, blank=True)
    anoExercicioOcupacao = models.CharField(max_length=4, null=True, blank=True)
    tipoLogradouro = models.CharField(max_length=50, null=True, blank=True)
    logradouro = models.CharField(max_length=255, null=True, blank=True)
    numeroLogradouro = models.CharField(max_length=10, null=True, blank=True)
    complementoLogradouro = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    municipio = models.CharField(max_length=50, null=True, blank=True)
    ddd = models.CharField(max_length=10, null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    regiaoFiscal = models.CharField(max_length=50, null=True, blank=True)
    anoObito = models.CharField(max_length=4, null=True, blank=True)
    indicadorEstrangeiro = models.CharField(max_length=50, null=True, blank=True)
    dataAtualizacao = models.DateTimeField(null=True, blank=True)
    tituloEleitor = models.CharField(max_length=17, null=True, blank=True)
    indicadorMoradorEstrangeiro = models.BooleanField(null=True, blank=True)
    latitudeAproximadaLocal = models.FloatField(null=True, blank=True)
    longitudeAproximadaLocal = models.FloatField(null=True, blank=True)
    municipioNaturalidade = models.CharField(max_length=255, null=True, blank=True)
    nomeSocial = models.CharField(max_length=255, null=True, blank=True)
    paisNascimento = models.CharField(max_length=255, null=True, blank=True)
    ufNaturalidade = models.CharField(max_length=255, null=True, blank=True)

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
        verbose_name = "Pessoa Cortex"
        verbose_name_plural = "Pessoas Cortex"