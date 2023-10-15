from rest_framework import serializers
from django.urls import reverse
from apps.point_interest import models

class SpotSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Spot
        fields = [f.name for f in models.Spot._meta.fields] + ['detail_url']

    def get_detail_url(self, obj):
        return reverse('point_interest:spot_detail_card', kwargs={'pk': obj.pk})



# # serializers.py
# from rest_framework import serializers
# from apps.point_interest import models

# class SpotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Spot
#         fields = '__all__'
