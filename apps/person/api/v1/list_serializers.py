from dataclasses import fields
from numpy import source
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.geo_fields import PointField
from guardian.shortcuts import get_perms

from apps.person.models import *
from base import helpers
from .serializers import RegistryCortexSerializer, PhysicalSerializer
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageListSerializer
from apps.document.api.serializers import DocumentListSerializer


class FaceListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField('_get_thumbnail', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_thumbnail(self, object):
        return helpers.get_image_variation(self, object, 'thumbnail')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Face
        fields = ('uuid', 'thumbnail', 'created_at', 'updated_at', 'permissions')


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
    thumbnail = serializers.SerializerMethodField('_get_thumbnail', read_only=True)

    def _get_thumbnail(self, object):
        return helpers.get_image_variation(self, object, 'thumbnail')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Tattoo
        fields = ('uuid', 'label', 'point', 'thumbnail', 'created_at', 'updated_at', 'permissions')


class PersonListSerializer(serializers.ModelSerializer):
    nicknames = NicknameListSerializer(many=True, required=False)
    faces = FaceListSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    images = ImageListSerializer(many=True, required=False)
    tattoos = TattooListSerializer(many=True, required=False)
    physicals = PhysicalSerializer(many=True, required=False)
    documents = DocumentListSerializer(many=True, required=False)
    registers = RegistryCortexSerializer(many=True, read_only=True, required=False, allow_null=True)
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
            'created_at', 'updated_at', 'registers', 'permissions')
