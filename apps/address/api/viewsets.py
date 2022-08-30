from rest_framework import generics, mixins, permissions, viewsets
from rest_framework_gis import filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from guardian.shortcuts import assign_perm

from apps.address.services import get_address_by_zipcode
from apps.address.models import Address
from apps.address.api.serializers import AddressSerializer


class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        new_address = get_address_by_zipcode(self.request.data['zipcode'])
        print(new_address)
        if serializer.is_valid():
            instance = serializer.save(created_by=self.request.user)
            assign_perm("change_address", self.request.user, instance)
            assign_perm("delete_address", self.request.user, instance)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class AddressRetrieve(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Address, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

