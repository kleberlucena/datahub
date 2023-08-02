from rest_framework.response import Response
from rest_framework import generics, permissions

from apps.image.api.serializers import *
from apps.image.models import *
from apps.portal.models import Entity, Military


class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            military = Military.objects.get(cpf=user.username)
            entity = Entity.objects.get(id=military.entity.id)
            instance = serializer.save(entity=entity, created_by=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ImageRetrieve(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = Image.objects.get(uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)