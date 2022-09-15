from dataclasses import fields
from numpy import source
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer
from guardian.shortcuts import get_perms

from apps.person.models import *
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageSerializer
from apps.document.api.serializers import DocumentSerializer


class FaceLegacySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    file = Base64ImageField()
    permissions = serializers.SerializerMethodField('_get_permissions')
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Face
        fields = ('uuid', 'file', 'created_at', 'updated_at', 'permissions')
        extra_fields = ('created_at', 'updated_at')

    def create(self, validated_data):

        created_at = validated_data.pop('created_at')
        updated_at = validated_data.pop('updated_at')
        print(created_at)
        instance = Face.objects.create(**validated_data, created_at=created_at, updated_at=updated_at)
        return instance


class NicknameLegacySerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    permissions = serializers.SerializerMethodField('_get_permissions')
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Nickname
        fields = ('uuid', 'label', 'created_at', 'updated_at', 'permissions')


class TattooLegacySerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    file = Base64ImageField()
    permissions = serializers.SerializerMethodField('_get_permissions')
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Tattoo
        fields = ('uuid', 'label', 'file', 'created_at', 'updated_at', 'permissions')

    def create(self, validated_data):
        file=validated_data.pop('file')
        label=validated_data.pop('label')
        person=validated_data.pop('person')
        created_at = validated_data.pop('created_at')
        updated_at = validated_data.pop('updated_at')
        return Tattoo.objects.create(person=person, label=label, file=file, created_at=created_at, updated_at=updated_at)


class PhysicalLegacySerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    value = serializers.CharField()
    permissions = serializers.SerializerMethodField('_get_permissions')
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Physical
        fields = ('uuid', 'label', 'value', 'created_at', 'updated_at', 'permissions')

    # def create(self, validated_data):
    #     created_at = validated_data.pop('created_at')
    #     updated_at = validated_data.pop('updated_at')
    #     instance = Physical.objects.create(**validated_data)
    #     instance.save(created_at=created_at, updated_at=updated_at)
    #     return instance


class PersonLegacySerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    nicknames = NicknameLegacySerializer(many=True, required=False)
    faces = FaceLegacySerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    tattoos = TattooLegacySerializer(many=True, required=False)
    physicals = PhysicalLegacySerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

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

    # def create(self, validated_data):
    #     created_at = validated_data.pop('created_at')
    #     updated_at = validated_data.pop('updated_at')
    #     instance = Person.objects.create(**validated_data, created_at=created_at, updated_at=updated_at)
    #     instance.update(created_at=created_at, updated_at=updated_at)
    #     return instance
