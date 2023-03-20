from rest_framework import serializers
from guardian.shortcuts import get_perms
from drf_extra_fields.geo_fields import PointField

from apps.address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    place = PointField(required=False)
    permissions = serializers.SerializerMethodField('_get_permissions')
    entity = serializers.SerializerMethodField('_get_entity')
    
    def _get_entity(self, object):
        if object.entity:
            return object.entity.name
        return None

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Address
        fields = ("uuid", "street", "number", "complement", "reference", "neighborhood", "city", "state", "region", "country",
                  "zipcode", "place", "created_at", "updated_at", "entity", "permissions")
