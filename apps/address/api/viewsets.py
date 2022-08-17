from rest_framework import generics, mixins, permissions, viewsets
from rest_framework_gis import filters
from rest_framework.response import Response

from apps.address.models import Address
from apps.address.api.serializers import AddressSerializer


class AddressList(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    
    
class AddressRetrieve(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = Address.objects.get(uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

