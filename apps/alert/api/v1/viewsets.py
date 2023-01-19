import json
from django.http import HttpResponse, HttpRequest
from django.db.models import Q
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import logging

from apps.alert.models import AlertCortex, PersonAlertCortex, VehicleAlertCortex
from . import serializers

placa = openapi.Parameter('placa', openapi.IN_QUERY, description="param placa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY, description="param cpf", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AddAlertCortexListView(generics.ListCreateAPIView):
    queryset = AlertCortex.objects.all()
    serializer_class = serializers.AlertCortexPolymorphicSerializer

    @swagger_auto_schema(method='get')
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = AlertCortex.objects.get_queryset()
        signal_number = self.request.query_params.get('placa')
        has_signal = Q()
        if signal_number is not None:
            has_signal = Q(placa__icontains=signal_number)
        return queryset.filter(has_signal)


class AddVehicleAlertCortexListView(generics.ListCreateAPIView):
    queryset = VehicleAlertCortex.objects.all()
    serializer_class = serializers.VehicleAlertCortexSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'dataPassagem', 'municipioLocal', 'dataOcorrencia']
    ordering = ['-created_at']

    @swagger_auto_schema(method='get', manual_parameters=[placa])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = VehicleAlertCortex.objects.get_queryset()
        signal_number = self.request.query_params.get('placa')
        has_signal = Q()
        if signal_number is not None:
            has_signal = Q(placa__icontains=signal_number)
        return queryset.filter(has_signal)


class AddPersonAlertCortexListView(generics.ListCreateAPIView):
    queryset = PersonAlertCortex.objects.all()
    serializer_class = serializers.PersonAlertCortexSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'nome', 'municipio', 'dataNascimento']
    ordering = ['-created_at']

    @swagger_auto_schema(method='get', manual_parameters=[cpf])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = PersonAlertCortex.objects.get_queryset()
        cpf = self.request.query_params.get('cpf')
        has_cpf = Q()
        if cpf is not None:
            has_cpf = Q(cpf__icontains=cpf)
        return queryset.filter(has_cpf)