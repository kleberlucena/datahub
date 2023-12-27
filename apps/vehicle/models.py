import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend

from base.models import Base, SoftDelete, Registry
from apps.person.models import Person
from apps.portal.models import Entity, Military


""" def get_entity_from_created_by(obj):
    # Recupera a entity a partir do user que criou o objeto
    user = obj.created_by
    military = Military.objects.get(cpf=user.username)
    entity = Entity.objects.get(id=military.entity.id)
    return entity """


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
    placaPreMercosul = models.CharField(max_length=11, null=True, blank=True)
    dataPreCadastro = models.CharField(max_length=50, null=True, blank=True)
    dataEmplacamento = models.CharField(max_length=50, null=True, blank=True)
    chassi = models.CharField(max_length=30, null=True, blank=True)
    identificadorUnicoVeiculo = models.CharField(
        max_length=30, null=True, blank=True)
    tipoDocumentoFaturado = models.CharField(
        max_length=30, null=True, blank=True)
    mesFabricacaoVeiculo = models.CharField(
        max_length=30, null=True, blank=True)
    ufDestinoVeiculoFaturado = models.CharField(
        max_length=30, null=True, blank=True)
    numeroIdentificacaoFaturado = models.CharField(
        max_length=50, null=True, blank=True)
    ufFatura = models.CharField(max_length=20, null=True, blank=True)
    ufJurisdicaoVeiculo = models.CharField(
        max_length=20, null=True, blank=True)
    ufEmplacamento = models.CharField(max_length=50, null=True, blank=True)
    tipoDocumentoProprietario = models.CharField(
        max_length=30, null=True, blank=True)
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
    capacidadeMaximaCarga = models.CharField(
        max_length=50, null=True, blank=True)
    pesoBrutoTotal = models.CharField(max_length=50, null=True, blank=True)
    capacidadeMaximaTracao = models.CharField(
        max_length=17, null=True, blank=True)
    indicadorRemarcacaoChassi = models.BooleanField(null=True, blank=True)
    numeroCaixaCambio = models.CharField(max_length=255, null=True, blank=True)
    quantidadeEixo = models.CharField(max_length=255, null=True, blank=True)
    numeroEixoTraseiro = models.CharField(
        max_length=255, null=True, blank=True)
    numeroEixoAuxiliar = models.CharField(
        max_length=255, null=True, blank=True)
    numeroMotor = models.CharField(max_length=255, null=True, blank=True)
    tipoMontagem = models.CharField(max_length=255, null=True, blank=True)
    numeroIdentificacaoImportador = models.CharField(
        max_length=255, null=True, blank=True)
    numeroDeclaracaoImportacao = models.CharField(
        max_length=255, null=True, blank=True)
    dataDeclaracaoImportacao = models.CharField(
        max_length=50, null=True, blank=True)
    codigoOrgaoSRF = models.CharField(max_length=255, null=True, blank=True)
    descricaoOrgaoRegiaoFiscal = models.CharField(
        max_length=255, null=True, blank=True)
    dataLimiteRestricaoTributaria = models.CharField(
        max_length=50, null=True, blank=True)
    restricaoVeiculo1 = models.CharField(max_length=255, null=True, blank=True)
    restricaoVeiculo2 = models.CharField(max_length=255, null=True, blank=True)
    restricaoVeiculo3 = models.CharField(max_length=255, null=True, blank=True)
    restricaoVeiculo4 = models.CharField(max_length=255, null=True, blank=True)
    dataLimiteRestricaoTributaria = models.CharField(
        max_length=50, null=True, blank=True)
    indicadorVeiculoLicenciadoCirculacao = models.CharField(
        max_length=255, null=True, blank=True)
    renavam = models.CharField(max_length=255, null=True, blank=True)
    codigoMunicipioEmplacamento = models.CharField(
        max_length=50, null=True, blank=True)
    dataAtualizacaoRouboFurto = models.CharField(
        max_length=50, null=True, blank=True)
    dataAtualizacaoAlarme = models.CharField(
        max_length=50, null=True, blank=True)
    indicadorVeiculoNacional = models.BooleanField(null=True, blank=True)
    numeroLicencaUsoConfiguracaoVeiculosMotor = models.CharField(
        max_length=50, null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    codigoCategoria = models.IntegerField(null=True, blank=True)
    dataEmissaoUltimoCRV = models.CharField(
        max_length=50, null=True, blank=True)
    numeroSequenciaCRV = models.CharField(max_length=50, null=True, blank=True)
    numeroCRV = models.CharField(max_length=50, null=True, blank=True)
    numeroViaCRV = models.IntegerField(null=True, blank=True)
    codigoSegurancaCRV = models.CharField(max_length=50, null=True, blank=True)
    numeroTipoCRLV = models.CharField(max_length=50, null=True, blank=True)
    dataEmissaoCRLV = models.CharField(max_length=50, null=True, blank=True)
    numeroViaCRLV = models.IntegerField(null=True, blank=True)
    anoUltimoLicenciamnento = models.IntegerField(null=True, blank=True)
    mesAnoValidadeLicenciamento = models.IntegerField(null=True, blank=True)
    valorIPVA = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    dataAtualizacaoVeiculo = models.CharField(
        max_length=50, null=True, blank=True)
    dataHoraAtualizacaoVeiculo = models.CharField(
        max_length=50, null=True, blank=True)
    numeroProcessoImportacao = models.CharField(
        max_length=50, null=True, blank=True)
    paisTransferenciaVeiculo = models.CharField(
        max_length=50, null=True, blank=True)
    origemPossuidor = models.CharField(max_length=255, null=True, blank=True)
    quantidadeRestricoesBaseEmplacamento = models.CharField(
        max_length=50, null=True, blank=True)
    registroAduaneiro = models.CharField(max_length=50, null=True, blank=True)
    situacaoVeiculo = models.CharField(max_length=50, null=True, blank=True)
    codigoMarcaModelo = models.IntegerField(null=True, blank=True)
    codigoEspecie = models.IntegerField(null=True, blank=True)
    codigoTipoVeiculo = models.IntegerField(null=True, blank=True)
    codigoCor = models.IntegerField(null=True, blank=True)
    codigoCarroceira = models.IntegerField(null=True, blank=True)
    restricao = models.JSONField(null=True)
    indiceNacionalVeiculos = models.JSONField(null=True)
    dataReplicacao = models.CharField(max_length=50, null=True, blank=True)
    flagAtivo = models.BooleanField(null=True, blank=True)
    proprietario = models.ForeignKey(
        PersonRenavamCortex, related_name='veiculos_proprio', on_delete=models.CASCADE, null=True, blank=True)
    possuidor = models.ForeignKey(
        PersonRenavamCortex, related_name='veiculos_em_posse', on_delete=models.CASCADE, null=True, blank=True)
    arrendatario = models.ForeignKey(
        PersonRenavamCortex, related_name='veiculos_arrendado', on_delete=models.CASCADE, null=True, blank=True)

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
    person_renavam_cortex = models.ForeignKey(
        PersonRenavamCortex, related_name='registers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Registro Veículo Cortex"
        verbose_name_plural = "Registros Veículo Cortex"


class Vehicle(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    signal = models.CharField('PLACA', max_length=11,
                              null=True, blank=True, unique=True)
    chassi = models.CharField(max_length=30, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    model_year = models.CharField(max_length=5, null=True, blank=True)
    manufactured_year = models.CharField(max_length=5, null=True, blank=True)
    owner = models.ForeignKey(Person, related_name='own_vehicles', null=True,
                              blank=True, on_delete=models.RESTRICT)
    custodian = models.ForeignKey(Person, related_name='custody_vehicles', null=True,
                                  blank=True, on_delete=models.RESTRICT)
    renter = models.ForeignKey(Person, related_name='rented_vehicles', null=True,
                               blank=True, on_delete=models.RESTRICT)
    updated_by = models.ForeignKey(
        User,
        related_name='vehicle_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='vehicle_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    entity = models.ForeignKey(
        Entity,
        related_name='vehicles_entity',
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
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"


class VehicleImage(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("descrição", max_length=255)
    file = StdImageField(
        'imagem de veículo',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='vehicles_imagens',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True
    )
    vehicle = models.ForeignKey(
        Vehicle, related_name='images', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User,
        related_name='images_vehicle_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='images_vehicle_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    entity = models.ForeignKey(
        Entity,
        related_name='vehicleimages_entity',
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
        verbose_name = "Imagem de Veículo"
        verbose_name_plural = "Imagens de Veículo"


class Movimento(models.Model):
    idMovimento = models.BigIntegerField(null=True, blank=True)
    dataPassagem = models.DateTimeField(null=True, blank=True)
    local = models.CharField(max_length=1024, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    vehicle_cortex = models.ForeignKey(VehicleCortex, related_name='moviments_vehicle_cortex', null=True,
                              blank=True, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "movimento"
        verbose_name_plural = "movimentos"

    def __str__(self):
        return self.idMovimento
