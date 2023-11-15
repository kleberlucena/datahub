from rest_framework import generics
from rest_framework import viewsets, filters
from apps.protect_network import models
from apps.protect_network.api.v1 import serializers
from django.db.models import Q



class SpotListView(generics.ListAPIView):
    queryset = models.Spot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_network__name']

    def get_queryset(self):
        queryset = models.Spot.objects.order_by('-created_at')[:1000]
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
           
        return queryset


class SpotListbyNetworkView(generics.ListAPIView):
    queryset = models.Spot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_network__name']

    def get_queryset(self):
        queryset = models.Spot.objects.all()
        spot_network_name = self.request.query_params.get('spot_network_name', None)
        if spot_network_name is not None:
            queryset = queryset.filter(spot_network__name=spot_network_name)

        queryset = queryset.order_by('-created_at')[:1000]
            
        return queryset
    

class SpotListbyTypeView(generics.ListAPIView):
    queryset = models.Spot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_type__name']

    def get_queryset(self):
        queryset = models.Spot.objects.all()
        spot_type_name = self.request.query_params.get('spot_type_name', None)
        if spot_type_name is not None:
            queryset = queryset.filter(spot_type__name=spot_type_name)

        queryset = queryset.order_by('-created_at')[:1000]
            
        return queryset
    

class SpotListFilterView(generics.ListAPIView):
    queryset = models.Spot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_network__name']

    def get_queryset(self):
        queryset = models.Spot.objects.all()
        spot_network_names = self.request.query_params.get('spot_network_name', '')
        spot_network_names_list = spot_network_names.split(',')

        if spot_network_names_list:
            queries = [Q(spot_network__name=spot_network) for spot_network in spot_network_names_list]
            query = queries.pop()
            for item in queries:
                query |= item

            queryset = queryset.filter(query)

        queryset = queryset.order_by('-created_at')[:1000]

        return queryset