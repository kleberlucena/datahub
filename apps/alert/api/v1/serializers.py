import logging
from rest_framework import serializers
from apps.cortex.models import PersonCortex
from apps.alert.models import AlertCortex, VehicleAlertCortex, PersonAlertCortex
from apps.person.api.v1.serializers import PersonSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VehicleAlertCortexSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=False)

    class Meta:
        model = VehicleAlertCortex
        fields = ('uuid', 'latitudeOcorrencia', 'longitudeOcorrencia', 'latitudePassagem', 'longitudePassagem',
                  'imagem', 'dataPassagem', 'unidadeRegistroBo', 'nomeDeclarante', 'sitOcrId', 'dataOcorrencia',
                  'municipioPlaca',	'municipioLocal', 'telefoneContato', 'ufPlaca', 'numeroBo', 'ufLocal',
                  'localPassagem', 'dddContato', 'sisId', 'historicoOcorrencia', 'idMovimento', 'placa', 'person')


class PersonAlertCortexSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=False)

    class Meta:
        model = PersonAlertCortex
        fields = ('uuid', 'uf',	'cpf', 'nome', 'nomeMae', 'foto', 'lat', 'long', 'estado', 'situacao', 'sistema',
                  'municipio', 'historico', 'dataHora', 'dataNascimento', 'local', 'anobo', 'numeroOcorrencia',
                  'dataHoraOcorrencia', 'municipioOcorrencia', 'ufOcorrencia', 'unidadeOcorrencia', 'sisId', 'sitId', 'person')