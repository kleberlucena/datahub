from dataclasses import fields
from rest_framework import serializers

from apps.image.models import *


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ['uuid', 'created_at', 'updated_at']