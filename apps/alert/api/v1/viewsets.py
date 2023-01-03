from django.http import HttpResponse, HttpRequest
from django.db.models import Q
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import logging

from apps.cortex.api.v1.viewsets import PessoaByCpfViewSet
from apps.alert.models import AlertCortex, PersonAlertCortex, VehicleAlertCortex
from . import serializers

placa = openapi.Parameter('placa', openapi.IN_QUERY, description="param placa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY, description="param cpf", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AddAlertCortexListView(generics.ListCreateAPIView):
    queryset = AlertCortex.objects.all()
    serializer_class = serializers.AlertCortexSerializer

    @swagger_auto_schema(method='get')
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        # username = request.user.username
        # try:
        #     instance = self.get_queryset()
        #     serializer = self.get_serializer(instance)
        #     return Response(serializer.data)
        # except Exception as e:
        #     raise logging.error('Error while getting personcortex by birthdate - {}'.format(e))
        #
        # return Response(status=status.HTTP_404_NOT_FOUND)

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
            serializer.save(dados=data)
            return Response(status=201)
        else:
            return Response(serializer.errors, status=400)


class AddVehicleAlertCortexListView(generics.ListCreateAPIView):
    queryset = VehicleAlertCortex.objects.all()
    serializer_class = serializers.VehicleAlertCortexSerializer

    @swagger_auto_schema(method='get', manual_parameters=[placa])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        # username = request.user.username
        # placa = request.query_params.get('placa', None)
        #
        # try:
        #     instance = self.get_queryset()
        #     serializer = self.get_serializer(instance)
        #     return Response(serializer.data)
        # except Exception as e:
        #     raise logging.error('Error while getting vehiclealertcortex by signal - {}'.format(e))
        #
        # return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        queryset = VehicleAlertCortex.objects.get_queryset()
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


class AddPersonAlertCortexListView(generics.ListCreateAPIView):
    queryset = PersonAlertCortex.objects.all()
    serializer_class = serializers.PersonAlertCortexSerializer

    @swagger_auto_schema(method='get', manual_parameters=[cpf])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        # username = request.user.username
        # cpf = request.query_params.get('cpf', None)
        #
        # try:
        #     instance = self.get_queryset()
        #     serializer = self.get_serializer(instance)
        #     return Response(serializer.data)
        # except Exception as e:
        #     raise logging.error('Error while getting personalertcortex by cpf - {}'.format(e))
        #
        # return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        queryset = PersonAlertCortex.objects.get_queryset()
        cpf = self.request.query_params.get('cpf')
        has_cpf = Q()
        if cpf is not None:
            has_cpf = Q(cpf__icontains=cpf)
        return queryset.filter(has_cpf)

    def create(self, request, *args,**kwargs):
        try:
            print('aquiiiiiiiii')
            data = self.request.data
            print(data)
            instance = PersonAlertCortex.objects.create(**data)
            return Response(status=201)
        except Exception as e:
            raise logger.error('Error while save Person alert - {}'.format(e))
            return Response(status=500)

    def perform_create(self, serializer):
        print('aquiiiiiiiii')
        data = self.request.data
        print(data)
        try:
            if serializer.is_valid():
                instance_alert = serializer.save(**data)
                # print('$$$$$$$$$$$$$$$$$$$$')
                # print(data)
                # instance_person = PessoaByCpfViewSet.as_view()(self.request._request).data
                # print('************')
                # print(instance_person)
                # instance_alert.person = instance_person
                # instance_alert.save()
                # {'detail': ErrorDetail(string='CSRF Failed: CSRF cookie not set.', code='permission_denied')}
                # Internal
                # Server
                # Error: / api / v1 / alert / cortex / person /

                return Response(status=201)
            else:
                logger.warning('Warn while save person alert - {}'.format(serializer))
                return Response(serializer.errors, status=400)
        except Exception as e:
            raise logger.error('Error while save person alert - {}'.format(e))
            return Response(status=500)