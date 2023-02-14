from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user, get_perms, get_groups_with_perms
import logging

from apps.vehicle.api.v1.serializers import VehicleCortexSerializer, IntermediateVehicleCortexSerializer, BasicVehicleCortexSerializer
from apps.vehicle.models import VehicleCortex
from apps.vehicle import helpers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VehicleByPlacaViewSet(generics.GenericAPIView):
    serializer_class = VehicleCortexSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_intermediate').exists():
            return IntermediateVehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_basic').exists():
            return BasicVehicleCortexSerializer
        raise Http404

    def get_queryset(self):
        """
        Optionally restricts the returned person_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_person to a given document,
        by filtering against a `document_name` or a `document_number` query parameter in the URL.
        """
        queryset = VehicleCortex.objects.all() 
        return queryset

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, placa):
        username = request.user.username
        vehicle_cortex = None

        try:
            vehicle_cortex = helpers.process_cortex_consult(username=username, placa=placa.upper())
            
        except Exception as e:
            logger.error('Error while process_cortex_consult vehicle_cortex - {}'.format(e))
        try:
            """  instance = get_object_or_404(VehicleCortex, placa=placa.upper())
            serializer = self.get_serializer()
            if serializer is None:
                return HttpResponseForbidden()
            else:
                serializer.serialize(instance)
                return Response(serializer.data) """
            instance = get_object_or_404(VehicleCortex, placa=placa.upper())
            serializer = self.get_serializer(instance)

            return Response(serializer.data)
        except (TypeError, AttributeError):
                return Response(HttpResponseForbidden)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=500)