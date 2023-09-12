from dataclasses import fields
from numpy import source
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.geo_fields import PointField
from drf_writable_nested import WritableNestedModelSerializer
from guardian.shortcuts import get_perms

from apps.person.models import *
from apps.bnmp.models import RegistryBNMP, PersonBNMP, MandadoPrisao
from apps.cortex.models import RegistryCortex, PersonCortex
from base.models import Registry
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageSerializer
from apps.document.api.serializers import DocumentSerializer
from apps.watermark import helpers as watermark_helpers
from base import helpers
from apps.vehicle.models import RegistryVehicleCortex, PersonRenavamCortex


class PersonToRenavamCortexSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonRenavamCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "municipioNaturalidade",
                  "ufNaturalidade", "paisNascimento", "situacaoCadastral", "identificadorResidenteExterior")


class RegistryVehicleCortexSerializer(serializers.ModelSerializer):
    person_renavam_cortex = PersonToRenavamCortexSerializer(
        read_only=True, required=False, allow_null=True)
    person_uuid = serializers.CharField(source="person")

    class Meta:
        model = RegistryVehicleCortex
        fields = ('uuid', 'created_at', 'updated_at',
                  'person_uuid', 'person_renavam_cortex')


class MandadoBNMPSerializer(serializers.ModelSerializer):

    class Meta:
        model = MandadoPrisao
        fields = ("seqPeca", "dataCriacao", "numeroProcesso", "numeroPeca", "tipoPeca", "status", "nomeServidor", "cargoServidor",
                  "nomeMagistrado", "textoJustificativaCancelamento", "dataConfirmacaoServidor", "dataExpedicao", "dataConclusao",
                  "dataExpiracaoPrisaoMandadoPrisao", "dataVencimentoMandados", "orgaoJudiciario", "dataValidade", "numeroPrazoPrisao",
                  "dataInfracao", "descricaoLocalOcorrencia", "sinteseDecisao", "tempoPenaAno", "tempoPenaMes", "tempoPenaDia",
                  "descricaoCumprimento", "observacao", "regimePrisional", "especiePrisao", "sigilo", "descricaoJustificativa", "nomeEstabelecimentoPrisional",
                  "dataPrisao", "ufCustodia", "municipioCustodia", "linkMandadoPrisao")


class PersonToBNMPSerializer(serializers.ModelSerializer):
    mandados = MandadoBNMPSerializer(
        many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = PersonBNMP
        fields = ('uuid', 'idpessoa', 'nome', 'alcunha', 'nomePai', 'nomeMae', 'dataNascimento', 'sexo',
                  'naturalidade', 'statusPessoa', 'indiceAssertividade', 'tipoBuscaCPF', 'mandados', 'created_at', 'created_at')


class PersonToCortexSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "municipioNaturalidade", "ufNaturalidade", "paisNascimento", "situacaoCadastral", "identificadorResidenteExterior",
                  "paisResidencia", "sexo", "nomeSocial", "naturezaOcupacao", "ocupacaoPrincipal", "anoExercicioOcupacao", "tipoLogradouro",
                  "logradouro", "numeroLogradouro", "complementoLogradouro", "bairro", "cep", "uf", "municipio", "ddd",
                  "telefone", "regiaoFiscal", "anoObito", "indicadorEstrangeiro", "indicadorMoradorEstrangeiro", "dataAtualizacao", "tituloEleitor",
                  "latitudeAproximadaLocal", "longitudeAproximadaLocal", "created_at", "updated_at")


class RegistryCortexSerializer(serializers.ModelSerializer):
    person_cortex = PersonToCortexSerializer(
        read_only=True, required=False, allow_null=True)
    person_uuid = serializers.CharField(source="person")

    class Meta:
        model = RegistryCortex
        fields = ('uuid', 'created_at', 'updated_at',
                  'person_uuid', 'person_cortex')


class RegistryBNMPSerializer(serializers.ModelSerializer):
    person_bnmp = PersonToBNMPSerializer(
        read_only=True, required=False, allow_null=True)
    person_uuid = serializers.CharField(source="person")

    class Meta:
        model = RegistryBNMP
        fields = ('uuid', 'created_at', 'updated_at',
                  'person_uuid', 'person_bnmp')


class RegistryPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registry
        fields = ('uuid', 'created_at', 'updated_at', 'person')


class RegistryPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Registry: RegistryPersonSerializer,
        RegistryCortex: RegistryCortexSerializer,
        RegistryBNMP: RegistryBNMPSerializer,
    }


class FaceSerializer(serializers.ModelSerializer):
    file = Base64ImageField(write_only=True)
    path_image = serializers.SerializerMethodField(
        '_get_image_path', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')
    thumbnail = serializers.SerializerMethodField(
        '_get_thumbnail', read_only=True)
    medium = serializers.SerializerMethodField('_get_medium', read_only=True)
    large = serializers.SerializerMethodField('_get_large', read_only=True)
    entity = serializers.SerializerMethodField('_get_entity')

    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None

    def _get_medium(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.medium.url, request.user.id)

    def _get_large(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.large.url, request.user.id)

    def _get_thumbnail(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.thumbnail.url, request.user.id)

    def _get_image_path(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.url, request.user.id)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Face
        fields = ('uuid', 'file', 'path_image', 'large', 'medium',
                  'thumbnail', 'created_at', 'updated_at', 'entity', 'permissions')


class NicknameSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')

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
        model = Nickname
        fields = ('uuid', 'label', 'created_at',
                  'updated_at', 'entity', 'permissions')


class TattooSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    point = PointField(required=False)
    file = Base64ImageField(write_only=True)
    path_image = serializers.SerializerMethodField(
        '_get_image_path', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')
    thumbnail = serializers.SerializerMethodField(
        '_get_thumbnail', read_only=True)
    medium = serializers.SerializerMethodField('_get_medium', read_only=True)
    large = serializers.SerializerMethodField('_get_large', read_only=True)
    entity = serializers.SerializerMethodField('_get_entity')

    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None

    def _get_medium(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.medium.url, request.user.id)

    def _get_large(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.large.url, request.user.id)

    def _get_thumbnail(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.thumbnail.url, request.user.id)

    def _get_image_path(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.url, request.user.id)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Tattoo
        fields = ('uuid', 'label', 'point', 'file', 'path_image', 'large', 'medium',
                  'thumbnail', 'created_at', 'updated_at', 'entity', 'permissions')


class PhysicalSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    value = serializers.CharField()
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')

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
        model = Physical
        fields = ('uuid', 'label', 'value', 'created_at',
                  'updated_at', 'entity', 'permissions')


class PersonSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    nicknames = NicknameSerializer(many=True, required=False)
    faces = FaceSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    tattoos = TattooSerializer(many=True, required=False)
    physicals = PhysicalSerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)
    registers = RegistryPolymorphicSerializer(
        many=True, read_only=True, required=False, allow_null=True)
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')

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
        model = Person
        fields = (
            'uuid', 'nicknames', 'addresses', 'images', 'faces', 'documents', 'tattoos', 'physicals',
            'created_at', 'updated_at', 'entity', 'registers', 'permissions')