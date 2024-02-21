from rest_framework import filters, generics, permissions, exceptions
from apps.protect_network import models
from apps.protect_network.api.v1 import serializers
from django.db.models import Q



class IsProtectNetworkManager(permissions.BasePermission):
    def has_permission(self, request, view):
        required_groups = ['profile:protect_network_basic', 'profile:protect_network_advanced', 'profile:protect_network_manager']
        has_permission = request.user.groups.filter(name__in=required_groups).exists()
        if not has_permission:
            raise exceptions.PermissionDenied("Você não tem permissão para acessar esta funcionalidade.")
        return has_permission
    

class SpotListbyTypeView(generics.ListAPIView):
    queryset = models.ProtectNetworkSpot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_spot_type__name']
    permission_classes = [IsProtectNetworkManager]

    def get_queryset(self):
        queryset = models.ProtectNetworkSpot.objects.all()
        spot_type_name = self.request.query_params.get('spot_spot_type_name', None)
        if spot_type_name is not None:
            queryset = queryset.filter(spot_type__name=spot_type_name)
           
        return queryset

class SpotListFilterView(generics.ListAPIView):
    queryset = models.ProtectNetworkSpot.objects.all()
    serializer_class = serializers.SpotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['spot_network__name']
    permission_classes = [IsProtectNetworkManager]

    def get_queryset(self):
        queryset = models.ProtectNetworkSpot.objects.all()
        spot_network_names = self.request.query_params.get('spot_network_name', '')
        spot_network_names_list = spot_network_names.split(',')

        if spot_network_names_list:
            queries = [Q(spot_network__name=spot_network) for spot_network in spot_network_names_list]
            query = queries.pop()
            for item in queries:
                query |= item

            queryset = queryset.filter(query)


        return queryset