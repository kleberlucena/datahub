from rest_framework import generics, viewsets, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.person.api.serializers import *
from apps.person.models import *


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user
        instance.soft_delete_policy_action(user)


class PersonList(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer
    

class PersonRetrieve(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = Person.objects.get(uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PersonAddFaceView(CreateModelMixin, generics.GenericAPIView):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.request.kwargs['uuid'])
        return serializer.save(person=person, created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddTatooView(CreateModelMixin, generics.GenericAPIView):
    queryset = Tatoo.objects.all()
    serializer_class = TatooSerializer

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.request.kwargs['uuid'])
        return serializer.save(person=person, created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddNicknameView(CreateModelMixin, generics.GenericAPIView):
    queryset = Nickname.objects.all()
    serializer_class = NicknameSerializer

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.request.kwargs['uuid'])
        return serializer.save(person=person, created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddPhysicalView(CreateModelMixin, generics.GenericAPIView):
    queryset = Physical.objects.all()
    serializer_class = PhysicalSerializer

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.request.kwargs['uuid'])
        return serializer.save(person=person, created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddDocumentView(CreateModelMixin, generics.GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.request.kwargs['uuid'])
        return serializer.save(person=person, created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddAddressView(CreateModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.request.kwargs['uuid'])
        return serializer.save(person=person, created_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


