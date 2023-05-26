import logging
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from guardian.shortcuts import assign_perm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.address.api.serializers import AddressSerializer
from apps.document.api.serializers import DocumentSerializer
from apps.image.api.serializers import ImageSerializer
from apps.address.models import Address
from apps.document.models import Document
from apps.image.models import Image
from apps.portal.models import Entity, Military
from ...models import CharacteristicType, VTR, PoliceTeam, PoliceReport, InvolvedPerson
from .serializers import CharacteristicTypeSerializer, VTRSerializer, PoliceTeamSerializer, PoliceReportSerializer, InvolvedPersonSerializer, PersonalCharacteristicSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)

INVOLVED_CHOICES = [
    ('requesters', 'requesters'),
    ('victims', 'victims'),
    ('suspects', 'suspects'),
    ('witnesses', 'witnesses'),
]


class CharacteristicTypeListViewSet(generics.ListAPIView):
    queryset = CharacteristicType.objects.all()
    serializer_class = CharacteristicTypeSerializer

    @swagger_auto_schema(method='get')
    @action(detail=True, methods=['GET'])
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class VTRViewSet(viewsets.ModelViewSet):
    queryset = VTR.objects.all()
    serializer_class = VTRSerializer


class PoliceTeamViewSet(viewsets.ModelViewSet):
    queryset = PoliceTeam.objects.all()
    serializer_class = PoliceTeamSerializer


class PoliceReportViewSet(viewsets.ModelViewSet):
    queryset = PoliceReport.objects.all()
    serializer_class = PoliceReportSerializer


class PoliceReportRetrieveViewSet(generics.RetrieveUpdateAPIView):
    queryset = PoliceReport.objects.all()
    permission_classes = [DjangoObjectPermissions]
    serializer_class = PoliceReportSerializer
    # for key
    lookup_field = 'uuid'

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'])
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(PoliceReport, uuid=kwargs['uuid'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize PoliceReport - {}'.format(e))
            return Response(status=403)


class PoliceReportAddInvolvedPersonViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = InvolvedPerson.objects.all()
    serializer_class = InvolvedPersonSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        police_report = get_object_or_404(
            PoliceReport, uuid=self.kwargs['uuid'])
        involved_type = self.kwargs['involved_type']
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
                        assign_perm("change_image",
                                    self.request.user, image)
                        assign_perm("delete_image",
                                    self.request.user, image)
                    police_report[involved_type].add(instance)
                    assign_perm("change_involvedperson",
                                self.request.user, instance)
                    assign_perm("delete_involvedperson",
                                self.request.user, instance)
                    police_report.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save InvolvedPerson - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class InvolvedPersonViewSet(viewsets.ModelViewSet):
    queryset = InvolvedPerson.objects.all()
    serializer_class = InvolvedPersonSerializer


class InvolvedPersonRetrieveViewSet(generics.RetrieveUpdateAPIView):
    queryset = InvolvedPerson.objects.all()
    permission_classes = [DjangoObjectPermissions]
    serializer_class = InvolvedPersonSerializer
    # for key
    lookup_field = 'uuid'

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'])
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(InvolvedPerson, uuid=kwargs['uuid'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize InvolvedPerson - {}'.format(e))
            return Response(status=403)


class InvolvedPersonAddDocumentViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        involved_person = get_object_or_404(
            InvolvedPerson, uuid=self.kwargs['uuid'])
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
                    involved_person.documents.add(instance)
                    assign_perm("change_document", self.request.user, instance)
                    assign_perm("delete_document", self.request.user, instance)
                    involved_person.save()
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


class InvolvedPersonAddAddressViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        involved_person = get_object_or_404(
            InvolvedPerson, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(entity=entity, created_by=user)
                    involved_person.addresses.add(instance)
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


class InvolvedPersonAddImageViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        involved_person = get_object_or_404(
            InvolvedPerson, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(entity=entity, created_by=user)
                    involved_person.images.add(instance)
                    assign_perm("change_image", self.request.user, instance)
                    assign_perm("delete_image", self.request.user, instance)
                    involved_person.save()
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


class InvolvedPersonAddPersonalCharacteristicViewSet(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = PersonalCharacteristicSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def perform_create(self, serializer):
        involved_person = get_object_or_404(
            InvolvedPerson, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(entity=entity, created_by=user)
                    involved_person.personal_characteristics.add(instance)
                    assign_perm("change_personalcharacteristic",
                                self.request.user, instance)
                    assign_perm("delete_personalcharacteristic",
                                self.request.user, instance)
                    involved_person.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn(
                    'Warning while save personal_characteristic - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
