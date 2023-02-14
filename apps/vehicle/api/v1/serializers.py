from rest_framework import serializers
from guardian.shortcuts import get_perms
from apps.vehicle.models import PersonRenavamCortex, VehicleCortex
from base.models import Registry
from apps.person.models import Person
from apps.person.api.v1.serializers import NicknameSerializer, FaceSerializer, AddressSerializer, ImageSerializer, TattooSerializer, PhysicalSerializer, DocumentSerializer


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