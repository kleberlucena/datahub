from django.http import HttpResponse
from django.core.exceptions import ValidationError, FieldError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import action
from guardian.shortcuts import assign_perm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from apps.person.models import *
from apps.bnmp import helpers
from apps.cortex.services import PortalCortexService
from apps.bnmp.api.v1.serializers import *
from apps.bnmp.models import PersonBNMP, MandadoPrisao

# Get an instance of a logger
logger = logging.getLogger(__name__)

mother_name = openapi.Parameter('mother_name', openapi.IN_QUERY,
                                description="param nome da mãe da pessoa", type=openapi.TYPE_STRING)
name = openapi.Parameter('name', openapi.IN_QUERY,
                         description="param nome da pessoa", type=openapi.TYPE_STRING)
birthdate = openapi.Parameter('bithdate', openapi.IN_QUERY,
                              description="param data de nascimento da pessoa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY,
                        description="param número do CPF da pessoa", type=openapi.TYPE_STRING)
idpessoa = openapi.Parameter('idpessoa', openapi.IN_QUERY,
                             description="param número do identificador da pessoa", type=openapi.TYPE_STRING)
nickname = openapi.Parameter('nickname', openapi.IN_QUERY,
                             description="param alcunha da pessoa", type=openapi.TYPE_STRING)

portalCortexService = PortalCortexService()


class PessoaByCpfViewSet(generics.GenericAPIView):
    queryset = PersonBNMP.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = PersonBNMPSerializer

    def get_queryset(self):
        return PersonBNMP.objects.all()

    def get_serializer_class(self):
        if self.request.user.groups.filter(name__icontains='profile:person').exists():
            return PersonBNMPSerializer
        else:
            raise PermissionDenied

    @swagger_auto_schema(method='get', manual_parameters=[cpf])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        cpf = self.request.query_params.get('cpf')
        username = self.request.user.username

        cpf = helpers.validate_cpf(value=cpf)
        instance = helpers.process_bnmp_consult(username=username, cpf=cpf)
        print(instance)
        if instance:
            serializer = self.get_serializer(instance, many=True)
            if serializer.data == []:
                raise NotFound
            return Response(serializer.data)
        else:
            raise NotFound

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({"detail": "Erro na validação do CPF."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class MandadoByIdPessoaViewSet(generics.GenericAPIView):
    queryset = MandadoPrisao.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = MandadoBNMPSerializer

    def get_queryset(self):
        return MandadoPrisao.objects.all()

    @swagger_auto_schema(method='get', manual_parameters=[idpessoa])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        idpessoa = self.request.query_params.get('idpessoa')
        username = self.request.user.username

        instance = helpers.process_bnmp_idpessoa_consult(
            username=username, idpessoa=idpessoa)
        if instance:
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data)
        else:
            raise NotFound

    def handle_exception(self, exc):
        if isinstance(exc, FieldError):
            return Response({"detail": "Erro em um atributo."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if isinstance(exc, ValidationError):
            return Response({"detail": "Erro na validação do CPF."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)


class BNMPExplorerViewSet(generics.GenericAPIView):
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = MandadoBNMPSerializer

    def get_queryset(self):
        return PersonBNMP.objects.all()

    @swagger_auto_schema(method='get', manual_parameters=[mother_name, name, birthdate, nickname])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        mother_name = self.request.query_params.get('mother_name')
        name = self.request.query_params.get('name')
        birthdate = self.request.query_params.get('birthdate')
        nickname = self.request.query_params.get('nickname')
        username = self.request.user.username

        data = helpers.process_bnmp_explorer(
            username=username, mother_name=mother_name, name=name, birthdate=birthdate, nickname=nickname)
        return Response(data)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({"detail": "Erro na validação do CPF."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
