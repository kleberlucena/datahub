from rest_framework import serializers
from apps.cortex.models import PersonCortex
from apps.person.models import Registry
from apps.person.api.v1.serializers import RegistrySerializer


class PersonCortexSerializer(serializers.ModelSerializer):
    registry = serializers.SerializerMethodField('_get_registry')

    def _get_registry(self, object):
        registry = Registry.objects.get(system_uuid=object.uuid)
        print(registry.uuid)
        if registry:
            serialized = RegistrySerializer(registry)
            print(serialized.data)
            return serialized.data

    class Meta:
        model = PersonCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "situacaoCadastral", "identificadorResidenteExterior",
                  "paisResidencia", "sexo", "naturezaOcupacao", "ocupacaoPrincipal", "anoExercicioOcupacao", "tipoLogradouro",
                  "logradouro", "numeroLogradouro", "complementoLogradouro", "bairro", "cep", "uf", "municipio", "ddd",
                  "telefone", "regiaoFiscal", "anoObito", "indicadorEstrangeiro", "dataAtualizacao", "tituloEleitor",
                  "registry", "created_at", "updated_at")