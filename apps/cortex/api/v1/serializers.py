import logging
from rest_framework import serializers
from apps.cortex.models import PersonCortex
from apps.person.models import Registry
from apps.person.api.v1.serializers import PersonSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RegistrySerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=False)

    class Meta:
        model = Registry
        fields = ('uuid', 'system_label', 'system_uuid', 'person', 'created_at', 'updated_at')


class PersonCortexSerializer(serializers.ModelSerializer):
    registers = serializers.SerializerMethodField('_get_registry')

    def _get_registry(self, object):
        try:
            registry = Registry.objects.filter(system_uuid=object.uuid)
            if registry:
                serialized = RegistrySerializer(registry, many=True)
                return serialized.data
        except Registry.DoesNotExist:
            logger.warning('Warning while getting registry unavailable')
            return None
        except Exception as e:
            logger.error('Error while getting registry local - {}'.format(e))
            return None

    class Meta:
        model = PersonCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "municipioNaturalidade", "ufNaturalidade", "paisNascimento", "situacaoCadastral", "identificadorResidenteExterior",
                  "paisResidencia", "sexo", "nomeSocial", "naturezaOcupacao", "ocupacaoPrincipal", "anoExercicioOcupacao", "tipoLogradouro",
                  "logradouro", "numeroLogradouro", "complementoLogradouro", "bairro", "cep", "uf", "municipio", "ddd",
                  "telefone", "regiaoFiscal", "anoObito", "indicadorEstrangeiro", "indicadorMoradorEstrangeiro", "dataAtualizacao", "tituloEleitor",
                  "latitudeAproximadaLocal", "longitudeAproximadaLocal", "registers", "created_at", "updated_at")