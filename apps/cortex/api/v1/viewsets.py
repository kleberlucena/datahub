from datetime import date
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotAllowed
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import logging

from apps.cortex.api.v1.serializers import PersonCortexSerializer, BasicPersonCortexSerializer
from apps.cortex.models import PersonCortex, RegistryCortex
from apps.cortex import helpers
from apps.cortex.services import PortalCortexService
from apps.person.models import Person
from apps.person.api.v1.serializers import PersonSerializer
from apps.document.models import Document, DocumentType
from base import helpers as helpers_base

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = PortalCortexService()

name = openapi.Parameter('name', openapi.IN_QUERY,
                         description="param name", type=openapi.TYPE_STRING)
mother_name = openapi.Parameter(
    'mother_name', openapi.IN_QUERY, description="param mother_name", type=openapi.TYPE_STRING)
birthdate = openapi.Parameter('birthdate', openapi.IN_QUERY, description="param birthdate",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)


class PersonRetrieveView(generics.RetrieveAPIView):
    queryset = PersonCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = PersonCortexSerializer
    # for key
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(PersonCortex, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(method='get')
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PessoaByCpfViewSet(generics.GenericAPIView):
    queryset = PersonCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = PersonCortexSerializer

    def get_serializer_class(self):
        if self.request.user.groups.filter(name__in=['profile:person_intermediate', 'profile:person_advanced', 'profile:person_basic']).exists():
            return PersonCortexSerializer
        return super().get_serializer_class()

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'])
    def get(self, request, cpf):
        username = request.user.username
        cpf = helpers_base.validate_cpf(cpf)
        person_cortex = None

        try:
            instance = helpers.process_cortex_consult(
                username=username, cpf=cpf)
            print(instance)
            documents = helpers.validate_document(cpf)
            if documents is None:
                helpers.create_person_and_document(instance)
            else:
                helpers.update_registers(
                    documents=documents, person_cortex=instance)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize person_cortex - {}'.format(e))
            return Response(status=500)

    def get_queryset(self):
        return PersonCortex.objects.all()

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class PessoaByBirthdateViewSet(generics.ListAPIView):
    queryset = PersonCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = PersonCortexSerializer

    @swagger_auto_schema(method='get', manual_parameters=[name, birthdate])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        username = request.user.username
        name = request.query_params.get('name', None)
        birthdate = request.query_params.get('birthdate', None)

        try:
            if self.request.user.groups.filter(name__in=['profile:person_intermediate', 'profile:person_advanced', 'profile:person_basic']).exists():
                people_json = portalCortexService.get_person_by_birthdate(username=username, name=name,
                                                                          birthdate=birthdate)
                return Response(people_json)
            raise HttpResponseNotAllowed
        except Exception as e:
            logger.error(
                'Error while getting personcortex by birthdate - {}'.format(e))
            raise HttpResponseServerError

    def get_queryset(self):
        return PersonCortex.objects.all()


class PessoaByMotherViewSet(generics.ListAPIView):
    queryset = PersonCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = PersonCortexSerializer

    @swagger_auto_schema(method='get', manual_parameters=[name, mother_name])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        username = request.user.username
        name = request.query_params.get('name', None)
        mother_name = request.query_params.get('mother_name', None)

        try:
            if self.request.user.groups.filter(name__in=['profile:person_intermediate', 'profile:person_advanced', 'profile:person_basic']).exists():
                people_json = portalCortexService.get_person_by_mother(
                    username=username, name=name, mother_name=mother_name)
                return Response(people_json)
            raise HttpResponseNotAllowed
        except Exception as e:
            logger.error(
                'Error while getting personcortex mother - {}'.format(e))
            raise HttpResponseServerError

    def get_queryset(self):
        return PersonCortex.objects.all()
