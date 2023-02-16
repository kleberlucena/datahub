from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics, filters, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from guardian.shortcuts import assign_perm
import logging

from apps.vehicle.api.v1.serializers import VehicleCortexSerializer, IntermediateVehicleCortexSerializer, BasicVehicleCortexSerializer, VehicleSerializer
from apps.vehicle.models import VehicleCortex, Vehicle
from apps.vehicle import helpers

signal = openapi.Parameter('signal', openapi.IN_QUERY, description="param signal do veículo", type=openapi.TYPE_STRING)
chassi = openapi.Parameter('chassi', openapi.IN_QUERY, description="param chassi do veículo", type=openapi.TYPE_STRING)
my = openapi.Parameter('my', openapi.IN_QUERY, description="param my pesquisa cadastros do usuário logado", type=openapi.TYPE_BOOLEAN)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VehicleByPlacaViewSet(generics.GenericAPIView):
    serializer_class = VehicleCortexSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_intermediate').exists():
            return IntermediateVehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_basic').exists():
            return BasicVehicleCortexSerializer
        raise Http404

    def get_queryset(self):
        """
        Optionally restricts the returned person_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_person to a given document,
        by filtering against a `document_name` or a `document_number` query parameter in the URL.
        """
        queryset = VehicleCortex.objects.all() 
        return queryset

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, placa):
        username = request.user.username
        vehicle_cortex = None

        try:
            helpers.process_cortex_consult(username=username, placa=placa.upper())
            
        except Exception as e:
            logger.error('Error while process_cortex_consult vehicle_cortex - {}'.format(e))
        try:
            vehicle_cortex = get_object_or_404(VehicleCortex, placa=placa.upper())
        except Exception as e:
            logger.error('Error while get vehicle_cortex - {}'.format(e))
            return Response(status=400)
        try:
            serializer = self.get_serializer(vehicle_cortex)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=403)
        

class AddVehicleListView(generics.ListCreateAPIView):
    # permission_classes = [DjangoModelPermissions]
    serializer_class = VehicleSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    queryset = Vehicle.objects.all()

    """ def get_serializer_class(self):
        if self.request.method in ['POST']:
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_advanced').exists():
            return list_serializers.PersonListSerializer
        elif self.request.user.groups.filter(name='profile:person_intermediate').exists():
            return list_serializers.IntermediatePersonListSerializer
        elif self.request.user.groups.filter(name='profile:person_basic').exists():
            return list_serializers.BasicPersonListSerializer
        raise Http404   """

    @action(detail=True, methods=['GET'])
    def list(self, request, *args, **kwargs):
        #self.permission_classes = [DjangoModelPermissions]
        queryset = self.filter_queryset(self.get_queryset())
        # queryset = get_objects_for_user(self.request.user, 'person.view_person')
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize person - {}'.format(e))
            return Response(status=403)

    def create(self, request, *args, **kwargs):
        try:
            print(request.data)
            print("*****************************")
            print("*****************************")
            print("*****************************")
            print("*****************************")
            print("*****************************")
            print("*****************************")
            serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error('Error while serialize vehicle - {}'.format(e))
            return Response(status=403)

    def get_queryset(self):
        """
        Optionally restricts the returned vehicle_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_vehicle to a given signal,
        by filtering against a `signal` or a `chassi` query parameter in the URL.
        """
        queryset = Vehicle.objects.all()
        my = self.request.query_params.get('my')
        has_my = Q()
        signal = self.request.query_params.get('signal')
        has_signal = Q()
        chassi = self.request.query_params.get('chassi')
        has_chassi = Q()
        if signal is not None:
            has_signal = Q(signal__icontains=signal)
        if chassi is not None:
            has_chassi = Q(chassi__icontains=chassi)
        if my is not None:
            has_my = Q(created_by=self.request.user)
        return queryset.filter(has_my & has_signal & has_chassi)

    def perform_create(self, serializer):
        try:
            print('no try do perform_create')
            if serializer.is_valid():
                instance = serializer.save(created_by=self.request.user)
                if instance.signal:
                    helpers.process_cortex_consult(username=self.request.user.username, placa=instance.signal)
                for image in instance.images.all():
                    image.created_by = self.request.user
                    image.save()
                    assign_perm("change_vehicle_image", self.request.user, image)
                    assign_perm("delete_vehicle_image", self.request.user, image)
                assign_perm("change_vehicle", self.request.user, instance)
                assign_perm("delete_vehicle", self.request.user, instance)
                return Response(serializer.data, status=201)
        except Exception as e:
            logger.error('Error while save serialize vehicle - {}'.format(e))
            # return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(method='get', manual_parameters=[signal, chassi, my])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)