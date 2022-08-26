from rest_framework import serializers

from apps.document.models import Document, DocumentImage, DocumentType
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer
from guardian.shortcuts import get_perms


class DocumentImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField()

    class Meta:
        model = DocumentImage
        fields = ['file']


class DocumentTypeSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, document_object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, document_object)
            return perms

    class Meta:
        model = DocumentType
        fields = ['label', 'emitter_department', 'permissions']


class DocumentSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('_get_permissions')
    images = DocumentImageSerializer(many=True)
    # type = DocumentTypeSerializer(many=False, required=False)

    def _get_permissions(self, document_object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, document_object)
            return perms

    class Meta:
        model = Document
        fields = ['uuid', 'number', 'type', 'images', 'permissions']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        type_data = validated_data.pop('type')
        document = Document.objects.create(**validated_data)
        for image_data in images_data:
            DocumentImage.objects.create(document=document, **image_data)
        return document

    def update(self, validated_data):
        images_data = validated_data.pop('images')
        document = Document.objects.update(**validated_data)
        for image_data in images_data:
            DocumentImage.objects.update(document=document, **image_data)
        return document