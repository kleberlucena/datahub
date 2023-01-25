from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
import logging

from apps.vehicle.api.v1.serializers import VehicleCortexSerializer
from apps.vehicle.models import VehicleCortex
from apps.vehicle import helpers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VehicleByPlacaViewSet(generics.GenericAPIView):
    queryset = VehicleCortex.objects.all()
    serializer_class = VehicleCortexSerializer

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'])
    def get(self, request, placa):
        username = request.user.username
        vehicle_cortex = None

        try:
            vehicle_cortex = helpers.process_cortex_consult(username=username, placa=placa)
            """ documents = helpers.validate_document(number=cpf)
            if documents is None or len(documents) == 0:
                print('sem documentos')
                helpers.create_person_and_document(vehicle_cortex)
            else:
                print('Com documentos')
                 helpers.update_registers(documents, vehicle_cortex) """
            instance = get_object_or_404(VehicleCortex, placa=placa)
            print("instance - {}".format(instance))
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=500)