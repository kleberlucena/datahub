import uuid
# from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from base.models import Base, SoftDelete, Registry


class PersonBNMP(Base, SoftDelete):
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
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Pessoa BNMP"
        verbose_name_plural = "Pessoas BNMP"


class MandadoPrisao(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    seqPeca = models.IntegerField(null=True, blank=True)
    dataCriacao = models.DateField(null=True, blank=True)
    numeroProcesso = models.CharField(max_length=255, null=True, blank=True)
    numeroPeca = models.CharField(max_length=255, null=True, blank=True)
    tipoPeca = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    nomeServidor = models.CharField(max_length=255, null=True, blank=True)
    cargoServidor = models.CharField(max_length=255, null=True, blank=True)
    nomeMagistrado = models.CharField(max_length=255, null=True, blank=True)
    textoJustificativaCancelamento = models.CharField(max_length=255, null=True, blank=True)
    dataConfirmacaoServidor = models.DateField(null=True, blank=True)
    dataExpedicao = models.DateField(null=True, blank=True)
    dataConclusao = models.DateField(null=True, blank=True)
    dataExpiracaoPrisaoMandadoPrisao = models.DateField(null=True, blank=True)
    dataVencimentoMandados = models.DateField(null=True, blank=True)
    orgaoJudiciario = models.CharField(max_length=255, null=True, blank=True)
    dataValidade = models.DateField(null=True, blank=True)
    numeroPrazoPrisao = models.CharField(max_length=255, null=True, blank=True)
    dataInfracao = models.DateField(null=True, blank=True)
    descricaoLocalOcorrencia = models.CharField(max_length=255, null=True, blank=True)
    sinteseDecisao =  models.TextField(max_length=255, null=True, blank=True)
    tempoPenaAno = models.CharField(max_length=255, null=True, blank=True)
    tempoPenaMes = models.CharField(max_length=255, null=True, blank=True)
    tempoPenaDia = models.CharField(max_length=255, null=True, blank=True)
    descricaoCumprimento  =  models.TextField(max_length=255, null=True, blank=True)
    observacao  = models.CharField(max_length=255, null=True, blank=True)
    regimePrisional  = models.CharField(max_length=255, null=True, blank=True)
    especiePrisao  = models.CharField(max_length=255, null=True, blank=True)
    sigilo = models.CharField(max_length=255, null=True, blank=True)
    descricaoJustificativa  = models.CharField(max_length=255, null=True, blank=True)
    nomeEstabelecimentoPrisional  = models.CharField(max_length=255, null=True, blank=True)
    dataPrisao  = models.DateField(null=True, blank=True)
    ufCustodia = models.CharField(max_length=255, null=True, blank=True)
    municipioCustodia = models.CharField(max_length=255, null=True, blank=True)
    linkMandadoPrisao = models.URLField(max_length=255, null=True, blank=True)
    tipificacaoPenal = models.JSONField(null=True, blank=True)
    person_bnmp = models.ForeignKey(PersonBNMP, related_name='mandados', on_delete=models.CASCADE, null=True, blank=True)
    
    updated_by = models.ForeignKey(
        User,
        related_name='bnmp_mandado_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='bnmp_mandado_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Mandado de Prisao"
        verbose_name_plural = "Mandados de Prisao"


class RegistryBNMP(Registry):
    person_bnmp = models.ForeignKey(PersonBNMP, related_name='registers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Registro BNMP"
        verbose_name_plural = "Registros BNMP"