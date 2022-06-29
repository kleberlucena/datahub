from dataclasses import fields
from numpy import source
from rest_framework import serializers

from apps.image.models import *


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ('uuid', 'file')
        