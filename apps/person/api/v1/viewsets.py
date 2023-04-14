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

from apps.person.api.v1 import serializers, list_serializers
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageSerializer, ImageMediumSerializer
from apps.document.api.serializers import DocumentSerializer
from apps.person.models import *
from apps.person import helpers
from apps.bnmp import helpers as helpers_bnmp
from apps.cortex import helpers as helpers_cortex
from apps.cortex.models import RegistryCortex
from apps.portal.models import Entity, Military
from base import helpers as helpers_base
import logging


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
tattoo_label = openapi.Parameter('tattoo_label', openapi.IN_QUERY, description="param tatuagem da pessoa", type=openapi.TYPE_STRING)
entity_name = openapi.Parameter('entity_name', openapi.IN_QUERY, description="param Unidade do usuário", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class PersonByCpfViewSet(generics.ListAPIView):
    queryset = Person.objects.all()
    #serializer_class = serializers.PersonSerializer
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:person_advanced').exists():
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_intermediate').exists():
            return serializers.IntermediatePersonSerializer
        elif self.request.user.groups.filter(name='profile:person_basic').exists():
            return serializers.BasicPersonSerializer
        raise Http404 

    def get_queryset(self):
        queryset = Person.objects.get_queryset()
        document_number = self.request.query_params.get('cpf')
        person = None
        has_cpf = Q()
        if document_number is not None:
            has_cpf = Q(documents__number__icontains=document_number)
        return queryset.filter(has_cpf)

    @swagger_auto_schema(method='get', manual_parameters=[cpf])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request):
        # obtenha a lista de resultados usando o queryset do viewset
        queryset = self.get_queryset()
        cpf = self.request.query_params.get('cpf')
        try:
            person_cortex = helpers_cortex.process_cortex_consult(username=request.user.username, cpf=cpf)
            documents = helpers_cortex.validate_document(number=cpf)
            if documents is None or len(documents) == 0:
                logger.info('Without documents - {}'.format(documents))
                helpers_cortex.create_person_and_document(person_cortex)
            else:
                logger.info('With documents - {}'.format(documents))
                helpers_cortex.update_registers(documents, person_cortex)
        except Exception as e:
            logger.error('Error while get person_cortex - {}'.format(e))
        try:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize person - {}'.format(e))
            return Response(status=403)


class AddPersonListView(generics.ListCreateAPIView):
    permission_classes = [DjangoObjectPermissions, DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    queryset = Person.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            if self.request.user.groups.filter(name__icontains='profile:person').exists():
                return serializers.PersonSerializer
            raise Http404  
        elif self.request.user.groups.filter(name='profile:person_advanced').exists():
            return list_serializers.PersonListSerializer
        elif self.request.user.groups.filter(name='profile:person_intermediate').exists():
            return list_serializers.IntermediatePersonListSerializer
        elif self.request.user.groups.filter(name='profile:person_basic').exists():
            return list_serializers.BasicPersonListSerializer
        raise Http404  

    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def list(self, request, *args, **kwargs):
        try:
            probable_cpf = self.request.query_params.get('document_number')
            cpf = helpers_base.validate_cpf(probable_cpf)
            helpers.process_cortex_consult(username=request.user.username, cpf=cpf)            
            helpers.process_bnmp_consult(username=request.user.username, cpf=cpf)            
        except Exception as e:
            logger.error('Error while get person_cortex - {}'.format(e))
        
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
        Optionally restricts the returned person_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_person to a given document,
        by filtering against a `document_name` or a `document_number` query parameter in the URL.
        """
        queryset = Person.objects.all()
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
        tattoo_label = self.request.query_params.get('tattoo_label')
        has_tattoo = Q()
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
            has_name = Q(documents__name__unaccent__icontains=document_name)  | Q(nicknames__label__unaccent__icontains=document_name)
        if document_mother is not None:
            has_mother = Q(documents__mother__unaccent__icontains=document_mother)
        if document_father is not None:
            has_father = Q(documents__father__unaccent__icontains=document_father)
        if document_birth_date is not None:
            has_birth_date = Q(documents__birth_date__icontains=document_birth_date)
        if document_number is not None:
            has_number = Q(documents__number__icontains=document_number)
        if nickname_label is not None:
            has_nickname = Q(nicknames__label__unaccent__icontains=nickname_label) | Q(documents__name__unaccent__icontains=nickname_label)
        if tattoo_label is not None:
            has_tattoo = Q(tattoos__label__unaccent__icontains=tattoo_label)
        if entity_name is not None:
            has_entity = Q(entity__name__unaccent__icontains=entity_name)
        if my is not None or self.request.user.groups.filter(name__in=['profile:person_intermediate', 'profile:person_basic']).exists():
            has_my = Q(created_by=self.request.user)
        return queryset.filter(has_my & 
                               has_city & 
                               has_neighborhood &
                               has_street &
                               has_complement & 
                               has_reference & 
                               has_zipcode & 
                               has_nickname & 
                               has_tattoo &
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
                    for nickname in instance.nicknames.all():
                        nickname.entity=entity
                        nickname.created_by=user
                        nickname.save()
                        assign_perm("change_nickname", self.request.user, nickname)
                        assign_perm("delete_nickname", self.request.user, nickname)
                    for tattoo in instance.tattoos.all():
                        tattoo.entity=entity
                        tattoo.created_by=user
                        tattoo.save()
                        assign_perm("change_tattoo", self.request.user, tattoo)
                        assign_perm("delete_tattoo", self.request.user, tattoo)
                    for address in instance.addresses.all():
                        address.entity=entity
                        address.created_by=user
                        address.save()
                        assign_perm("change_address", self.request.user, address)
                        assign_perm("delete_address", self.request.user, address)
                    for physical in instance.physicals.all():
                        physical.entity=entity
                        physical.created_by=user
                        physical.save()
                        assign_perm("change_physical", self.request.user, physical)
                        assign_perm("delete_physical", self.request.user, physical)
                    for document in instance.documents.all():
                        document.entity=entity
                        document.created_by=user
                        document.save()                        
                        if document.type.label == 'CPF':
                            helpers.process_cortex_consult(username=self.request.user.username, cpf=document.number)
                            helpers.process_bnmp_consult(username=self.request.user.username, cpf=cpf) 
                        assign_perm("change_document", self.request.user, document)
                        assign_perm("delete_document", self.request.user, document)
                        for image in document.images.all():
                            image.entity=entity
                            image.created_by=user
                            image.save()
                            assign_perm("change_documentimage", self.request.user, image)
                            assign_perm("delete_documentimage", self.request.user, image)
                    for face in instance.faces.all():
                        face.entity=entity
                        face.created_by=user
                        face.save()
                        assign_perm("change_face", self.request.user, face)
                        assign_perm("delete_face", self.request.user, face)
                    for image in instance.images.all():
                        image.entity=entity
                        image.created_by=user
                        image.save()
                        assign_perm("change_image", self.request.user, image)
                        assign_perm("delete_image", self.request.user, image)
                    assign_perm("change_person", self.request.user, instance)
                    assign_perm("delete_person", self.request.user, instance)
                    instance.save()               
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.error, status=422)
            except Exception as e:
                logger.warn('Warning while serialize person - {}'.format(e))
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
                                            tattoo_label,
                                            entity_name])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PersonRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Person.objects.all()
    permission_classes = [DjangoObjectPermissions]
    # serializer_class = serializers.PersonSerializer
    # for key
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:person_advanced').exists():
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_intermediate').exists():
            return serializers.IntermediatePersonSerializer
        elif self.request.user.groups.filter(name='profile:person_basic').exists():
            return serializers.BasicPersonSerializer
        raise Http404

    @swagger_auto_schema()
    @action(detail=True, methods=['DELETE'])
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        user = self.request.user
        unauthorized = HttpResponse("Unauthorized", status=401)
        if user.has_perm('person.delete_person', instance):
            for address in instance.addresses.all():
                if not user.has_perm('address.delete_address', address):
                    return unauthorized
            for document in instance.documents.all():
                if not user.has_perm('document.delete_document', document):
                    return unauthorized
            for image in instance.images.all():
                if not user.has_perm('image.delete_image', image):
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
            instance = get_object_or_404(Person, uuid=kwargs['uuid'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize person - {}'.format(e))
            return Response(status=403)


# views to Add attributes of person

class PersonAddFaceView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Face.objects.all()
    serializer_class = serializers.FaceSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(person=person, entity=entity, created_by=user)
                    assign_perm("change_face", self.request.user, instance)
                    assign_perm("delete_face", self.request.user, instance)
                    person.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save face - {}'.format(e))
                transaction.set_rollback(True)
                raise e
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddTattooView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Tattoo.objects.all()
    serializer_class = serializers.TattooSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(person=person, entity=entity, created_by=user)
                    assign_perm("change_tattoo", self.request.user, instance)
                    assign_perm("delete_tattoo", self.request.user, instance)
                    person.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Tattoo - {}'.format(e))
                transaction.set_rollback(True)
                raise e
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddNicknameView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Nickname.objects.all()
    serializer_class = serializers.NicknameSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(person=person, entity=entity, created_by=user)
                    assign_perm("change_nickname", self.request.user, instance)
                    assign_perm("delete_nickname", self.request.user, instance)
                    person.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Nickname - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddPhysicalView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Physical.objects.all()
    serializer_class = serializers.PhysicalSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(person=person, entity=entity, created_by=user)
                    assign_perm("change_physical", self.request.user, instance)
                    assign_perm("delete_physical", self.request.user, instance)
                    person.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Physical - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddDocumentView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(entity=entity, created_by=user)
                    for image in instance.images.all():
                            image.entity=entity
                            image.created_by=user
                            image.save()
                            assign_perm("change_documentimage", self.request.user, image)
                            assign_perm("delete_documentimage", self.request.user, image)
                    person.documents.add(instance)
                    assign_perm("change_document", self.request.user, instance)
                    assign_perm("delete_document", self.request.user, instance)
                    person.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Document - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddAddressView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(entity=entity, created_by=user)
                    person.addresses.add(instance)
                    assign_perm("change_address", self.request.user, instance)
                    assign_perm("delete_address", self.request.user, instance)
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Address - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddImageView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(entity=entity, created_by=user)
                    person.images.add(instance)
                    assign_perm("change_image", self.request.user, instance)
                    assign_perm("delete_image", self.request.user, instance)
                    person.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Image - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# views to recovery, Update or Delete attributes of person

class FaceUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Face.objects.all()
    serializer_class = serializers.FaceSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Face, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Face, uuid=kwargs['uuid'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='DELETE')
    @action(detail=True, methods=['DELETE'])
    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Face, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('person.delete_face', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)
        
    @swagger_auto_schema(method='DELETE')
    @action(detail=True, methods=['DELETE'])
    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TattooUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tattoo.objects.all()
    serializer_class = serializers.TattooSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Tattoo, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Tattoo, uuid=kwargs['uuid'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Tattoo, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('person.delete_tattoo', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)


class NicknameUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nickname.objects.all()
    serializer_class = serializers.NicknameSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Nickname, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Nickname, uuid=kwargs['uuid'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Nickname, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('person.delete_nickname', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)


class PhysicalUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Physical.objects.all()
    serializer_class = serializers.PhysicalSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Physical, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Physical, uuid=kwargs['uuid'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Physical, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('person.delete_physical', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)


class DocumentUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Document, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Document, uuid=kwargs['uuid'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Document, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('document.delete_document', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)


class AddressUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Address, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Address, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Address, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('address.delete_address', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)


class ImageUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Image, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Image, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Image, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('image.delete_image', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)
