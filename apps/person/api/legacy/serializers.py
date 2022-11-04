from dataclasses import fields
from numpy import source
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.geo_fields import PointField
from drf_writable_nested import WritableNestedModelSerializer
from guardian.shortcuts import get_perms

from apps.person.models import *
from apps.document.models import Document, DocumentImage
from apps.document.api.serializers import DocumentImageSerializer
from apps.image.models import Image

class DocumentLegacySerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('_get_permissions')
    images = DocumentImageSerializer(many=True, required=False)
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def _get_permissions(self, document_object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, document_object)
            return perms

    class Meta:
        model = Document
        fields = ['uuid', 'number', 'name', 'type', 'images', 'created_at', 'updated_at', 'permissions']

    def create(self, validated_data):
        images_data = None
        type_uuid = None
        try:
            images_data = validated_data.pop('images')
        except Exception as e:
            print(f'Error images; {e}')

        document = Document.objects.create(**validated_data)

        if images_data is not None:
            for image_data in images_data:
                DocumentImage.objects.create(document=document, **image_data)
        return document

    def update(self, validated_data):
        images_data = validated_data.pop('images')
        document = Document.objects.update(**validated_data)
        for image_data in images_data:
            DocumentImage.objects.update(document=document, **image_data)
        return document


class ImageLegacySerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    file = Base64ImageField()
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Image
        fields = ['uuid', 'file', 'label', 'created_at', 'updated_at', 'permissions']


class AddressLegacySerializer(serializers.ModelSerializer):
    place = PointField(required=False)
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Address
        fields = ("uuid", "street", "number", "complement", "neighborhood", "city", "state", "region", "country",
                  "zipcode", "place", 'created_at', 'updated_at', "permissions")


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
    point = PointField(required=False)
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
        fields = ('uuid', 'label', 'point', 'file', 'created_at', 'updated_at', 'permissions')


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


class PersonLegacySerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    nicknames = NicknameLegacySerializer(many=True, required=False)
    faces = FaceLegacySerializer(many=True, required=False)
    addresses = AddressLegacySerializer(many=True, required=False)
    images = ImageLegacySerializer(many=True, required=False)
    tattoos = TattooLegacySerializer(many=True, required=False)
    physicals = PhysicalLegacySerializer(many=True, required=False)
    documents = DocumentLegacySerializer(many=True, required=False)
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
