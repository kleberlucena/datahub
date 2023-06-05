from rest_framework import serializers

from ...models import CharacteristicType, PersonalCharacteristic, VTR, PoliceTeam, PoliceReport, InvolvedPerson


class CharacteristicTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CharacteristicType
        fields = ['id', 'label']


class PersonalCharacteristicSerializer(serializers.ModelSerializer):
    characteristic_type = CharacteristicTypeSerializer()

    class Meta:
        model = PersonalCharacteristic
        fields = ['id', 'description', 'file', 'characteristic_type']


class VTRSerializer(serializers.ModelSerializer):

    class Meta:
        model = VTR
        fields = '__all__'


class PoliceTeamSerializer(serializers.ModelSerializer):
    vtr = VTRSerializer()
    entity = serializers.SerializerMethodField('_get_entity')

    def _get_entity(self, object):
        if object.unit:
            return object.unit.name
        return None

    class Meta:
        model = PoliceTeam
        fields = '__all__'


class PoliceReportSerializer(serializers.ModelSerializer):
    police_team = PoliceTeamSerializer()
    entity = serializers.SerializerMethodField('_get_entity')

    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None

    class Meta:
        model = PoliceReport
        fields = '__all__'


class InvolvedPersonSerializer(serializers.ModelSerializer):
    personal_characteristics = PersonalCharacteristicSerializer(
        many=True, required=False, allow_null=True)

    class Meta:
        model = InvolvedPerson
        fields = ['id', 'uuid', 'name', 'mother', 'father', 'birth_date', 'phone',
                  'profession', 'personal_characteristics', 'addresses', 'images', 'documents']
