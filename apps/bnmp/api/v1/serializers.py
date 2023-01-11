from rest_framework import serializers

from apps.bnmp.models import PersonBNMP
from apps.person.api.v1.serializers import PersonSerializer


class PersonBNMPSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=False, read_only=True)

    class Meta:
        model = PersonBNMP
        fields = ('uuid', 'idpessoa', 'nome', 'alcunha', 'nomePai', 'nomeMae', 'dataNascimento', 'sexo', 
        'naturalidade', 'statusPessoa', 'indiceAssertividade', 'tipoBuscaCPF', 'person', 'created_at')