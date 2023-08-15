from rest_framework import serializers
from django.contrib.gis.geos import Point, GEOSGeometry

from apps.radio.models import Gps


class GpsSerializer(serializers.ModelSerializer):
    """ location = serializers.DictField(child=serializers.FloatField())
    accuracy = serializers.IntegerField()
    emergency = serializers.BooleanField()
    timestamp = serializers.DateTimeField()
    id = serializers.CharField(max_length=20)
    timestampReceived = serializers.DateTimeField() """

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        gps_instance = Gps.objects.create(**validated_data)
        gps_instance.location = Point(
            location_data['coordinates'][0], location_data['coordinates'][1], srid=4326)
        gps_instance.save()
        return gps_instance

    class Meta:
        model = Gps
        fields = ("location", "accuracy", "emergency", "timestamp",
                  "id", "timestampReceived", "created_at")
        geo_field = "location"
