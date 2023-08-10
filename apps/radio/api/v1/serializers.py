from rest_framework import serializers

from apps.radio.models import Gps


class GpsSerializer(serializers.ModelSerializer):
    dados = serializers.JSONField(required=False)
    user = serializers.CharField(required=False)
    http_user_agent = serializers.CharField(required=False)
    remote_host = serializers.CharField(required=False)
    ipaddress = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Gps
        fields = ("dados", "user", "http_user_agent", "remote_host", "ipaddress", "created_at")