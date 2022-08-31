from rest_framework import generics, viewsets, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from guardian.shortcuts import assign_perm

from apps.person.api.serializers import *
from apps.person.models import *


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoObjectPermissions]

    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def perform_create(self, serializer):
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

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user
        instance.soft_delete_policy_action(user)


class PersonList(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class AddPersonListView(generics.ListCreateAPIView):
    permission_classes = [DjangoObjectPermissions]
    serializer_class = PersonSerializer

    queryset = Person.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned person_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_person to a given document,
        by filtering against a `document_name` or a `document_number` query parameter in the URL.
        """
        queryset = Person.objects.all()
        my = self.request.query_params.get('my')
        document_name = self.request.query_params.get('document_name')
        document_number = self.request.query_params.get('document_number')
        if document_number is not None:
            queryset = queryset.filter(documents__number__startswith=document_number)
        if document_name is not None:
            queryset = queryset.filter(documents__name__startswith=document_name)
        if my is not None:
            queryset = queryset.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
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
        return Response(serializer.errors, status=400)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete_policy_action(self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)


class PersonRetrieveView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = Person.objects.get(uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PersonAddFaceView(CreateModelMixin, generics.GenericAPIView):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_face", self.request.user, instance)
            assign_perm("delete_face", self.request.user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddTattooView(CreateModelMixin, generics.GenericAPIView):
    queryset = Tattoo.objects.all()
    serializer_class = TattooSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_tattoo", self.request.user, instance)
            assign_perm("delete_tattoo", self.request.user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddNicknameView(CreateModelMixin, generics.GenericAPIView):
    queryset = Nickname.objects.all()
    serializer_class = NicknameSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_nickname", self.request.user, instance)
            assign_perm("delete_nickname", self.request.user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddPhysicalView(CreateModelMixin, generics.GenericAPIView):
    queryset = Physical.objects.all()
    serializer_class = PhysicalSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        person = get_object_or_404(Person, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            instance = serializer.save(person=person, created_by=self.request.user)
            assign_perm("change_physical", self.request.user, instance)
            assign_perm("delete_physical", self.request.user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddDocumentView(CreateModelMixin, generics.GenericAPIView):
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
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonAddAddressView(CreateModelMixin, generics.GenericAPIView):
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


class PersonAddImageView(CreateModelMixin, generics.GenericAPIView):
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
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# view to Update attributes of person

class FaceUpdateView(generics.UpdateAPIView):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer
    permission_classes = [DjangoObjectPermissions]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Face, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class TattooUpdateView(generics.UpdateAPIView):
    queryset = Tattoo.objects.all()
    serializer_class = TattooSerializer
    permission_classes = [DjangoObjectPermissions]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Tattoo, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class NicknameUpdateView(generics.UpdateAPIView):
    queryset = Nickname.objects.all()
    serializer_class = NicknameSerializer
    permission_classes = [DjangoObjectPermissions]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Nickname, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class PhysicalUpdateView(generics.UpdateAPIView):
    queryset = Physical.objects.all()
    serializer_class = PhysicalSerializer
    permission_classes = [DjangoObjectPermissions]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Physical, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class DocumentUpdateView(generics.UpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DjangoObjectPermissions]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Document, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class AddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [DjangoObjectPermissions]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Address, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ImageUpdateView(generics.UpdateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [DjangoObjectPermissions]

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Image, uuid=kwargs['uuid'])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)




