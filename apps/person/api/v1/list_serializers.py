from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.geo_fields import PointField
from guardian.shortcuts import get_perms

from apps.person.models import *
from base import helpers
from base.models import Registry
from .serializers import RegistryPolymorphicSerializer, PhysicalSerializer
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageListSerializer
from apps.document.api.serializers import DocumentListSerializer
from apps.watermark import helpers as watermark_helpers


class FaceListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(
        '_get_thumbnail', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_thumbnail(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.thumbnail.url, request.user.id)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Face
        fields = ('uuid', 'thumbnail', 'created_at',
                  'updated_at', 'permissions')


class NicknameListSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Nickname
        fields = ('uuid', 'label', 'created_at', 'updated_at', 'permissions')


class TattooListSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    point = PointField(required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')
    thumbnail = serializers.SerializerMethodField(
        '_get_thumbnail', read_only=True)

    def _get_thumbnail(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.thumbnail.url, request.user.id)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Tattoo
        fields = ('uuid', 'label', 'point', 'thumbnail',
                  'created_at', 'updated_at', 'permissions')


class RegistryPersonSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('_get_type')

    def _get_type(self, object):
        if object.polymorphic_ctype:
            return object.polymorphic_ctype.model
        return None

    class Meta:
        model = Registry
        fields = ('uuid', 'created_at', 'updated_at',
                  'polymorphic_ctype_id', 'type')


class PersonListSerializer(serializers.ModelSerializer):
    nicknames = NicknameListSerializer(many=True, required=False)
    faces = FaceListSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    images = ImageListSerializer(many=True, required=False)
    tattoos = TattooListSerializer(many=True, required=False)
    physicals = PhysicalSerializer(many=True, required=False)
    documents = DocumentListSerializer(many=True, required=False)
    # registers = RegistryPolymorphicSerializer(
    #     many=True, read_only=True, required=False, allow_null=True)
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None

    class Meta:
        model = Person
        fields = (
            'uuid', 'nicknames', 'addresses', 'images', 'faces', 'documents', 'tattoos', 'physicals',
            'created_at', 'updated_at', 'entity', 'registers', 'permissions')


class IntermediatePersonListSerializer(serializers.ModelSerializer):
    nicknames = NicknameListSerializer(many=True, required=False)
    faces = FaceListSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    images = ImageListSerializer(many=True, required=False)
    tattoos = TattooListSerializer(many=True, required=False)
    physicals = PhysicalSerializer(many=True, required=False)
    documents = DocumentListSerializer(many=True, required=False)
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


class BasicPersonListSerializer(serializers.ModelSerializer):
    nicknames = NicknameListSerializer(many=True, required=False)
    faces = FaceListSerializer(many=True, required=False)
    images = ImageListSerializer(many=True, required=False)
    documents = DocumentListSerializer(many=True, required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Person
        fields = (
            'uuid', 'nicknames', 'images', 'faces', 'documents',
            'created_at', 'updated_at', 'permissions')
