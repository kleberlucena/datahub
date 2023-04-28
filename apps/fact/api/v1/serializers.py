from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.geo_fields import PointField
from drf_writable_nested import WritableNestedModelSerializer
from guardian.shortcuts import get_perms

from apps.watermark import helpers as watermark_helpers
from apps.fact.models import Fact, FactImage, FactType
from apps.address.api.serializers import AddressSerializer
from apps.person.models import Person
from apps.person.api.v1 import serializers as person_serializer


class FactTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FactType
        fields = ['id', 'uuid', 'title', 'description']


class FactPersonSerializer(serializers.ModelSerializer):
    nicknames = person_serializer.NicknameSerializer(many=True, required=False)
    faces = person_serializer.FaceMediumSerializer(many=True, required=False)
    addresses = AddressSerializer(many=True, required=False)
    documents = person_serializer.DocumentSerializer(many=True, required=False)
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
            'uuid', 'nicknames', 'addresses', 'faces', 'documents', 'created_at', 'updated_at', 'permissions', 'entity')


class FactImageSerializer(serializers.ModelSerializer):
    label = serializers.CharField()
    file = Base64ImageField(write_only=True)
    path_image = serializers.SerializerMethodField('_get_image_path', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')
    thumbnail = serializers.SerializerMethodField('_get_thumbnail', read_only=True)
    medium = serializers.SerializerMethodField('_get_medium', read_only=True)
    large = serializers.SerializerMethodField('_get_large', read_only=True)
    entity = serializers.SerializerMethodField('_get_entity')

    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None

    def _get_medium(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.medium.url, request.user.id)

    def _get_large(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.large.url, request.user.id)

    def _get_thumbnail(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.thumbnail.url, request.user.id)

    def _get_image_path(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.url, request.user.id)

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = FactImage
        fields = ('uuid', 'label', 'file', 'path_image', 'large', 'medium', 'thumbnail', 'created_at', 'updated_at', 'entity', 'permissions')


class FactSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    victims = FactPersonSerializer(read_only=True, many=True, required=False)
    suspects = FactPersonSerializer(read_only=True, many=True, required=False)
    witnesses = FactPersonSerializer(read_only=True, many=True, required=False)
    addresses = AddressSerializer(read_only=True, many=True, required=False)
    images = FactImageSerializer(many=True, required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')
    fact_type = serializers.SerializerMethodField('_get_fact_type')
    
    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms
        
    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None
    
    def _get_fact_type(self, object):
        if object.fact_type:
            return object.fact_type.title
        return None

    class Meta:
        model = Fact
        fields = (
            'uuid', 'title', 'description', 'fact_type', 'start_time', 'end_time', 'victims', 'suspects', 'witnesses', 'addresses', 'images', 
            'created_at', 'updated_at', 'permissions', 'entity')