from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, mixins, status
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response
from rest_framework.decorators import action
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, get_objects_for_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.person.api.v1 import serializers, list_serializers
from apps.address.api.serializers import AddressSerializer
from apps.image.api.serializers import ImageSerializer
from apps.document.api.serializers import DocumentSerializer
from apps.person.models import *
from apps.person import helpers, tasks
from apps.cortex import helpers as helpers_cortex
from apps.cortex.models import PersonCortex
import logging


document_name = openapi.Parameter('document_name', openapi.IN_QUERY, description="param nome do documento da pessoa", type=openapi.TYPE_STRING)
document_number = openapi.Parameter('document_number', openapi.IN_QUERY, description="param número do documento da pessoa", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY, description="param número do CPF da pessoa", type=openapi.TYPE_STRING)
nickname_label = openapi.Parameter('nickname_label', openapi.IN_QUERY, description="param alcunha da pessoa", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class PersonByCpfViewSet(generics.ListAPIView):
    queryset = Person.objects.all()
    #serializer_class = serializers.PersonSerializer
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]

    def get_serializer_class(self):
        print(self.request.user.groups)
        if self.request.user.groups.filter(name='profile:person_advanced').exists():
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_intermediate').exists():
            return serializers.IntermediatePersonSerializer
        return serializers.BasicPersonSerializer 

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
        print(cpf)
        try:
            person_cortex = helpers_cortex.process_cortex_consult(username=request.user.username, cpf=cpf)
            documents = helpers_cortex.validate_document(number=cpf)
            if documents is None or len(documents) == 0:
                print('sem documentos')
                helpers_cortex.create_person_and_document(person_cortex)
            else:
                print('Com documentos')
                helpers_cortex.update_registers(documents, person_cortex)
        except Exception as e:
            logger.error('Error while serialize person_cortex - {}'.format(e))
            return Response(status=500)
            """ unregistered_people_condition = ~Q(registers__system_label__contains='CORTEX PESSOA')
            unregistered_people = queryset.filter(unregistered_people_condition)
            if unregistered_people.exists():
                tasks.cortex_registry_list(username=request.user.username, person_list=unregistered_people, cpf=request.query_params.get('cpf')) """
        finally:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class AddPersonListView(generics.ListCreateAPIView):
    permission_classes = [DjangoObjectPermissions, DjangoModelPermissions]
    serializer_class = serializers.PersonSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    queryset = Person.objects.all()

    def get_serializer_class(self):
        print(self.request.user.groups)
        if self.request.method in ['POST']:
            return serializers.PersonSerializer
        elif self.request.user.groups.filter(name='profile:person_advanced').exists():
            return list_serializers.PersonListSerializer
        elif self.request.user.groups.filter(name='profile:person_intermediate').exists():
            return list_serializers.IntermediatePersonListSerializer
        return list_serializers.BasicPersonListSerializer 

    @action(detail=True, methods=['GET'], permission_classes=IsAdminUser)
    def list(self, request, *args, **kwargs):
        self.permission_classes = [DjangoModelPermissions]
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = get_objects_for_user(self.request.user, 'person.view_person')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        document_name = self.request.query_params.get('document_name')
        has_name = Q()
        document_number = self.request.query_params.get('document_number')
        has_number = Q()
        nickname_label = self.request.query_params.get('nickname_label')
        has_nickname = Q()
        if document_name is not None:
            has_name = Q(documents__name__icontains=document_name)
        if document_number is not None:
            has_number = Q(documents__number__icontains=document_number)
        if nickname_label is not None:
            has_nickname = Q(nicknames__label__icontains=nickname_label)
        if my is not None:
            has_my = Q(created_by=self.request.user)
        return queryset.filter(has_my & has_nickname & has_number & has_name)

    def perform_create(self, serializer):
        try:
            if serializer.is_valid():
                instance = serializer.save(created_by=self.request.user)
                nicknames = instance.nicknames.all()
                for nickname in nicknames:
                    nickname.created_by = self.request.user
                    nickname.save()
                    assign_perm("change_nickname", self.request.user, nickname)
                    assign_perm("delete_nickname", self.request.user, nickname)
                for tattoo in instance.tattoos.all():
                    tattoo.created_by = self.request.user
                    tattoo.save()
                    assign_perm("change_tattoo", self.request.user, tattoo)
                    assign_perm("delete_tattoo", self.request.user, tattoo)
                for address in instance.addresses.all():
                    address.created_by = self.request.user
                    address.save()
                    assign_perm("change_address", self.request.user, address)
                    assign_perm("delete_address", self.request.user, address)
                for physical in instance.physicals.all():
                    physical.created_by = self.request.user
                    physical.save()
                    assign_perm("change_physical", self.request.user, physical)
                    assign_perm("delete_physical", self.request.user, physical)
                for document in instance.documents.all():
                    document.created_by = self.request.user
                    document.save()
                    if document.type.label == 'CPF':
                        helpers.process_external_consult(id_person=instance.id, username=self.request.user.username, cpf=document.number)
                    assign_perm("change_document", self.request.user, document)
                    assign_perm("delete_document", self.request.user, document)
                for face in instance.faces.all():
                    face.created_by = self.request.user
                    face.save()
                    assign_perm("change_face", self.request.user, face)
                    assign_perm("delete_face", self.request.user, face)
                for image in instance.images.all():
                    image.created_by = self.request.user
                    image.save()
                    assign_perm("change_image", self.request.user, image)
                    assign_perm("delete_image", self.request.user, image)
                assign_perm("change_person", self.request.user, instance)
                assign_perm("delete_person", self.request.user, instance)
                return Response(serializer.data, status=201)
        except Exception as e:
            return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(method='get', manual_parameters=[document_name, document_number, nickname_label])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PersonRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Person.objects.all()
    permission_classes = [DjangoObjectPermissions]
    serializer_class = serializers.PersonSerializer
    # for key
    lookup_field = 'uuid'

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

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Person, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PersonAddFaceView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Face.objects.all()
    serializer_class = serializers.FaceSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_face", self.request.user, instance)
            assign_perm("delete_face", self.request.user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddTattooView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Tattoo.objects.all()
    serializer_class = serializers.TattooSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_tattoo", self.request.user, instance)
            assign_perm("delete_tattoo", self.request.user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddNicknameView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Nickname.objects.all()
    serializer_class = serializers.NicknameSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_nickname", self.request.user, instance)
            assign_perm("delete_nickname", self.request.user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddPhysicalView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Physical.objects.all()
    serializer_class = serializers.PhysicalSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_physical", self.request.user, instance)
            assign_perm("delete_physical", self.request.user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddDocumentView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(created_by=self.request.user)
            person.documents.add(instance)
            assign_perm("change_document", self.request.user, instance)
            assign_perm("delete_document", self.request.user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddAddressView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(created_by=self.request.user)
            person.addresses.add(instance)
            assign_perm("change_address", self.request.user, instance)
            assign_perm("delete_address", self.request.user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddImageView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(created_by=self.request.user)
            person.images.add(instance)
            assign_perm("change_image", self.request.user, instance)
            assign_perm("delete_image", self.request.user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# view to Update or Delete attributes of person

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
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Face, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('person.delete_face', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)


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
            return Response(serializer.errors, status=400)

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
            return Response(serializer.errors, status=400)

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
            return Response(serializer.errors, status=400)

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
            return Response(serializer.errors, status=400)

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
            return Response(serializer.errors, status=400)

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
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Image, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('image.delete_image', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)
