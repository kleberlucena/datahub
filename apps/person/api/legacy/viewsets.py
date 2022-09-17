from rest_framework import generics
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm
from . import serializers
from apps.person.models import *


class AddPersonView(generics.CreateAPIView):
    serializer_class = serializers.PersonLegacySerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.kwargs['username'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])

        if serializer.is_valid():
            instance = serializer.save(created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            nicknames = instance.nicknames.all()
            for nickname in nicknames:
                nickname.created_by = user
                nickname.save()
                assign_perm("change_nickname", user, nickname)
                assign_perm("delete_nickname", user, nickname)
            for tattoo in instance.tattoos.all():
                tattoo.created_by = user
                tattoo.save()
                assign_perm("change_tattoo", user, tattoo)
                assign_perm("delete_tattoo", user, tattoo)
            for address in instance.addresses.all():
                address.created_by = user
                address.save()
                assign_perm("change_address", user, address)
                assign_perm("delete_address", user, address)
            for physical in instance.physicals.all():
                physical.created_by = user
                physical.save()
                assign_perm("change_physical", user, physical)
                assign_perm("delete_physical", user, physical)
            for document in instance.documents.all():
                document.created_by = user
                document.save()
                assign_perm("change_document", user, document)
                assign_perm("delete_document", user, document)
            for face in instance.faces.all():
                face.created_by = user
                face.save()
                assign_perm("change_face", user, face)
                assign_perm("delete_face", user, face)
            for image in instance.images.all():
                image.created_by = user
                image.save()
                assign_perm("change_image", user, image)
                assign_perm("delete_image", user, image)
            assign_perm("change_person", user, instance)
            assign_perm("delete_person", user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddFaceView(CreateModelMixin, generics.GenericAPIView):
    queryset = Face.objects.all()
    serializer_class = serializers.FaceLegacySerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.kwargs['username'])
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])

        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            assign_perm("change_face", user, instance)
            assign_perm("delete_face", user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddTattooView(CreateModelMixin, generics.GenericAPIView):
    queryset = Tattoo.objects.all()
    serializer_class = serializers.TattooLegacySerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            assign_perm("change_tattoo", user, instance)
            assign_perm("delete_tattoo", user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddNicknameView(CreateModelMixin, generics.GenericAPIView):
    queryset = Nickname.objects.all()
    serializer_class = serializers.NicknameLegacySerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            assign_perm("change_nickname", user, instance)
            assign_perm("delete_nickname", user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddPhysicalView(CreateModelMixin, generics.GenericAPIView):
    queryset = Physical.objects.all()
    serializer_class = serializers.PhysicalLegacySerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            assign_perm("change_physical", user, instance)
            assign_perm("delete_physical", user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddDocumentView(CreateModelMixin, generics.GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = serializers.DocumentLegacySerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])
        if serializer.is_valid():
            instance = serializer.save(created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            person.documents.add(instance)
            assign_perm("change_document", user, instance)
            assign_perm("delete_document", user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddAddressView(CreateModelMixin, generics.GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = serializers.AddressLegacySerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])
        if serializer.is_valid():
            instance = serializer.save(created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            person.addresses.add(instance)
            assign_perm("change_address", user, instance)
            assign_perm("delete_address", user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddImageView(CreateModelMixin, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = serializers.ImageLegacySerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        user = get_object_or_404(User, uuid=self.kwargs['username'])
        created_at = str(self.request.data['created_at'])
        updated_at = str(self.request.data['updated_at'])
        if serializer.is_valid():
            instance = serializer.save(created_by=user)
            instance.created_at = created_at
            instance.updated_at = updated_at
            instance.save()
            person.images.add(instance)
            assign_perm("change_image", user, instance)
            assign_perm("delete_image", user, instance)
            person.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)