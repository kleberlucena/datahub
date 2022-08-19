from rest_framework.response import Response
from rest_framework import generics, permissions

from apps.image.api.serializers import *
from apps.image.models import *


class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ImageRetrieve(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = Image.objects.get(uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)