from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from guardian.shortcuts import get_perms

from apps.address.models import Address


class AddressSerializer(geo_serializers.GeoFeatureModelSerializer):
    permissions = serializers.SerializerMethodField('_get_permissions')

    def _get_permissions(self, object):
        request = self.context.get('request', None)
        if request:
            perms = get_perms(request.user, object)
            return perms

    class Meta:
        model = Address
        fields = ("uuid", "street", "number", "complement", "neighborhood", "city", "state", "region", "country", "zipcode", "permissions")
        geo_field = "place"
        

class AddressListSerializer(geo_serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Address
        fields = ("uuid", "street", "number", "complement", "neighborhood", "city", "state", "region", "country", "zipcode")
        geo_field = "place"


# class VisitSerializer(geo_serializers.GeoFeatureModelSerializer):
#     class Meta:
#         model = Visit
#         fields = ["id", "label", "datetime", "updated_by", "updated_at", "created_by", "created_at"]
#         geo_field = "place"
