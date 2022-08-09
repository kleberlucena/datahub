from dataclasses import fields
from numpy import source
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer

from apps.person.models import *
from apps.address.api.serializers import AddressSerializer, AddressListSerializer
from apps.image.api.serializers import ImageSerializer
from apps.document.api.serializers import DocumentSerializer


class FaceSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    file = Base64ImageField()

    class Meta:
        model = Face
        fields = ('uuid', 'file',)

    def create(self, validated_data):
        file=validated_data.pop('file')
        uuid=validated_data.pop('uuid')
        person=validated_data.pop('person')
        return Face.objects.create(uuid=uuid, person=person, file=file)


class NicknameSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    nickname = serializers.CharField()

    class Meta:
        model = Nickname
        fields = ('uuid', 'nickname',)


class TatooSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    label = serializers.CharField()
    file = Base64ImageField()

    class Meta:
        model = Tatoo
        fields = ('uuid', 'label', 'file')

    def create(self, validated_data):
        file=validated_data.pop('file')
        label=validated_data.pop('label')
        uuid=validated_data.pop('uuid')
        person=validated_data.pop('person')
        return Tatoo.objects.create(uuid=uuid, person=person, label=label, file=file)



class PhysicalSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    label = serializers.CharField()
    value = serializers.CharField()

    class Meta:
        model = Physical
        fields = ('uuid', 'label', 'value')


class PersonSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    nicknames = NicknameSerializer(many=True)
    faces = FaceSerializer(many=True)
    addresses = AddressSerializer(many=True)
    images = ImageSerializer(many=True)
    tatoos = TatooSerializer(many=True)
    physicals = PhysicalSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Person
        fields = (
            'uuid', 'nicknames', 'addresses', 'images', 'faces', 'documents', 'tatoos', 'physicals')


class PersonListSerializer(serializers.ModelSerializer):
    nicknames = NicknameSerializer(many=True)
    faces = FaceSerializer(many=True)
    addresses = AddressSerializer(many=True)
    images = ImageSerializer(many=True)
    tatoos = TatooSerializer(many=True)
    physicals = PhysicalSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Person
        fields = (
            'uuid', 'nicknames', 'addresses', 'images', 'faces', 'documents', 'tatoos', 'physicals')
        
    