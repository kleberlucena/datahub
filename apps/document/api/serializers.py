import logging 
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_perms

from base import helpers
from apps.document.models import Document, DocumentImage, DocumentType
from apps.watermark import helpers as watermark_helpers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DocumentImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField(write_only=True)
    path_image = serializers.SerializerMethodField('_get_image_path', read_only=True)
    permissions = serializers.SerializerMethodField('_get_permissions')
    thumbnail = serializers.SerializerMethodField('_get_thumbnail', read_only=True)
    medium = serializers.SerializerMethodField('_get_medium', read_only=True)
    large = serializers.SerializerMethodField('_get_large', read_only=True)

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

    def _get_permissions(self, document_image_object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, document_image_object)
            return perms

    class Meta:
        model = DocumentImage
        fields = ['uuid', 'file', 'path_image', 'large', 'medium', 'thumbnail', 'label', 'created_at', 'updated_at', 'permissions']


class DocumentImageListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('_get_permissions')
    thumbnail = serializers.SerializerMethodField('_get_thumbnail', read_only=True)

    def _get_thumbnail(self, object):
        request = self.context.get('request', None)
        return watermark_helpers.handle(object.file.thumbnail.url, request.user.id)

    def _get_permissions(self, document_image_object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, document_image_object)
            return perms

    class Meta:
        model = DocumentImage
        fields = ['uuid', 'thumbnail', 'label', 'created_at', 'updated_at', 'permissions']


class DocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentType
        fields = ['id', 'label', 'emitter_department']


class DocumentSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('_get_permissions')
    images = DocumentImageSerializer(many=True, required=False)

    def _get_permissions(self, document_object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, document_object)
            return perms

    class Meta:
        model = Document
        fields = ['uuid', 'number', 'name', 'birth_date', 'mother', 'father', 'type', 'images', 'created_at', 'updated_at', 'permissions']

    def create(self, validated_data):
        images_data = None
        type_uuid = None
        try:
            images_data = validated_data.pop('images')
        except Exception as e:
            logger.error('Error while validate images - {}'.format(e))

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


class DocumentListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('_get_permissions')
    images = DocumentImageListSerializer(many=True,  read_only=True)

    def _get_permissions(self, document_object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, document_object)
            return perms

    class Meta:
        model = Document
        fields = ['uuid', 'number', 'name', 'birth_date', 'mother', 'father', 'type', 'images', 'created_at', 'updated_at', 'permissions']