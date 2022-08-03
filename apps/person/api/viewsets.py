from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response

from apps.person.api.serializers import *
from apps.person.models import *


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


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
    