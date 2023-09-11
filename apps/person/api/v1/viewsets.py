from django.http import HttpResponse, Http404
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, mixins, status
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.decorators import action
from guardian.shortcuts import assign_perm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.person.api.v1 import serializers, list_serializers
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageSerializer
from apps.document.api.serializers import DocumentSerializer
from apps.person.models import *
from apps.person import helpers
from apps.bnmp import helpers as helpers_bnmp
from apps.cortex import helpers as helpers_cortex
from apps.cortex.models import RegistryCortex
from apps.portal.models import Entity, Military
from base import helpers as base_helpers
import logging


my = openapi.Parameter('my', openapi.IN_QUERY,
                       description="param meus, que filtra os cadastros de pessoa pelo usuário", type=openapi.TYPE_BOOLEAN)
address_city = openapi.Parameter('address_city', openapi.IN_QUERY,
                                 description="param cidade do endereço da pessoa", type=openapi.TYPE_STRING)
address_neighborhood = openapi.Parameter('address_neighborhood', openapi.IN_QUERY,
                                         description="param bairro do endereço da pessoa", type=openapi.TYPE_STRING)
address_street = openapi.Parameter('address_street', openapi.IN_QUERY,
                                   description="param rua do endereço da pessoa", type=openapi.TYPE_STRING)
address_complement = openapi.Parameter('address_complement', openapi.IN_QUERY,
                                       description="param complemento do endereço da pessoa", type=openapi.TYPE_STRING)
address_reference = openapi.Parameter('address_reference', openapi.IN_QUERY,
                                      description="param referência do endereço da pessoa", type=openapi.TYPE_STRING)
address_zipcode = openapi.Parameter('address_zipcode', openapi.IN_QUERY,
                                    description="param CEP do endereço da pessoa", type=openapi.TYPE_STRING)
document_name = openapi.Parameter('document_name', openapi.IN_QUERY,
                                  description="param nome do documento da pessoa", type=openapi.TYPE_STRING)
document_mother = openapi.Parameter('document_mother', openapi.IN_QUERY,
                                    description="param mãe do documento da pessoa", type=openapi.TYPE_STRING)
document_father = openapi.Parameter('document_father', openapi.IN_QUERY,
                                    description="param pai do documento da pessoa", type=openapi.TYPE_STRING)
document_birth_date = openapi.Parameter(
    'document_birth_date', openapi.IN_QUERY, description="FORMAT: YYYY-MM-DD", type=openapi.FORMAT_DATE)
document_number = openapi.Parameter('document_number', openapi.IN_QUERY,
                                    description="param número do documento da pessoa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY,
                        description="param número do CPF da pessoa", type=openapi.TYPE_STRING)
nickname_label = openapi.Parameter(
    'nickname_label', openapi.IN_QUERY, description="param alcunha da pessoa", type=openapi.TYPE_STRING)
tattoo_label = openapi.Parameter('tattoo_label', openapi.IN_QUERY,
                                 description="param tatuagem da pessoa", type=openapi.TYPE_STRING)
entity_name = openapi.Parameter('entity_name', openapi.IN_QUERY,
                                description="param Unidade do usuário", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class PersonByCpfViewSet(generics.ListAPIView):
    queryset = Person.objects.all()
    # serializer_class = serializers.PersonSerializer
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:person_advanced').exists():
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_intermediate').exists():
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_basic').exists():
            return serializers.PersonSerializer
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
            person_cortex = helpers_cortex.process_cortex_consult(
                username=request.user.username, cpf=cpf)
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
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    queryset = Person.objects.all()

    def get_serializer_class(self):            
        if self.request.user.groups.filter(name__in=['profile:person_intermediate', 'profile:person_advanced', 'profile:person_basic']).exists():
            if self.request.method == 'POST':
                return serializers.PersonSerializer
            else:
                return list_serializers.PersonListSerializer
        else:
            raise PermissionDenied

    @action(detail=True, methods=['GET'], permission_classes=DjangoModelPermissions)
    def list(self, request, *args, **kwargs):
        probable_cpf = self.request.query_params.get('document_number')
        try:
            if probable_cpf:
                cpf = base_helpers.validate_cpf(probable_cpf)
                print(cpf)
                if cpf:
                    person_cortex = helpers_cortex.process_cortex_consult(
                        username=request.user.username, cpf=cpf)
                    if person_cortex:
                        documents = helpers_cortex.validate_document(cpf)
                        if documents is None:
                            helpers_cortex.create_person_and_document(
                                person_cortex)
                        else:
                            helpers_cortex.update_registers(
                                documents=documents, person_cortex=person_cortex)
                    helpers_bnmp.process_bnmp_consult(
                        username=request.user.username, cpf=cpf)
        except Exception as e:
            logger.warning('CPF not Found - {}'.format(e))
        try:
            queryset = self.get_queryset().filter(
                self.build_filter_conditions()
            )
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error('Error while getting person bacinf - {}'.format(e))
            raise ValidationError(e)        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)

    def perform_create(self, serializer):
        with transaction.atomic():
            try:
                user = self.request.user
                military = Military.objects.get(cpf=user.username)
                entity = Entity.objects.get(id=military.entity.id)
                instance = serializer.save(created_by=user, entity=entity)

                self.update_related_objects(instance, entity, user)

                assign_perm("change_person", user, instance)
                assign_perm("delete_person", user, instance)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.warn('Warning while saving person - {}'.format(e))
                transaction.set_rollback(True)
                raise e

    def update_related_objects(self, instance, entity, user):
        for related_object in ['nicknames', 'tattoos', 'addresses', 'physicals', 'documents', 'faces', 'images']:
            logger.info('Info object - {}'.format(related_object))
            for related_instance in getattr(instance, related_object).all():
                object_name = type(related_instance).__name__.lower()
                print(object_name)
                related_instance.entity = entity
                related_instance.created_by = user
                related_instance.save()
                assign_perm("change_{}".format(object_name),
                            user, related_instance)
                assign_perm("delete_{}".format(object_name),
                            user, related_instance)
                if related_object == 'documents' and related_instance.type.label == 'CPF':
                    try:
                        cpf = base_helpers.validate_cpf(
                            value=related_instance.number)
                        helpers.process_cortex_consult(
                            username=self.request.user.username, cpf=cpf, person=instance)
                        helpers.process_bnmp_consult(
                            username=self.request.user.username, cpf=cpf, person=instance)
                    except ValidationError as e:
                        logger.warn('Warning CPF is no valid - {}'.format(e))
                if related_object == 'documents':
                    for image in related_instance.images.all():
                        image.entity = entity
                        image.created_by = user
                        image.save()
                        assign_perm("change_documentimage", user, image)
                        assign_perm("delete_documentimage", user, image)

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

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return Response({"detail": "Erro na validação dos dados. {}".format(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        if isinstance(exc, ObjectDoesNotExist):
            return Response({"detail": "Objeto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

    def build_filter_conditions(self):
        logger.info('No filtro personalizado - {}'.format(self.request.user))
        filters = Q()
        query_params = self.request.query_params
        try:
            my_param = query_params.get('my')
            #logger.info('Meus cadastros - {}'.format(my_param))

            filters &= Q(created_by=self.request.user) if my_param is not None or self.request.user.groups.filter(name='profile:person_basic').exists() else Q()

            query_dict = {'address_city': 'addresses__city', 'address_neighborhood': 'addresses__neighborhood', 'address_street': 'addresses__street',
                        'address_complement': 'addresses__complement', 'address_reference': 'addresses__reference', 'address_zipcode': 'addresses__zipcode',
                        'document_name': 'documents__name', 'document_mother': 'documents__mother', 'document_father': 'documents__father',
                        'document_birth_date': 'documents__birth_date', 'document_number': 'documents__number', 'nickname_label': 'nicknames__label',
                        'tattoo_label': 'tattoos__label', 'entity_name': 'entity__name'}

            for field, flag in query_dict.items():
                if value := query_params.get(field):
                    q = Q(**{f"{flag}__iexact": value}) if field in ['document_number', 'document_birth_date'] else Q(
                        **{f"{flag}__unaccent__icontains": value})
                    filters &= q
            logger.info('Query_filter - {}'.format(filters))
            return filters
        except Exception as e:
             logger.Error('Exception - {}'.format(e))
             raise e


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
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_basic').exists():
            return serializers.PersonSerializer
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
                    instance = serializer.save(
                        person=person, entity=entity, created_by=user)
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
                    instance = serializer.save(
                        person=person, entity=entity, created_by=user)
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
                    instance = serializer.save(
                        person=person, entity=entity, created_by=user)
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
                    instance = serializer.save(
                        person=person, entity=entity, created_by=user)
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
                        image.entity = entity
                        image.created_by = user
                        image.save()
                        assign_perm("change_documentimage",
                                    self.request.user, image)
                        assign_perm("delete_documentimage",
                                    self.request.user, image)
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
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
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
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
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
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
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
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
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
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
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

        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
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

        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
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
