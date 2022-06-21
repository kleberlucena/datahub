from dataclasses import fields
from rest_framework import serializers

from ..models import *


class PersonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Person
        fields = ['uuid', 'created_at', 'updated_at']