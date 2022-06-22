from rest_framework import generics, permissions

from apps.image.api.serializers import *
from apps.image.models import *


class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    