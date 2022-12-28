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
    registry = serializers.SerializerMethodField('_get_registry')

    def _get_registry(self, object):
        try:
            registry = Registry.objects.get(system_uuid=object.uuid)
            if registry:
                serialized = RegistrySerializer(registry)
                return serialized.data
        except Registry.DoesNotExist:
            raise logger.warning('Warning while getting registry unavailable')
            return {}
        except Exception as e:
            raise logger.error('Error while getting registry local - {}'.format(e))

    class Meta:
        model = PersonCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "situacaoCadastral", "identificadorResidenteExterior",
                  "paisResidencia", "sexo", "naturezaOcupacao", "ocupacaoPrincipal", "anoExercicioOcupacao", "tipoLogradouro",
                  "logradouro", "numeroLogradouro", "complementoLogradouro", "bairro", "cep", "uf", "municipio", "ddd",
                  "telefone", "regiaoFiscal", "anoObito", "indicadorEstrangeiro", "dataAtualizacao", "tituloEleitor",
                  "registry", "created_at", "updated_at")