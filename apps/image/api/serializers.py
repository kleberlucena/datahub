from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from guardian.shortcuts import get_perms

from apps.image.models import *


class ImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField()
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms
    
    class Meta:
        model = Image
        fields = ['uuid', 'file', 'created_at', 'updated_at', 'permissions']