from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from guardian.shortcuts import get_perms

from base import helpers
from apps.image.models import *



class ImageSerializer(serializers.ModelSerializer):
    '''
    Serializador de imagens de Pessoas e genéricas
    '''
    file = Base64ImageField(write_only=True)
    path_image = serializers.SerializerMethodField('_get_image_path', read_only=True)
    label = serializers.CharField(required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')
    thumbnail = serializers.SerializerMethodField('_get_thumbnail', read_only=True)
    medium = serializers.SerializerMethodField('_get_medium', read_only=True)
    large = serializers.SerializerMethodField('_get_large', read_only=True)

    def _get_medium(self, object):
        return helpers.get_image_variation(self, object, 'medium')

    def _get_large(self, object):
        return helpers.get_image_variation(self, object, 'large')

    def _get_thumbnail(self, object):
        return helpers.get_image_variation(self, object, 'thumbnail')

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
        model = Image
        fields = ['uuid', 'file', 'path_image', 'large', 'medium', 'thumbnail', 'label', 'created_at', 'updated_at', 'permissions']


class ImageListSerializer(serializers.ModelSerializer):
    '''
    Serializador de lista de imagens de Pessoas e genéricas
    '''
    label = serializers.CharField(required=False)
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
        model = Image
        fields = ['uuid', 'thumbnail', 'label', 'created_at', 'updated_at', 'permissions']