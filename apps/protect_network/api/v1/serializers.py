from rest_framework import serializers
from django.urls import reverse
from apps.protect_network import models


class SpotSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    spot = serializers.SerializerMethodField('get_spot')

    class Meta:
        model = models.ProtectNetworkSpot
        fields = ['spot', 'tags', 'update_score', 'next_update', 'is_headquarters', 'cnpj', 
                  'parent_company', 'spot_network', 'qpp' ] + ['detail_url']

    def get_spot(self, obj):
        resposta = {"name": obj.spot.name, "latitude": obj.spot.latitude, "longitude": obj.spot.longitude}
        return resposta

    def get_detail_url(self, obj):
        return reverse('protect_network:spot_detail_card', kwargs={'pk': obj.pk})
