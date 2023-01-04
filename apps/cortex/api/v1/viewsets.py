from datetime import date
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import logging

from apps.cortex.api.v1.serializers import PersonCortexSerializer
from apps.cortex.models import PersonCortex
from apps.cortex.services import PortalCortexService
from apps.person.models import Person, Registry
from apps.person.api.v1.serializers import PersonSerializer
from apps.document.models import Document, DocumentType

# Get an instance of a logger
logger = logging.getLogger(__name__)

portalCortexService = PortalCortexService()

name = openapi.Parameter('name', openapi.IN_QUERY, description="param name", type=openapi.TYPE_STRING)
mother_name = openapi.Parameter('mother_name', openapi.IN_QUERY, description="param mother_name", type=openapi.TYPE_STRING)
birthdate = openapi.Parameter('birthdate', openapi.IN_QUERY, description="param birthdate", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)


class PersonRetrieveView(generics.RetrieveAPIView):
    queryset = PersonCortex.objects.all()
    serializer_class = PersonCortexSerializer
    # for key
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(PersonCortex, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PessoaByCpfViewSet(generics.GenericAPIView):
    queryset = PersonCortex.objects.all()
    serializer_class = PersonCortexSerializer

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'])
    def get(self, request, cpf):
        username = request.user.username
        person_cortex = None
        try:
            person_cortex = PersonCortex.objects.get(numeroCPF=cpf)
        except PersonCortex.DoesNotExist:
            person_cortex = None
        except Exception as e:
            raise logger.error('Error while getting personcortex local - {}'.format(e))
        try:
            if person_cortex is None:
                person_json = portalCortexService.get_person_by_cpf(username=username, cpf=cpf)
                value = person_json['numeroCPF']
                person_cortex, created = PersonCortex.objects.update_or_create(
                        numeroCPF=value, defaults={**person_json},
                    )
            elif person_cortex.updated_at.date() < date.today():
                person_json = portalCortexService.get_person_by_cpf(username=username, cpf=cpf)
                person_cortex.save(person_json)
        except Exception as e:
            raise logger.error('Error while getting personcortex on cortex repository - {}'.format(e))
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            registry = Registry.objects.get(system_uuid=person_cortex.uuid)
        except Registry.DoesNotExist:
            person = Person.objects.create()
            document = Document(number=person_cortex.numeroCPF,
                                name=person_cortex.nomeCompleto,
                                birth_date=person_cortex.dataNascimento,
                                mother=person_cortex.nomeMae,
                                type=DocumentType.objects.get(label="CPF"))
            document.save()
            person.documents.add(document)
            person.save()
            registry = Registry.objects.create(system_label="CORTEX", system_uuid=person_cortex.uuid, person=person)
        except Exception as e:
            raise logger.error('Error while getting person and add Registry - {}'.format(e))
            return Response(status=500)

        try:
            instance = get_object_or_404(PersonCortex, numeroCPF=cpf)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            raise logger.error('Error while serialize person_cortex - {}'.format(e))
            return Response(status=500)

    def get_queryset(self):
        return PersonCortex.objects.all()


class PessoaByBirthdateViewSet(generics.ListAPIView):
    queryset = PersonCortex.objects.all()
    serializer_class = PersonCortexSerializer

    @swagger_auto_schema(method='get', manual_parameters=[name, birthdate])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        username = request.user.username
        name = request.query_params.get('name', None)
        birthdate = request.query_params.get('birthdate', None)

        try:
            people_json = portalCortexService.get_person_by_birthdate(username=username, name=name,
                                                                   birthdate=birthdate)
            return Response(people_json)
        except Exception as e:
            raise logger.error('Error while getting personcortex by birthdate - {}'.format(e))

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return PersonCortex.objects.all()


class PessoaByMotherViewSet(generics.ListAPIView):
    queryset = PersonCortex.objects.all()
    serializer_class = PersonCortexSerializer

    @swagger_auto_schema(method='get', manual_parameters=[name, mother_name])
    @action(detail=True, methods=['GET'])
    def get(self, request):
        username = request.user.username
        name = request.query_params.get('name', None)
        mother_name = request.query_params.get('mother_name', None)

        try:
            people_json = portalCortexService.get_person_by_mother(username=username, name=name, mother_name=mother_name)
            return Response(people_json)
        except Exception as e:
            raise logger.error('Error while getting personcortex mother - {}'.format(e))

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return PersonCortex.objects.all()
