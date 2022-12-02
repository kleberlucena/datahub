from rest_framework import serializers
from apps.cortex.models import PersonCortex


class PersonCortexSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonCortex
        fields = ("numeroCPF", "nomeCompleto", "nomeMae", "dataNascimento", "situacaoCadastral", "identificadorResidenteExterior",
                  "paisResidencia", "sexo", "naturezaOcupacao", "ocupacaoPrincipal", "anoExercicioOcupacao", "tipoLogradouro",
                  "logradouro", "numeroLogradouro", "complementoLogradouro", "bairro", "cep", "uf", "municipio", "ddd",
                  "telefone", "regiaoFiscal", "anoObito", "indicadorEstrangeiro", "dataAtualizacao", "tituloEleitor",
                  "created_at", "updated_at")