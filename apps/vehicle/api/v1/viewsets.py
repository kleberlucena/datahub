from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics, filters, mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import DjangoObjectPermissions, DjangoModelPermissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from guardian.shortcuts import assign_perm
import logging

from apps.vehicle.api.v1.serializers import VehicleCortexSerializer, IntermediateVehicleCortexSerializer, BasicVehicleCortexSerializer, VehicleSerializer, BasicVehicleSerializer, IntermediateVehicleSerializer, VehicleUpdateSerializer, VehicleImageSerializer
from apps.vehicle.models import PersonRenavamCortex, VehicleCortex, Vehicle, VehicleImage
from apps.vehicle import helpers
from apps.person.api.v1.serializers import PersonSerializer
from apps.person.models import Person
from apps.portal.models import Entity, Military

signal = openapi.Parameter('signal', openapi.IN_QUERY, description="param signal do veículo", type=openapi.TYPE_STRING)
chassi = openapi.Parameter('chassi', openapi.IN_QUERY, description="param chassi do veículo", type=openapi.TYPE_STRING)
my = openapi.Parameter('my', openapi.IN_QUERY, description="param my pesquisa cadastros do usuário logado", type=openapi.TYPE_BOOLEAN)
cpf_owner = openapi.Parameter('cpf_owner', openapi.IN_QUERY, description="param número do CPF do proprietário", type=openapi.TYPE_STRING)
cpf_custodian = openapi.Parameter('cpf_custodian', openapi.IN_QUERY, description="param número do CPF do possuidor", type=openapi.TYPE_STRING)
cpf_renter = openapi.Parameter('cpf_renter', openapi.IN_QUERY, description="param número do CPF do arrendatário", type=openapi.TYPE_STRING)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class VehicleByCPFViewSet(generics.GenericAPIView):
    model = VehicleCortex
    serializer_class = VehicleCortexSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_intermediate').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_basic').exists():
            return BasicVehicleCortexSerializer
        raise Http404
    
    def get_queryset(self):
        queryset = VehicleCortex.objects.all() 
        return queryset

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, cpf):
        username = request.user.username
        vehicle_cortex = None
        try:
            vehicle_cortex = helpers.process_cortex_consult_by_cpf(username=username, cpf=cpf)
            
        except Exception as e:
            logger.error('Error while process_cortex_consult_by_cpf vehicle_cortex - {}'.format(e))
        try:
            serializer = self.get_serializer(vehicle_cortex, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=403)


class VehicleByMotorViewSet(generics.GenericAPIView):
    serializer_class = VehicleCortexSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_intermediate').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_basic').exists():
            return BasicVehicleCortexSerializer
        raise Http404

    def get_queryset(self):
        queryset = VehicleCortex.objects.all() 
        return queryset

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, motor):
        username = request.user.username
        vehicle_cortex = None

        try:
            helpers.process_cortex_consult(username=username, motor=motor.upper())
            
        except Exception as e:
            logger.error('Error while process_cortex_consult vehicle_cortex - {}'.format(e))
        try:
            vehicle_cortex = get_object_or_404(VehicleCortex, numeroMotor=motor.upper())
        except Exception as e:
            logger.error('Error while get vehicle_cortex - {}'.format(e))
        try:
            serializer = self.get_serializer(vehicle_cortex)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=403)


class VehicleByRenavamViewSet(generics.GenericAPIView):
    serializer_class = VehicleCortexSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_intermediate').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_basic').exists():
            return BasicVehicleCortexSerializer
        raise Http404

    def get_queryset(self):
        queryset = VehicleCortex.objects.all() 
        return queryset

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, renavam):
        username = request.user.username
        vehicle_cortex = None

        try:
            helpers.process_cortex_consult(username=username, renavam=renavam.upper())
            
        except Exception as e:
            logger.error('Error while process_cortex_consult vehicle_cortex - {}'.format(e))
        try:
            vehicle_cortex = get_object_or_404(VehicleCortex, renavam=renavam.upper())
        except Exception as e:
            logger.error('Error while get vehicle_cortex - {}'.format(e))
            return Response(status=400)
        try:
            serializer = self.get_serializer(vehicle_cortex)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=403)


class VehicleByChassiViewSet(generics.GenericAPIView):
    serializer_class = VehicleCortexSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_intermediate').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_basic').exists():
            return BasicVehicleCortexSerializer
        raise Http404

    def get_queryset(self):
        queryset = VehicleCortex.objects.all() 
        return queryset

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, chassi):
        username = request.user.username
        vehicle_cortex = None

        try:
            chassi = chassi.strip()
            helpers.process_cortex_consult(username=username, chassi=chassi.upper())
        except Exception as e:
            logger.error('Error while process_cortex_consult vehicle_cortex - {}'.format(e))
        try:
            vehicle_cortex = get_object_or_404(VehicleCortex, chassi=chassi.upper())
        except Exception as e:
            logger.error('Error while get vehicle_cortex - {}'.format(e))
            return Response(status=400)
        try:
            serializer = self.get_serializer(vehicle_cortex)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=403)


class VehicleByPlacaViewSet(generics.GenericAPIView):
    serializer_class = VehicleCortexSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='profile:vehicle_advanced').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_intermediate').exists():
            return VehicleCortexSerializer
        elif self.request.user.groups.filter(name='profile:vehicle_basic').exists():
            return BasicVehicleCortexSerializer
        raise Http404

    def get_queryset(self):
        queryset = VehicleCortex.objects.all() 
        return queryset

    @swagger_auto_schema()
    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def get(self, request, placa):
        username = request.user.username
        vehicle_cortex = None

        try:
            helpers.process_cortex_consult(username=username, placa=placa.upper())
            
        except Exception as e:
            logger.error('Error while process_cortex_consult vehicle_cortex - {}'.format(e))
        try:
            vehicle_cortex = get_object_or_404(VehicleCortex, placa=placa.upper())
        except Exception as e:
            logger.error('Error while get vehicle_cortex - {}'.format(e))
            return Response(status=400)
        try:
            serializer = self.get_serializer(vehicle_cortex)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize vehicle_cortex - {}'.format(e))
            return Response(status=403)


class VehicleUpdateView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = VehicleUpdateSerializer
    # for key
    lookup_field = 'uuid'

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Vehicle, uuid=kwargs['uuid'])
        data=request.data
        cpf_owner = None
        cpf_custodian = None
        cpf_renter = None
        
        try:
            cpf_owner=data.pop("cpf_owner")
        except:
            pass
        try:   
            cpf_custodian=data.pop("cpf_custodian")
        except:
            pass
        try:
            cpf_renter=data.pop("cpf_renter")
        except:
            pass
        serializer = self.serializer_class(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            self.perform_update(instance=instance, cpf_owner=cpf_owner, cpf_custodian=cpf_custodian, cpf_renter=cpf_renter)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)    

    def perform_update(self, instance, cpf_owner, cpf_custodian, cpf_renter):        
        if cpf_owner:
            owner = Person.objects.filter(documents__number=cpf_owner)
            instance.owner = owner[0]
        if cpf_custodian:
            custodian = Person.objects.filter(documents__number=cpf_custodian)
            instance.custodian = custodian[0]
        if cpf_renter:
            renter = Person.objects.filter(documents__number=cpf_renter)
            instance.renter = renter[0]
        instance.save()
        return instance
    

class VehicleRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = VehicleSerializer
    # for key
    lookup_field = 'uuid'

    def update(self, *args, **kwargs):
        dados = self.request.data

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Vehicle, uuid=self.kwargs['uuid'])
        user = self.request.user
        unauthorized = HttpResponse("Unauthorized", status=401)
        if user.has_perm('vehicle.delete_vehicle', instance):
            """ for image in instance.images.all():
                if not user.has_perm('image_vehicle.delete_image_vehicle', image):
                    return unauthorized """
            if instance.soft_delete_cascade_policy_action(deleted_by=user):
                return HttpResponse("Deleted", status=204)
            else:
                return HttpResponse("Deleting", status=202)
        else:
            return unauthorized

    @swagger_auto_schema(method='get')
    @action(detail=True, methods=['GET'])
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Vehicle, uuid=kwargs['uuid'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize Vehicle - {}'.format(e))
            return Response(status=403)


class VehicleAddOwnerView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        vehicle = get_object_or_404(Vehicle, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                instance = serializer.save(created_by=self.request.user)
                print(instance)
                assign_perm("change_person", self.request.user, instance)
                assign_perm("delete_person", self.request.user, instance)
                vehicle.owner=instance
                vehicle.save()
                return Response(serializer.data, status=201)
            except Exception as e:
                logger.error('Error while add Owner Vehicle - {}'.format(e))
                return Response(serializer.errors, status=500)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VehicleAddCustodianView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        vehicle = get_object_or_404(Vehicle, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                instance = serializer.save(created_by=self.request.user)
                assign_perm("change_person", self.request.user, instance)
                assign_perm("delete_person", self.request.user, instance)
                vehicle.custodian=instance
                vehicle.save()
                return Response(serializer.data, status=201)
            except Exception as e:
                logger.error('Error while add Custodian Vehicle - {}'.format(e))
                return Response(serializer.errors, status=500)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VehicleAddRenterView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [DjangoObjectPermissions]

    def perform_create(self, serializer):
        vehicle = get_object_or_404(Vehicle, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            try:
                instance = serializer.save(created_by=self.request.user)
                assign_perm("change_person", self.request.user, instance)
                assign_perm("delete_person", self.request.user, instance)
                vehicle.renter=instance
                vehicle.save()
                return Response(serializer.data, status=201)
            except Exception as e:
                logger.error('Error while add Renter Vehicle - {}'.format(e))
                return Response(serializer.errors, status=500)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AddVehicleListView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = VehicleSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    queryset = Vehicle.objects.all()

    def get_serializer_class(self):
        if self.request.user.groups.filter(name__icontains='profile:vehicle').exists():
            return VehicleSerializer
        raise Http404  

    @action(detail=True, methods=['GET'])
    def list(self, request, *args, **kwargs):
        #self.permission_classes = [DjangoModelPermissions]
        queryset = self.filter_queryset(self.get_queryset())
        # queryset = get_objects_for_user(self.request.user, 'person.view_person')
        try:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
        
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error('Error while serialize person - {}'.format(e))
            return Response(status=403)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error('Error while serialize vehicle - {}'.format(e))
            return Response(serializer.errors, status=422)

    def get_queryset(self):
        """
        Optionally restricts the returned vehicle_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_vehicle to a given signal,
        by filtering against a `signal` or a `chassi` query parameter in the URL.
        """
        queryset = Vehicle.objects.all()
        my = self.request.query_params.get('my')
        has_my = Q()
        signal = self.request.query_params.get('signal')
        has_signal = Q()
        chassi = self.request.query_params.get('chassi')
        has_chassi = Q()
        if signal is not None:
            has_signal = Q(signal__icontains=signal)
        if chassi is not None:
            has_chassi = Q(chassi__icontains=chassi)
        if my is not None:
            has_my = Q(created_by=self.request.user)
        return queryset.filter(has_my & has_signal & has_chassi)

    @transaction.atomic
    def perform_create(self, serializer):
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save()
                    instance.created_by=user
                    instance.entity=entity
                    if instance.signal:
                        helpers.process_cortex_consult(username=user.username, placa=instance.signal)
                        for image in instance.images.all():
                            image.created_by=user
                            image.entity=entity
                            image.save()
                            assign_perm("change_vehicleimage", self.request.user, image)
                            assign_perm("delete_vehicleimage", self.request.user, image)
                    assign_perm("change_vehicle", self.request.user, instance)
                    assign_perm("delete_vehicle", self.request.user, instance)
                    instance.save()
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Vehicle - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(method='get', manual_parameters=[signal, chassi, my])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

   
class VehicleAddImageView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [DjangoObjectPermissions]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        self.perform_create(self.get_serializer(data=request.data))

    def perform_create(self, serializer):
        vehicle = get_object_or_404(Vehicle, uuid=self.kwargs['uuid'])
        if serializer.is_valid():
            user = self.request.user
            military = Military.objects.get(cpf=user.username)
            entity = Entity.objects.get(id=military.entity.id)
            instance = serializer.save(vehicle=vehicle, entity=entity, created_by=user)
            assign_perm("change_vehicleimage", user, instance)
            assign_perm("delete_vehicleimage", user, instance)
            vehicle.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=422)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)