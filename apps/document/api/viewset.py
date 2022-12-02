from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.response import Response
from guardian.shortcuts import assign_perm
from django.shortcuts import get_object_or_404

from apps.document.models import Document, DocumentImage, DocumentType
from apps.document.api.serializers import DocumentSerializer, DocumentImageSerializer, DocumentTypeSerializer


class DocumentTypeListViewSet(generics.ListAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save(created_by=self.request.user)
            assign_perm("change_document", self.request.user, instance)
            assign_perm("delete_document", self.request.user, instance)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def perform_destroy(self, instance):
        user = self.request.user
        instance.soft_delete_cascade_policy_action(deleted_by=user)


class DocumentRetrieve(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = Document.objects.get(uuid=kwargs['uuid'])
        print(f"aqui {kwargs['uuid']}")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = DocumentImage.objects.all()
    serializer_class = DocumentImageSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete_policy_action(self.request.user)