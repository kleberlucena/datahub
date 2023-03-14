from rest_framework import serializers
from guardian.shortcuts import get_perms

from base.models import Suggestion 


class SuggestionSerializer(serializers.ModelSerializer):
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
        model = Suggestion
        fields = ('uuid', 'label', 'content', 'created_at', 'updated_at', 'entity', 'permissions')