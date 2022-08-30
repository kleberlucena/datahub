from rest_framework import serializers
from guardian.shortcuts import get_perms
from drf_extra_fields.geo_fields import PointField

from apps.address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    place = PointField()
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Address
        fields = ("uuid", "street", "number", "complement", "neighborhood", "city", "state", "region", "country", "zipcode", "place", "permissions")
