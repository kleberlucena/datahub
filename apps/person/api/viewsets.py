from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.person.api.serializers import *
from apps.person.models import *


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
    