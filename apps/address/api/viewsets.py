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
    
    
    # def retrieve(self, request, *args, **kwargs):
    #     instance = Address.objects.get(uuid=kwargs['uuid'])
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


# class AddressViewSet(viewsets.ModelViewSet):
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)

#     def perform_destroy(self, instance):
#         user = self.request.user
#         instance.soft_delete_policy_action(user)


# class VisitViewSet(viewsets.ModelViewSet):
#     bbox_filter_field = "place"
#     filter_backends = (filters.InBBoxFilter,)
#     queryset = Visit.objects.all()
#     serializer_class = VisitSerializer

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

#     def perform_update(self, serializer):
#         serializer.save(updated_by=self.request.user)

#     def perform_destroy(self, instance):
#         user = self.request.user
#         instance.soft_delete_policy_action(user)
