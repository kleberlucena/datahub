import logging
from django.http import HttpResponse, Http404
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, mixins, status
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, get_objects_for_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.portal.models import Entity, Military
from apps.fact.models import Fact, FactType
from apps.fact.api.v1.serializers import FactSerializer, FactTypeSerializer

my = openapi.Parameter('my', openapi.IN_QUERY, description="param meu, que filtra os cadastros de pessoa pelo usuário", type=openapi.TYPE_BOOLEAN)
address_city = openapi.Parameter('address_city', openapi.IN_QUERY, description="param cidade do endereço da pessoa", type=openapi.TYPE_STRING)
address_neighborhood = openapi.Parameter('address_neighborhood', openapi.IN_QUERY, description="param bairro do endereço da pessoa", type=openapi.TYPE_STRING)
address_street = openapi.Parameter('address_street', openapi.IN_QUERY, description="param rua do endereço da pessoa", type=openapi.TYPE_STRING)
address_complement = openapi.Parameter('address_complement', openapi.IN_QUERY, description="param complemento do endereço da pessoa", type=openapi.TYPE_STRING)
address_reference = openapi.Parameter('address_reference', openapi.IN_QUERY, description="param referência do endereço da pessoa", type=openapi.TYPE_STRING)
address_zipcode = openapi.Parameter('address_zipcode', openapi.IN_QUERY, description="param CEP do endereço da pessoa", type=openapi.TYPE_STRING)
document_name = openapi.Parameter('document_name', openapi.IN_QUERY, description="param nome do documento da pessoa", type=openapi.TYPE_STRING)
document_mother = openapi.Parameter('document_mother', openapi.IN_QUERY, description="param mãe do documento da pessoa", type=openapi.TYPE_STRING)
document_father = openapi.Parameter('document_father', openapi.IN_QUERY, description="param pai do documento da pessoa", type=openapi.TYPE_STRING)
document_birth_date = openapi.Parameter('document_birth_date', openapi.IN_QUERY, description="FORMAT: YYYY-MM-DD", type=openapi.FORMAT_DATE)
document_number = openapi.Parameter('document_number', openapi.IN_QUERY, description="param número do documento da pessoa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY, description="param número do CPF da pessoa", type=openapi.TYPE_STRING)
nickname_label = openapi.Parameter('nickname_label', openapi.IN_QUERY, description="param alcunha da pessoa", type=openapi.TYPE_STRING)
entity_name = openapi.Parameter('entity_name', openapi.IN_QUERY, description="param Unidade do usuário", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AddFactListView(generics.ListCreateAPIView):
    permission_classes = [DjangoObjectPermissions, DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    queryset = Fact.objects.all()

    def get_serializer_class(self):
        if self.request.user.groups.filter(name__icontains='profile:person_advanced').exists():
            return FactSerializer
        raise Http404  

    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def list(self, request, *args, **kwargs):        
        try:            
            self.permission_classes = [DjangoModelPermissions]
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize person - {}'.format(e))
            return Response(status=403)
        

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            retorno = self.perform_create(serializer)
            return retorno
        except Exception as e:
            print('nem serializou')
            return Response(status=403)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)     

    def get_queryset(self):
        """
        Optionally restricts the returned fact_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_fact to a given document,
        by filtering against a `document_name` or a `document_number` query parameter in the URL.
        """
        queryset = Fact.objects.all()
        my = self.request.query_params.get('my')
        has_my = Q()
        address_city = self.request.query_params.get('address_city')
        has_city = Q()
        address_neighborhood = self.request.query_params.get('address_neighborhood')
        has_neighborhood = Q()
        address_street = self.request.query_params.get('address_street')
        has_street = Q()
        address_complement = self.request.query_params.get('address_complement')
        has_complement = Q()
        address_reference = self.request.query_params.get('address_reference')
        has_reference = Q()
        address_zipcode = self.request.query_params.get('address_zipcode')
        has_zipcode = Q()
        document_name = self.request.query_params.get('document_name')
        has_name = Q()
        document_mother = self.request.query_params.get('document_mother')
        has_mother = Q()
        document_father = self.request.query_params.get('document_father')
        has_father = Q()
        document_birth_date = self.request.query_params.get('document_birth_date')
        has_birth_date = Q()
        document_number = self.request.query_params.get('document_number')
        has_number = Q()
        nickname_label = self.request.query_params.get('nickname_label')
        has_nickname = Q()        
        entity_name = self.request.query_params.get('entity_name')
        has_entity = Q()
        if address_city is not None:
            has_city = Q(addresses__city__unaccent__icontains=address_city)
        if address_neighborhood is not None:
            has_neighborhood = Q(addresses__neighborhood__unaccent__icontains=address_neighborhood)
        if address_street is not None:
            has_street = Q(addresses__street__unaccent__icontains=address_street)
        if address_complement is not None:
            has_complement = Q(addresses__complement__unaccent__icontains=address_complement)
        if address_reference is not None:
            has_reference = Q(addresses__reference__unaccent__icontains=address_reference)
        if address_zipcode is not None:
            has_zipcode = Q(addresses__zipcode__icontains=address_zipcode)
        if document_name is not None:
            has_name = Q(suspects__documents__name__unaccent__icontains=document_name)  | Q(suspects__nicknames__label__unaccent__icontains=document_name)
        if document_mother is not None:
            has_mother = Q(suspects__documents__mother__unaccent__icontains=document_mother)
        if document_father is not None:
            has_father = Q(suspects__documents__father__unaccent__icontains=document_father)
        if document_birth_date is not None:
            has_birth_date = Q(suspects__documents__birth_date__icontains=document_birth_date)
        if document_number is not None:
            has_number = Q(suspects__documents__number__icontains=document_number)
        if nickname_label is not None:
            has_nickname = Q(suspects__nicknames__label__unaccent__icontains=nickname_label) | Q(suspects__documents__name__unaccent__icontains=nickname_label)
        if entity_name is not None:
            has_entity = Q(entity__name__unaccent__icontains=entity_name)
        if my is not None:
            has_my = Q(created_by=self.request.user)
        return queryset.filter(has_my & 
                               has_city & 
                               has_neighborhood &
                               has_street &
                               has_complement & 
                               has_reference & 
                               has_zipcode & 
                               has_nickname & 
                               has_number & 
                               has_name &
                               has_mother &
                               has_father &
                               has_birth_date &
                               has_entity)

    def perform_create(self, serializer):
        with transaction.atomic():
            try:
                person_cortex = None
                if serializer.is_valid():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save()
                    instance.created_by=user
                    instance.entity=entity

                    for address in instance.addresses.all():
                        address.entity=entity
                        address.created_by=user
                        address.save()
                        assign_perm("change_address", self.request.user, address)
                        assign_perm("delete_address", self.request.user, address)
                    
                    for image in instance.images.all():
                        image.entity=entity
                        image.created_by=user
                        image.save()
                        assign_perm("change_factimage", self.request.user, image)
                        assign_perm("delete_factimage", self.request.user, image)
                    assign_perm("change_fact", self.request.user, instance)
                    assign_perm("delete_fact", self.request.user, instance)
                    instance.save()               
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.error, status=422)
            except Exception as e:
                logger.warn('Warning while serialize fact - {}'.format(e))
                transaction.set_rollback(True)
                raise e

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(method='get', 
                         manual_parameters=[my, 
                                            address_city,
                                            address_neighborhood,
                                            address_street,
                                            address_complement,
                                            address_reference,
                                            address_zipcode,
                                            document_name, 
                                            document_mother, 
                                            document_father, 
                                            document_birth_date, 
                                            document_number, 
                                            nickname_label,
                                            entity_name])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FactRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Fact.objects.all()
    permission_classes = [DjangoObjectPermissions]
    # serializer_class = serializers.PersonSerializer
    # for key
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:person_advanced').exists():
            return FactSerializer
        raise Http404

    @swagger_auto_schema()
    @action(detail=True, methods=['DELETE'])
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Fact, uuid=self.kwargs['uuid'])
        user = self.request.user
        unauthorized = HttpResponse("Unauthorized", status=401)
        if user.has_perm('fact.delete_fact', instance):
            for address in instance.addresses.all():
                if not user.has_perm('address.delete_address', address):
                    return unauthorized
            for image in instance.images.all():
                if not user.has_perm('image.delete_factimage', image):
                    return unauthorized
            if instance.soft_delete_cascade_policy_action(deleted_by=user):
                return HttpResponse("Deleted", status=204)
            else:
                return HttpResponse("Deleting", status=202)
        else:
            return unauthorized

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'])
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Fact, uuid=kwargs['uuid'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize fact - {}'.format(e))
            return Response(status=403)


class FactTypeListViewSet(generics.ListAPIView):
    queryset = FactType.objects.all()
    serializer_class = FactTypeSerializer