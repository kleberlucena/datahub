from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user, get_perms, get_groups_with_perms
import logging

from apps.vehicle.api.v1.serializers import VehicleCortexSerializer, VehicleIntermediateCortexSerializer, VehicleBasicCortexSerializer
from apps.vehicle.models import VehicleCortex
from apps.vehicle import helpers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VehicleByPlacaViewSet(generics.GenericAPIView):
    queryset = VehicleCortex.objects.all()
    permission_classes = [DjangoModelPermissions, DjangoObjectPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='cortex_vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='cortex_vehicle_intermediate').exists():
            return VehicleIntermediateCortexSerializer
        return VehicleBasicCortexSerializer            


    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, placa):
        username = request.user.username
        vehicle_cortex = None

        try:
            vehicle_cortex = helpers.process_cortex_consult(username=username, placa=placa.upper())
            """ documents = helpers.validate_document(number=cpf)
            if documents is None or len(documents) == 0:
                print('sem documentos')
                helpers.create_person_and_document(vehicle_cortex)
            else:
                print('Com documentos')
                 helpers.update_registers(documents, vehicle_cortex) """
        except Exception as e:
            logger.error('Error while process_cortex_consult vehicle_cortex - {}'.format(e))
        try:
            instance = get_object_or_404(VehicleCortex, placa=placa.upper())
            perms = get_groups_with_perms(VehicleCortex)
            print(perms)
            print("instance - {}".format(instance))
            serializer = self.get_serializer(instance)
            return Response(serializer.data)    
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=500)