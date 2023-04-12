from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from guardian.shortcuts import assign_perm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from base import helpers as base_helpers
from apps.person.models import *
from apps.bnmp import helpers
from apps.cortex.services import PortalCortexService
from apps.bnmp.api.v1.serializers import *
from apps.bnmp.models import PersonBNMP

# Get an instance of a logger
logger = logging.getLogger(__name__)

document_name = openapi.Parameter('document_name', openapi.IN_QUERY, description="param nome do documento da pessoa", type=openapi.TYPE_STRING)
document_number = openapi.Parameter('document_number', openapi.IN_QUERY, description="param número do documento da pessoa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY, description="param número do CPF da pessoa", type=openapi.TYPE_STRING)
nickname_label = openapi.Parameter('nickname_label', openapi.IN_QUERY, description="param alcunha da pessoa", type=openapi.TYPE_STRING)

portalCortexService = PortalCortexService()

class PessoaByCpfViewSet(generics.GenericAPIView):
    queryset = PersonBNMP.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]
    serializer_class = PersonBNMPSerializer

    def get_queryset(self):
        return PersonBNMP.objects.all()      

    @swagger_auto_schema(method='get', manual_parameters=[cpf])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        cpf = self.request.query_params.get('cpf')
        username = self.request.user.username

        try:
            cpf = base_helpers.validate_cpf(value=cpf)
            instance = helpers.process_bnmp_consult(username=username, cpf=cpf)
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error('Error while validate CPF - {}'.format(e))
            return Response(status=422)
        except Exception as e:
            logger.error('Error while serialize person_bnmp - {}'.format(e))
            return Response(status=500)