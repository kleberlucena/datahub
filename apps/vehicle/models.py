import uuid
from django.db import models

from base.models import Base, SoftDelete, Registry


class PersonRenavamCortex(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tipoDocumento = models.CharField(max_length=30, null=True, blank=True)
    numeroDocumento = models.CharField(max_length=50, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)

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
        verbose_name = "Pessoa Renavan Cortex"
        verbose_name_plural = "Pessoas Renavan Cortex"


class VehicleCortex(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    placa = models.CharField(max_length=11, unique=True)
    dataEmplacamento = models.DateTimeField(null=True, blank=True)
    chassi = models.CharField(max_length=30, null=True, blank=True)
    tipoDocumentoFaturado = models.CharField(max_length=30, null=True, blank=True)
    numeroIdentificacaoFaturado = models.CharField(max_length=50, null=True, blank=True)
    ufFatura = models.CharField(max_length=50, null=True, blank=True)
    tipoDocumentoProprietario = models.CharField(max_length=30, null=True, blank=True)
    ufEmplacamento = models.CharField(max_length=50, null=True, blank=True)
    municipioPlaca = models.CharField(max_length=255, null=True, blank=True)
    anoFabricacao = models.CharField(max_length=5, null=True, blank=True)
    anoModelo = models.CharField(max_length=5, null=True, blank=True)
    marcaModelo = models.CharField(max_length=255, null=True, blank=True)
    grupoVeiculo = models.CharField(max_length=255, null=True, blank=True)
    tipoVeiculo = models.CharField(max_length=255, null=True, blank=True)
    especie = models.CharField(max_length=255, null=True, blank=True)
    carroceria = models.CharField(max_length=255, null=True, blank=True)
    numeroCarroceria = models.CharField(max_length=8, null=True, blank=True)
    cor = models.CharField(max_length=255, null=True, blank=True)
    combustivel = models.CharField(max_length=50, null=True, blank=True)
    potencia = models.CharField(max_length=50, null=True, blank=True)
    cilindrada = models.CharField(max_length=50, null=True, blank=True)
    lotacao = models.CharField(max_length=50, null=True, blank=True)
    capacidadeMaximaCarga = models.CharField(max_length=50, null=True, blank=True)
    pesoBrutoTotal = models.CharField(max_length=50, null=True, blank=True)        
    capacidadeMaximaTracao = models.CharField(max_length=17, null=True, blank=True)
    indicadorRemarcacaoChassi = models.BooleanField(null=True, blank=True)
    numeroCaixaCambio = models.CharField(max_length=255, null=True, blank=True)
    quantidadeEixo = models.CharField(max_length=255, null=True, blank=True)
    numeroEixoTraseiro = models.CharField(max_length=255, null=True, blank=True)
    numeroEixoAuxiliar = models.CharField(max_length=255, null=True, blank=True)
    numeroMotor = models.CharField(max_length=255, null=True, blank=True)
    tipoMontagem = models.CharField(max_length=255, null=True, blank=True)
    numeroIdentificacaoImportador = models.CharField(max_length=255, null=True, blank=True)
    numeroDeclaracaoImportacao = models.CharField(max_length=255, null=True, blank=True)
    dataDeclaracaoImportacao = models.DateTimeField(null=True, blank=True)
    codigoOrgaoSRF = models.CharField(max_length=255, null=True, blank=True)
    dataDeclaracaoImportacao = models.DateTimeField(null=True, blank=True)
    restricaoVeiculo1 = models.CharField(max_length=255, null=True, blank=True)
    restricaoVeiculo2 = models.CharField(max_length=255, null=True, blank=True)
    restricaoVeiculo3 = models.CharField(max_length=255, null=True, blank=True)
    restricaoVeiculo4 = models.CharField(max_length=255, null=True, blank=True)
    dataLimiteRestricaoTributaria = models.DateField(null=True, blank=True)
    indicadorVeiculoLicenciadoCirculacao = models.CharField(max_length=255, null=True, blank=True)
    renavam = models.CharField(max_length=255, null=True, blank=True)
    codigoMunicipioEmplacamento = models.CharField(max_length=50, null=True, blank=True)
    dataAtualizacaoRouboFurto = models.DateField(null=True, blank=True)
    dataAtualizacaoAlarme = models.DateField(null=True, blank=True)
    indicadorVeiculoNacional = models.BooleanField(null=True, blank=True)
    numeroLicencaUsoConfiguracaoVeiculosMotor = models.CharField(max_length=50, null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    codigoCategoria = models.IntegerField(null=True, blank=True)
    dataEmissaoUltimoCRV = models.DateField(null=True, blank=True)
    dataAtualizacaoVeiculo = models.DateTimeField(null=True, blank=True)
    dataHoraAtualizacaoVeiculo = models.DateTimeField(null=True, blank=True)
    numeroProcessoImportacao = models.CharField(max_length=50, null=True, blank=True)
    paisTransferenciaVeiculo = models.CharField(max_length=50, null=True, blank=True)
    origemPossuidor = models.CharField(max_length=255, null=True, blank=True)
    quaantidadeRestricoesBaseEmplacamento = models.CharField(max_length=50, null=True, blank=True)
    registroAduaneiro = models.CharField(max_length=50, null=True, blank=True)
    situacaoVeiculo = models.CharField(max_length=50, null=True, blank=True)
    codigoMarcaModelo = models.IntegerField(null=True, blank=True)
    codigoEspecie = models.IntegerField(null=True, blank=True)
    codigoTipoVeiculo = models.IntegerField(null=True, blank=True)
    codigoCor = models.IntegerField(null=True, blank=True)
    restricao = models.JSONField(null=True)
    """ nomeProprietario  = models.CharField(max_length=255, null=True, blank=True)
    nomePossuidor = models.CharField(max_length=255, null=True, blank=True)
    nomeArrendatario = models.CharField(max_length=255, null=True, blank=True) """
    proprietario = models.ForeignKey(PersonRenavamCortex, related_name='veiculos_proprio', on_delete=models.CASCADE, null=True, blank=True)
    possuidor = models.ForeignKey(PersonRenavamCortex, related_name='veiculos_em_posse', on_delete=models.CASCADE, null=True, blank=True)
    arrendatario = models.ForeignKey(PersonRenavamCortex, related_name='veiculos_arrendado', on_delete=models.CASCADE, null=True, blank=True)
    
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
        verbose_name = "Veículo Cortex"
        verbose_name_plural = "Veículos Cortex"


class RegistryVehicleCortex(Registry):
    person_renavan_cortex = models.ForeignKey(PersonRenavamCortex, related_name='registers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Registro Veículo Cortex"
        verbose_name_plural = "Registros Veículo Cortex"