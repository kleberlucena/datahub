from dataclasses import fields
from numpy import source
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.geo_fields import PointField
from drf_writable_nested import WritableNestedModelSerializer
from guardian.shortcuts import get_perms

from apps.person.models import *
from base import helpers
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageSerializer
from apps.document.api.serializers import DocumentSerializer

class FaceSerializer(serializers.ModelSerializer):
    file = Base64ImageField(write_only=True)
    path_image = serializers.SerializerMethodField('_get_image_path', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_image_path(self, object):
        request = self.context.get('request', None)
        if request:
            img_name = object.file.name
            old_url = object.file.storage.url(img_name)
            return helpers.get_watermark_url(old_url, request.user.username)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Face
        fields = ('uuid', 'file', 'path_image', 'created_at', 'updated_at', 'permissions')


class NicknameSerializer(serializers.ModelSerializer):
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


class TattooSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    point = PointField(required=False)
    file = Base64ImageField(write_only=True)
    path_image = serializers.SerializerMethodField('_get_image_path', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_image_path(self, object):
        request = self.context.get('request', None)
        if request:
            img_name = object.file.name
            old_url = object.file.storage.url(img_name)
            return helpers.get_watermark_url(old_url, request.user.username)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Tattoo
        fields = ('uuid', 'label', 'point', 'file', 'path_image', 'created_at', 'updated_at', 'permissions')

    def create(self, validated_data):
        file=validated_data.pop('file')
        label=validated_data.pop('label')
        point=validated_data.pop('point')
        person=validated_data.pop('person')
        return Tattoo.objects.create(person=person, label=label, point=point, file=file)


class PhysicalSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    value = serializers.CharField()
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Physical
        fields = ('uuid', 'label', 'value', 'created_at', 'updated_at', 'permissions')


class PersonSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    nicknames = NicknameSerializer(many=True, required=False)
    faces = FaceSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    tattoos = TattooSerializer(many=True, required=False)
    physicals = PhysicalSerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)
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
