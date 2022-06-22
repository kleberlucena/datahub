from rest_framework import generics, permissions

from apps.person.api.serializers import *
from apps.person.models import *


class PersonList(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]
    