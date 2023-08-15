import json
from django.http import HttpResponse, Http404
from django.db.models import Q
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
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
municipioPlaca = openapi.Parameter(
    'municipioPlaca', openapi.IN_QUERY, description="param municipioPlaca", type=openapi.TYPE_STRING)
municipioLocal = openapi.Parameter(
    'municipioLocal', openapi.IN_QUERY, description="param municipioLocal", type=openapi.TYPE_STRING)
ufPlaca = openapi.Parameter('ufPlaca', openapi.IN_QUERY,
                            description="param ufPlaca", type=openapi.TYPE_STRING)
ufLocal = openapi.Parameter('ufLocal', openapi.IN_QUERY,
                            description="param ufLocal", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY,
                        description="param cpf", type=openapi.TYPE_STRING)
nome = openapi.Parameter('nome', openapi.IN_QUERY,
                         description="param nome", type=openapi.TYPE_STRING)
municipio = openapi.Parameter(
    'municipio', openapi.IN_QUERY, description="param municipio", type=openapi.TYPE_STRING)
created_at = openapi.Parameter(
    'created_at', openapi.IN_QUERY, description="param created_at", type=openapi.FORMAT_DATETIME)

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
    queryset = VehicleAlertCortex.objects.all().order_by('-created_at')
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = serializers.VehicleAlertCortexSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'dataPassagem',
                       'municipioLocal', 'dataOcorrencia']
    ordering = ['-created_at']

    def get_serializer_class(self):
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

    @swagger_auto_schema(method='get', manual_parameters=[placa, municipioPlaca, municipioLocal, ufPlaca, ufLocal, created_at])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        placa = self.request.query_params.get('placa')
        municipioPlaca = self.request.query_params.get('municipioPlaca')
        municipioLocal = self.request.query_params.get('municipioLocal')
        ufPlaca = self.request.query_params.get('ufPlaca')
        ufLocal = self.request.query_params.get('ufLocal')
        created_at = self.request.query_params.get('created_at')
        has_placa = Q()
        has_municipio_placa = Q()
        has_municipio_local = Q()
        has_uf_placa = Q()
        has_uf_local = Q()
        has_created_at = Q()
        if placa is not None:
            has_placa = Q(placa__icontains=placa)
        if municipioPlaca is not None:
            has_municipio_placa = Q(municipioPlaca__icontains=municipioPlaca)
        if municipioLocal is not None:
            has_municipio_local = Q(municipioLocal__icontains=municipioLocal)
        if ufPlaca is not None:
            has_uf_placa = Q(ufPlaca__icontains=ufPlaca)
        if ufLocal is not None:
            has_uf_local = Q(ufLocal__icontains=ufLocal)
        if created_at is not None:
            has_created_at = Q(created_at__icontains=created_at)
        queryset = queryset.filter(
            has_placa, has_municipio_placa, has_municipio_local, has_uf_placa, has_uf_local, has_created_at)
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
    queryset = PersonAlertCortex.objects.all().order_by('-created_at')
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = serializers.PersonAlertCortexSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'nome', 'cpf', 'municipio']
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

    @swagger_auto_schema(method='get', manual_parameters=[cpf, nome, municipio, created_at])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        cpf = self.request.query_params.get('cpf')
        nome = self.request.query_params.get('nome')
        municipio = self.request.query_params.get('municipio')
        created_at = self.request.query_params.get('created_at')
        has_cpf = Q()
        has_nome = Q()
        has_municipio = Q()
        has_created_at = Q()
        if cpf is not None:
            has_cpf = Q(cpf__icontains=cpf)
        if nome is not None:
            has_nome = Q(nome__icontains=nome)
        if municipio is not None:
            has_municipio = Q(municipio__icontains=municipio)
        if created_at is not None:
            has_created_at = Q(created_at__icontains=created_at)
        queryset = queryset.filter(
            has_cpf, has_nome, has_municipio, has_created_at)

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
