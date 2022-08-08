from rest_framework import serializers

from apps.document.models import Document, DocumentImage
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer


class DocumentImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField()

    class Meta:
        model = DocumentImage
        fields = ['file']


class DocumentSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    images = DocumentImageSerializer(many=True)

    class Meta:
        model = Document
        fields = ['uuid', 'number', 'label', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
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