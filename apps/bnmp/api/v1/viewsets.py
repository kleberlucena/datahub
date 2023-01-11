from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import filters
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from guardian.shortcuts import assign_perm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from apps.person.models import *
from apps.person import helpers, tasks
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
    serializer_class = PersonBNMPSerializer

    def get_queryset(self):
        print('no queryset')
        cpf = self.request.query_params.get('cpf')
        print(cpf)
        username = self.request.user.username
        print(username)
        person_bnmp = None
        try:
            person_bnmp = PersonBNMP.objects.get(numeroCPF=cpf)
            print(person_bnmp)
        except PersonBNMP.DoesNotExist:
            try:
                print('não encontrado localmente')
                person_bnmp = None
                person_json = portalCortexService.get_person_bnmp_by_cpf(username, cpf)
                print( person_json)
                person_bnmp = PersonBNMP.objects.create(**person_json)  
            except Exception as e:
                logger.error('Error while getting person bnmp remote - {}'.format(e))          
            """ if person_bnmp: 
                bnmp = portalCortexService.get_bnmp_by_idpessoa(username=username, idpessoa=person_bnmp.idpessoa)
                return bnmp """
        except Exception as e:
            logger.error('Error while getting person bnmp - {}'.format(e))
        finally:
            return person_bnmp

    @swagger_auto_schema(method='get', manual_parameters=[cpf])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        print('no get')
        return self.list(request, *args, **kwargs)
    
    def list(self, request):
        print('no list')
        # obtenha a lista de resultados usando o queryset do viewset
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)