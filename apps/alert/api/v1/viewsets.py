import json
from django.http import HttpResponse, Http404
from django.db.models import Q
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from drf_yasg.utils import swagger_auto_schema
import logging

from apps.alert.models import AlertCortex, PersonAlertCortex, VehicleAlertCortex
from . import serializers

placa = openapi.Parameter('placa', openapi.IN_QUERY,
                          description="param placa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY,
                        description="param cpf", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AddAlertCortexListView(generics.ListCreateAPIView):
    queryset = AlertCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = serializers.AlertCortexPolymorphicSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.user.groups.filter(name='profile:alert_advanced').exists():
            return serializers.AlertCortexPolymorphicSerializer
        else:
            raise PermissionDenied

    # @swagger_auto_schema(method='get', manual_parameters=[cpf, placa])
    @swagger_auto_schema(method='get')
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        """ cpf = self.request.query_params.get('cpf')
        signal_number = self.request.query_params.get('placa')
        has_cpf = Q()
        has_signal = Q()
        if cpf is not None:
            has_cpf = Q(cpf__icontains=cpf)
        if signal_number is not None:
            has_signal = Q(placa__icontains=signal_number)
        queryset = queryset.filter(has_signal | has_cpf) """
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data == []:
            raise NotFound
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class AddVehicleAlertCortexListView(generics.ListCreateAPIView):
    queryset = VehicleAlertCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = serializers.VehicleAlertCortexSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'dataPassagem',
                       'municipioLocal', 'dataOcorrencia']
    ordering = ['-created_at']

    def get_serializer_class(self):
        print(self.request.user.groups.filter(
            name='profile:alert_advanced').exists())
        if self.request.method in ['POST']:
            return serializers.VehicleAlertCortexSerializer
        elif self.request.user.groups.filter(name='profile:alert_advanced').exists():
            return serializers.VehicleAlertCortexSerializer
        elif self.request.user.groups.filter(name='profile:alert_vehicle_intermediate').exists():
            return serializers.IntermediateVehicleAlertCortexSerializer
        elif self.request.user.groups.filter(name='profile:alert_vehicle_basic').exists():
            return serializers.BasicVehicleAlertCortexSerializer
        else:
            raise PermissionDenied

    @swagger_auto_schema(method='get', manual_parameters=[placa])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        signal_number = self.request.query_params.get('placa')
        has_signal = Q()
        if signal_number is not None:
            has_signal = Q(placa__icontains=signal_number)
        queryset = queryset.filter(has_signal)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data == []:
            raise NotFound
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class AddPersonAlertCortexListView(generics.ListCreateAPIView):
    queryset = PersonAlertCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = serializers.PersonAlertCortexSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'nome', 'municipio', 'dataNascimento']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return serializers.PersonAlertCortexSerializer
        elif self.request.user.groups.filter(name='profile:alert_advanced').exists():
            return serializers.PersonAlertCortexSerializer
        elif self.request.user.groups.filter(name='profile:alert_person_intermediate').exists():
            return serializers.IntermediatePersonAlertCortexSerializer
        elif self.request.user.groups.filter(name='profile:alert_person_basic').exists():
            return serializers.BasicPersonAlertCortexSerializer
        else:
            raise PermissionDenied

    @swagger_auto_schema(method='get', manual_parameters=[cpf])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        cpf = self.request.query_params.get('cpf')
        has_cpf = Q()
        if cpf is not None:
            has_cpf = Q(cpf__icontains=cpf)
        queryset = queryset.filter(has_cpf)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if serializer.data == []:
            raise NotFound
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
