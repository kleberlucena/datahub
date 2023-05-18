import logging
from guardian.shortcuts import get_perms
from rest_framework import serializers
from apps.cortex.models import PersonCortex
from base.models import Registry
from apps.person.models import Person
from apps.person.api.v1.serializers import NicknameSerializer, FaceSerializer, AddressSerializer, ImageSerializer, TattooSerializer, PhysicalSerializer, DocumentSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class PersonToSerializer(serializers.ModelSerializer):
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


class RegistrySerializer(serializers.ModelSerializer):
    person = PersonToSerializer(read_only=True)
    # person_cortex = PersonToCortexSerializer(read_only=True, required=False, allow_null=True)

    class Meta:
        model = Registry
        fields =  ('uuid', 'created_at', 'updated_at', 'person')

        
class BasicPersonCortexSerializer(serializers.ModelSerializer):
    dataAtualizacao = serializers.DateTimeField(format=None)

    class Meta:
        model = PersonCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "sexo", "nomeSocial", "anoObito", "dataAtualizacao", "created_at", "updated_at")


class PersonCortexSerializer(serializers.ModelSerializer):
    dataAtualizacao = serializers.DateTimeField(format=None)
    registers = RegistrySerializer(many=True, read_only=True)

    class Meta:
        model = PersonCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "municipioNaturalidade", "ufNaturalidade", "paisNascimento", "situacaoCadastral", "identificadorResidenteExterior",
                  "paisResidencia", "sexo", "nomeSocial", "naturezaOcupacao", "ocupacaoPrincipal", "anoExercicioOcupacao", "tipoLogradouro",
                  "logradouro", "numeroLogradouro", "complementoLogradouro", "bairro", "cep", "uf", "municipio", "ddd",
                  "telefone", "regiaoFiscal", "anoObito", "indicadorEstrangeiro", "indicadorMoradorEstrangeiro", "dataAtualizacao", "tituloEleitor",
                  "latitudeAproximadaLocal", "longitudeAproximadaLocal", "indiceNacionalPessoas", "registers", "created_at", "updated_at")
