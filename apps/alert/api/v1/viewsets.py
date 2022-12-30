from django.http import HttpResponse
from django.db.models import Q
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import logging

from apps.alert.models import AlertCortex, PersonAlertCortex, VehicleAlertCortex
from . import serializers

placa = openapi.Parameter('placa', openapi.IN_QUERY, description="param placa", type=openapi.TYPE_STRING)
mother_name = openapi.Parameter('mother_name', openapi.IN_QUERY, description="param mother_name", type=openapi.TYPE_STRING)
birthdate = openapi.Parameter('birthdate', openapi.IN_QUERY, description="param birthdate", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)


class AddVehicleAlertCortexListView(generics.ListCreateAPIView):
    queryset = VehicleAlertCortex.objects.all()
    serializer_class = serializers.VehicleAlertCortexSerializer

    @swagger_auto_schema(method='get', manual_parameters=[placa])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        username = request.user.username
        placa = request.query_params.get('placa', None)

        try:
            instance = self.get_queryset()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            raise logging.error('Error while getting personcortex by birthdate - {}'.format(e))

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        queryset = AlertCortex.objects.get_queryset()
        signal_number = self.request.query_params.get('placa')
        has_signal = Q()
        if signal_number is not None:
            has_signal = Q(placa__icontains=signal_number)
        return queryset.filter(has_signal)

    def perform_create(self, serializer):
        data = self.request.data
        if serializer.is_valid():
            serializer.save(**data)
            return Response(status=201)
        else:
            return Response(serializer.errors, status=400)

