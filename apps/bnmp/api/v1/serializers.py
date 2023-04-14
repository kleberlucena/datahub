from rest_framework import serializers
from guardian.shortcuts import get_perms

from base.models import Registry
from apps.bnmp.models import PersonBNMP, MandadoPrisao
from apps.person.models import Person
from apps.person.api.v1 import serializers as person_serializes


class PersonToBNMPSerializer(serializers.ModelSerializer):
    nicknames = person_serializes.NicknameSerializer(many=True, required=False)
    faces = person_serializes.FaceSerializer(many=True, required=False)
    addresses = person_serializes.AddressSerializer(many=True, required=False)
    images = person_serializes.ImageSerializer(many=True, required=False)
    tattoos = person_serializes.TattooSerializer(many=True, required=False)
    physicals = person_serializes.PhysicalSerializer(many=True, required=False)
    documents = person_serializes.DocumentSerializer(many=True, required=False)
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
        

class RegistryBNMPSerializer(serializers.ModelSerializer):
    person = PersonToBNMPSerializer(read_only=True, required=False)
    # person_cortex = PersonToCortexSerializer(read_only=True, required=False, allow_null=True)

    class Meta:
        model = Registry
        fields =  ('uuid', 'created_at', 'updated_at', 'person')


class MandadoBNMPSerializer(serializers.ModelSerializer):

     class Meta:
        model = MandadoPrisao
        fields = ("seqPeca", "dataCriacao", "numeroProcesso", "numeroPeca", "tipoPeca", "status", "nomeServidor", "cargoServidor",
                "nomeMagistrado", "textoJustificativaCancelamento", "dataConfirmacaoServidor", "dataExpedicao", "dataConclusao",
                "dataExpiracaoPrisaoMandadoPrisao", "dataVencimentoMandados", "orgaoJudiciario", "dataValidade", "numeroPrazoPrisao",
                "dataInfracao", "descricaoLocalOcorrencia", "sinteseDecisao", "tempoPenaAno", "tempoPenaMes", "tempoPenaDia",
                "descricaoCumprimento", "observacao", "regimePrisional", "especiePrisao", "sigilo", "descricaoJustificativa", "nomeEstabelecimentoPrisional",
                "dataPrisao", "ufCustodia", "municipioCustodia", "linkMandadoPrisao", "tipificacaoPenal")


class PersonBNMPSerializer(serializers.ModelSerializer):
    registers = RegistryBNMPSerializer(many=True, read_only=True, required=False, allow_null=True)
    mandados = MandadoBNMPSerializer(many=True, read_only=True, required=False, allow_null=True)

    class Meta:
        model = PersonBNMP
        fields = ('uuid', 'idpessoa', 'nome', 'alcunha', 'nomePai', 'nomeMae', 'dataNascimento', 'sexo', 
        'naturalidade', 'statusPessoa', 'indiceAssertividade', 'tipoBuscaCPF', 'mandados', 'registers', 'created_at', 'created_at')