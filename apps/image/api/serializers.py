from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from apps.image.models import *


class ImageSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    file = Base64ImageField()
    
    class Meta:
        model = Image
        fields = ['uuid', 'file']