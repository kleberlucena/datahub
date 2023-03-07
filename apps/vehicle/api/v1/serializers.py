from rest_framework import serializers
from guardian.shortcuts import get_perms
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer

from apps.vehicle.models import PersonRenavamCortex, VehicleCortex, Vehicle, VehicleImage
from base.models import Registry
from apps.person.models import Person
from apps.person.api.v1.serializers import NicknameSerializer, FaceSerializer, AddressSerializer, ImageSerializer, TattooSerializer, PhysicalSerializer, DocumentSerializer
from apps.watermark import helpers as watermark_helpers


class PersonToVehicleSerializer(serializers.ModelSerializer):
    nicknames = NicknameSerializer(many=True, required=False)
    faces = FaceSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    tattoos = TattooSerializer(many=True, required=False)
    physicals = PhysicalSerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')
    
    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Person
        fields = (
            'uuid', 'nicknames', 'addresses', 'images', 'faces', 'documents', 'tattoos', 'physicals',
            'created_at', 'updated_at', 'permissions')


class RegistryVehicleSerializer(serializers.ModelSerializer):
    person = PersonToVehicleSerializer(read_only=True)
    # person_cortex = PersonToCortexSerializer(read_only=True, required=False, allow_null=True)

    class Meta:
        model = Registry
        fields =  ('uuid', 'created_at', 'updated_at', 'person')


class PersonRenavamCortexSerializer(serializers.ModelSerializer):
    registers = RegistryVehicleSerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = PersonRenavamCortex
        fields = ("uuid", "tipoDocumento", "numeroDocumento", "nome", "endereco", "registers")


class ProprietarioRenavamCortexSerializer(serializers.ModelSerializer):
    registers = RegistryVehicleSerializer(many=True, read_only=True, required=False, allow_null=True)
    tipoDocumentoProprietario = serializers.CharField(source="tipoDocumento")
    numeroDocumentoProprietario = serializers.CharField(source="numeroDocumento")
    nomeProprietario = serializers.CharField(source="nome")
    enderecoProprietario = serializers.CharField(source="endereco")

    class Meta:
        model = PersonRenavamCortex
        fields = ("uuid", "tipoDocumentoProprietario", "numeroDocumentoProprietario", "nomeProprietario", "enderecoProprietario", "registers")


class PossuidorRenavamCortexSerializer(serializers.ModelSerializer):
    registers = RegistryVehicleSerializer(many=True, read_only=True, required=False, allow_null=True)
    tipoDocumentoPossuidor = serializers.CharField(source="tipoDocumento")
    numeroDocumentoPossuidor = serializers.CharField(source="numeroDocumento")
    nomePossuidor = serializers.CharField(source="nome")
    enderecoPossuidor = serializers.CharField(source="endereco")

    class Meta:
        model = PersonRenavamCortex
        fields = ("uuid", "tipoDocumentoPossuidor", "numeroDocumentoPossuidor", "nomePossuidor", "enderecoPossuidor", "registers")


class ArrendatarioRenavamCortexSerializer(serializers.ModelSerializer):
    registers = RegistryVehicleSerializer(many=True, read_only=True, required=False, allow_null=True)
    tipoDocumentoArrendatario = serializers.CharField(source="tipoDocumento")
    numeroDocumentoArrendatario = serializers.CharField(source="numeroDocumento")
    nomeArrendatario = serializers.CharField(source="nome")
    enderecoArrendatario = serializers.CharField(source="endereco")

    class Meta:
        model = PersonRenavamCortex
        fields = ("uuid", "tipoDocumentoArrendatario", "numeroDocumentoArrendatario", "nomeArrendatario", "enderecoArrendatario", "registers")


class ProprietarioBasicRenavamCortexSerializer(serializers.ModelSerializer):
    nomeProprietario = serializers.CharField(source="nome")

    class Meta:
        model = PersonRenavamCortex
        fields = ("nomeProprietario",)


class ProprietarioIntermediateRenavamCortexSerializer(serializers.ModelSerializer):
    tipoDocumentoProprietario = serializers.CharField(source="tipoDocumento")
    numeroDocumentoProprietario = serializers.CharField(source="numeroDocumento")
    nomeProprietario = serializers.CharField(source="nome")

    class Meta:
        model = PersonRenavamCortex
        fields = ("tipoDocumentoProprietario", "numeroDocumentoProprietario", "nomeProprietario")


class PossuidorIntermediateRenavamCortexSerializer(serializers.ModelSerializer):
    tipoDocumentoPossuidor = serializers.CharField(source="tipoDocumento")
    numeroDocumentoPossuidor = serializers.CharField(source="numeroDocumento")
    nomePossuidor = serializers.CharField(source="nome")

    class Meta:
        model = PersonRenavamCortex
        fields = ("tipoDocumentoPossuidor", "numeroDocumentoPossuidor", "nomePossuidor")


class ArrendatarioIntermediateRenavamCortexSerializer(serializers.ModelSerializer):
    tipoDocumentoArrendatario = serializers.CharField(source="tipoDocumento")
    numeroDocumentoArrendatario = serializers.CharField(source="numeroDocumento")
    nomeArrendatario = serializers.CharField(source="nome")

    class Meta:
        model = PersonRenavamCortex
        fields = ("tipoDocumentoArrendatario", "numeroDocumentoArrendatario", "nomeArrendatario")


class VehicleCortexSerializer(serializers.ModelSerializer):    
    dataDeclaracaoImportacao = serializers.DateTimeField(format=None)
    dataEmplacamento = serializers.DateTimeField(format=None)
    proprietario = ProprietarioRenavamCortexSerializer(read_only=True, required=False)
    possuidor = PossuidorRenavamCortexSerializer(read_only=True, required=False)
    arrendatario = ArrendatarioRenavamCortexSerializer(read_only=True, required=False)

    class Meta:
        model = VehicleCortex
        fields = ("uuid", "placa", "dataEmplacamento", "chassi", "tipoDocumentoFaturado", "numeroIdentificacaoFaturado", 
                  "ufFatura", "tipoDocumentoProprietario", "ufEmplacamento", "municipioPlaca", "anoFabricacao", "anoModelo", 
                  "marcaModelo", "grupoVeiculo", "tipoVeiculo", "especie", "carroceria", "numeroCarroceria", "cor", 
                  "combustivel", "potencia", "cilindrada", "lotacao", "capacidadeMaximaCarga", "pesoBrutoTotal", 
                  "capacidadeMaximaTracao", "indicadorRemarcacaoChassi", "numeroCaixaCambio", "quantidadeEixo", "numeroEixoTraseiro",
                  "numeroEixoAuxiliar", "numeroMotor", "tipoMontagem", "numeroIdentificacaoImportador", "numeroDeclaracaoImportacao",
                  "dataDeclaracaoImportacao", "codigoOrgaoSRF", "dataDeclaracaoImportacao", "restricaoVeiculo1", "restricaoVeiculo2", 
                  "restricaoVeiculo3", "restricaoVeiculo4", "dataLimiteRestricaoTributaria", "indicadorVeiculoLicenciadoCirculacao", 
                  "renavam", "codigoMunicipioEmplacamento", "dataAtualizacaoRouboFurto", "dataAtualizacaoAlarme", 
                  "indicadorVeiculoNacional", "numeroLicencaUsoConfiguracaoVeiculosMotor", "categoria", "codigoCategoria", 
                  "dataEmissaoUltimoCRV", "dataHoraAtualizacaoVeiculo", "numeroProcessoImportacao", "paisTransferenciaVeiculo", 
                  "origemPossuidor", "quaantidadeRestricoesBaseEmplacamento", "registroAduaneiro", "situacaoVeiculo", 
                  "codigoMarcaModelo", "codigoEspecie", "codigoTipoVeiculo", "codigoCor", "restricao", 
                  "proprietario", "possuidor", "arrendatario")


class IntermediateVehicleCortexSerializer(serializers.ModelSerializer):
    dataEmplacamento = serializers.DateTimeField(format=None)
    proprietario = ProprietarioIntermediateRenavamCortexSerializer(read_only=True, required=False)
    possuidor = PossuidorIntermediateRenavamCortexSerializer(read_only=True, required=False)
    arrendatario = ArrendatarioIntermediateRenavamCortexSerializer(read_only=True, required=False)

    class Meta:
        model = VehicleCortex
        fields = ("uuid", "placa", "dataEmplacamento", "chassi", "ufEmplacamento", "municipioPlaca", "anoFabricacao", "anoModelo", 
                  "marcaModelo", "grupoVeiculo", "tipoVeiculo", "especie", "cor", 
                  "combustivel", "potencia", "cilindrada", "lotacao", "capacidadeMaximaCarga", "pesoBrutoTotal", 
                  "capacidadeMaximaTracao", "indicadorRemarcacaoChassi", "numeroCaixaCambio", "quantidadeEixo", "numeroEixoTraseiro",
                  "numeroEixoAuxiliar", "numeroMotor", "tipoMontagem", "restricaoVeiculo1", "restricaoVeiculo2", 
                  "restricaoVeiculo3", "restricaoVeiculo4", "dataLimiteRestricaoTributaria", "indicadorVeiculoLicenciadoCirculacao", 
                  "renavam", "codigoMunicipioEmplacamento", "dataAtualizacaoRouboFurto", "dataAtualizacaoAlarme", 
                  "indicadorVeiculoNacional", "numeroLicencaUsoConfiguracaoVeiculosMotor", "categoria", "codigoCategoria", 
                  "dataEmissaoUltimoCRV", "dataHoraAtualizacaoVeiculo", "numeroProcessoImportacao", "paisTransferenciaVeiculo", 
                  "origemPossuidor", "quaantidadeRestricoesBaseEmplacamento", "registroAduaneiro", "situacaoVeiculo", 
                  "codigoMarcaModelo", "codigoEspecie", "codigoTipoVeiculo", "codigoCor", "restricao", 
                  "proprietario", "possuidor", "arrendatario")


class BasicVehicleCortexSerializer(serializers.ModelSerializer):
    dataEmplacamento = serializers.DateTimeField(format=None)
    proprietario = ProprietarioBasicRenavamCortexSerializer(read_only=True, required=False)

    class Meta:
        model = VehicleCortex
        fields = ("uuid", "placa", "dataEmplacamento", "chassi", "ufEmplacamento", "municipioPlaca", "anoFabricacao", "anoModelo", 
                  "marcaModelo", "grupoVeiculo", "tipoVeiculo", "especie", "cor", "combustivel", "potencia", "cilindrada", "lotacao", 
                  "capacidadeMaximaCarga", "pesoBrutoTotal", "capacidadeMaximaTracao", "indicadorRemarcacaoChassi", "numeroCaixaCambio", 
                  "quantidadeEixo", "numeroEixoTraseiro", "numeroEixoAuxiliar", "numeroMotor", "tipoMontagem", "restricaoVeiculo1", 
                  "restricaoVeiculo2", "restricaoVeiculo3", "restricaoVeiculo4", "dataLimiteRestricaoTributaria", 
                  "indicadorVeiculoLicenciadoCirculacao", "renavam", "codigoMunicipioEmplacamento", "dataAtualizacaoRouboFurto", 
                  "dataAtualizacaoAlarme", "indicadorVeiculoNacional", "numeroLicencaUsoConfiguracaoVeiculosMotor", "categoria", "codigoCategoria", 
                  "dataEmissaoUltimoCRV", "dataHoraAtualizacaoVeiculo", "numeroProcessoImportacao", "paisTransferenciaVeiculo", 
                  "origemPossuidor", "quaantidadeRestricoesBaseEmplacamento", "registroAduaneiro", "situacaoVeiculo", 
                  "codigoMarcaModelo", "codigoEspecie", "codigoTipoVeiculo", "codigoCor", "restricao", "proprietario")


class VehicleImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField(write_only=True)    
    path_image = serializers.SerializerMethodField('_get_image_path', read_only=True)
    thumbnail = serializers.SerializerMethodField('_get_thumbnail', read_only=True)
    medium = serializers.SerializerMethodField('_get_medium', read_only=True)
    large = serializers.SerializerMethodField('_get_large', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')

    def _get_medium(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.medium.url, request.user.id)

    def _get_large(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.large.url, request.user.id)

    def _get_thumbnail(self, object):
        request = self.context.get('request', None)
        print(request)
        return watermark_helpers.handle(object.file.thumbnail.url, request.user.id)

    def _get_image_path(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.url, request.user.id)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms
    
    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None

    class Meta:
        model = VehicleImage
        fields = ('uuid', 'label', 'file', 'path_image', 'large', 'medium', 'thumbnail', "entity", 'created_at', 'updated_at', 'permissions')

    """ def create(self, validated_data):
        file=validated_data.pop('file')
        label=validated_data.pop('label')
        vehicle=validated_data.pop('vehicle')
        return VehicleImage.objects.create(vehicle=vehicle, label=label, file=file) """
        

class VehicleUpdateSerializer(serializers.ModelSerializer):    
    signal = serializers.CharField(required=False, allow_null=True)
    cpf_owner = serializers.CharField(write_only=True, required=False, allow_null=True)
    cpf_custodian = serializers.CharField(write_only=True, required=False, allow_null=True)
    cpf_renter = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Vehicle
        fields = ("chassi", "signal", "brand", "model", "color", "category", "model_year", "manufactured_year", "cpf_owner", "cpf_custodian", "cpf_renter", "created_at", "updated_at", "permissions")


class VehicleSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):    
    signal = serializers.CharField(required=False, allow_null=True)
    cpf_owner = serializers.CharField(write_only=True, required=False, allow_null=True)
    cpf_custodian = serializers.CharField(write_only=True, required=False, allow_null=True)
    cpf_renter = serializers.CharField(write_only=True, required=False, allow_null=True)
    owner = PersonToVehicleSerializer(read_only=True)
    custodian = PersonToVehicleSerializer(read_only=True)
    renter = PersonToVehicleSerializer(read_only=True)
    images = VehicleImageSerializer(many=True, required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')

    def update(self, instance, validated_data):
        owner = Person.objects.filter(cpf=validated_data["cpf_owner"])
        custodian = Person.objects.filter(cpf=validated_data["cpf_custodian"])
        renter = Person.objects.filter(cpf=validated_data["cpf_renter"])
        instance.owner = owner[0]
        instance.custodian = custodian[0]
        instance.renter = renter[0]
        instance.save()
        return instance

    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None
    
    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Vehicle
        fields = ("uuid", "chassi", "signal", "brand", "model", "color", "category", "model_year",
                  "manufactured_year", "owner", "cpf_owner", "custodian", "cpf_custodian", "renter", "entity", "cpf_renter", "images", "created_at", "updated_at", "permissions")


class BasicVehicleSerializer(serializers.ModelSerializer):    
    signal = serializers.CharField(required=False, allow_null=True)
    owner = PersonToVehicleSerializer(read_only=True)    
    images = VehicleImageSerializer(many=True, required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Vehicle
        fields = ("uuid", "chassi", "signal", "brand", "model", "color", "category", "model_year",
                  "manufactured_year", "owner", "images", "created_at", "updated_at", "permissions")             


class IntermediateVehicleSerializer(serializers.ModelSerializer):    
    signal = serializers.CharField(required=False, allow_null=True)
    owner = PersonToVehicleSerializer(read_only=True)
    custodian = PersonToVehicleSerializer(read_only=True)
    renter = PersonToVehicleSerializer(read_only=True)
    images = VehicleImageSerializer(many=True, required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Vehicle
        fields = ("uuid", "chassi", "signal", "brand", "model", "color", "category", "model_year",
                  "manufactured_year", "owner", "cpf_owner", "custodian", "cpf_custodian", "renter", "cpf_renter", "images", "created_at", "updated_at", "permissions")             

