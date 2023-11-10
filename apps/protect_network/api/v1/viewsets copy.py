from rest_framework import generics
from rest_framework import viewsets, filters
from apps.protect_network import models
from apps.protect_network.api.v1 import serializers
from django.db.models import Q

class SpotListView(generics.ListAPIView):
    queryset = models.Spot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_type__name']  # Mantemos a filtragem pelo nome do spot_type

    def get_queryset(self):
        queryset = models.Spot.objects.order_by('-created_at')[:1000]
        
        # Filtragem baseada no nome do ponto de interesse
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
           
        return queryset
    
class SpotListbyTypeView(generics.ListAPIView):
    queryset = models.Spot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_type__name']  # Mantemos a filtragem pelo nome do spot_type

    def get_queryset(self):
        queryset = models.Spot.objects.all()
        # Filtragem baseada no nome do spot_type
        spot_type_name = self.request.query_params.get('spot_type_name', None)
        if spot_type_name is not None:
            queryset = queryset.filter(spot_type__name=spot_type_name)

        
        queryset = queryset.order_by('-created_at')[:1000]
            
        return queryset
    

class SpotListFilterView(generics.ListAPIView):
    queryset = models.Spot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_type__name']

    def get_queryset(self):
        queryset = models.Spot.objects.all()
        spot_type_names = self.request.query_params.get('spot_type_name', '')

        # Divida a string em uma lista de tipos
        spot_type_names_list = spot_type_names.split(',')

        if spot_type_names_list:
            queries = [Q(spot_type__name=spot_type) for spot_type in spot_type_names_list]
            query = queries.pop()
            for item in queries:
                query |= item

            queryset = queryset.filter(query)

        queryset = queryset.order_by('-created_at')[:1000]

        return queryset

#     # views.py
# from rest_framework import generics
# from rest_framework import viewsets, filters
# from apps.protect_network import models
# from apps.protect_network.api.v1 import serializers


# class SpotListView(generics.ListAPIView):
#     queryset = models.Spot.objects.all()
#     serializer_class = serializers.SpotSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['spot_type__name']

#     def get_queryset(self):
#         queryset = models.Spot.objects.order_by('-created_at')[:1000]
#         # Suponhamos que você quer filtrar com um parâmetro chamado 'name'
#         name = self.request.query_params.get('name', None)
#         if name is not None:
#             queryset = queryset.filter(name=name)
#         return queryset