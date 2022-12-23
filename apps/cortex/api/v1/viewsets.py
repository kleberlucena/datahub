from datetime import date
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.shortcuts import get_object_or_404
from apps.cortex.api.v1.serializers import PersonCortexSerializer
from apps.cortex.models import PersonCortex
from apps.cortex.services import PortalCortexService
from apps.person.models import Person, Registry
from apps.document.models import Document, DocumentType

portalCortexService = PortalCortexService()

name = openapi.Parameter('name', openapi.IN_QUERY, description="param name", type=openapi.TYPE_STRING)
mother_name = openapi.Parameter('mother_name', openapi.IN_QUERY, description="param mother_name", type=openapi.TYPE_STRING)
birthdate = openapi.Parameter('birthdate', openapi.IN_QUERY, description="param birthdate", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE)


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
            print('%s (%s)' % (e, type(e)))
        try:
            if person_cortex is None or person_cortex.updated_at.date() < date.today():
                person_json = portalCortexService.get_person_by_cpf(username=username, cpf=cpf)
                PersonCortex.objects.update_or_create(**person_json)
                document = Document.objects.update_or_create(number=person_cortex.numeroCPF, name=person_cortex.nomeCompleto, birth_date=person_cortex.dataNascimento, mother=person_cortex.nomeMae, type=DocumentType.objects.get(label="CPF"))
            if person_cortex:
                person = Person.objects.update_or_create(document=document)
                Registry.objects.update_or_create(system_label="CORTEX", system_uuid=person_cortex.uuid, person=person)
                # TODO: Verificar se essa pessoa est[a na Bacinf, criando caso n'ao exista, vincular atraves do model reg

            instance = get_object_or_404(PersonCortex, numeroCPF=cpf)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            print('%s (%s)' % (e, type(e)))

        return Response(status=status.HTTP_404_NOT_FOUND)

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
            print('%s (%s)' % (e, type(e)))

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
            print('%s (%s)' % (e, type(e)))

        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        return PersonCortex.objects.all()