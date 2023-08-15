from django.db.models import Q
from rest_framework import generics, status, generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from apps.radio.api.v1.serializers import GpsSerializer
from apps.radio.models import Gps

# Get an instance of a logger
logger = logging.getLogger(__name__)

created_at = openapi.Parameter('created_at', openapi.IN_QUERY,
                               description="FORMAT: YYYY-MM-DD", type=openapi.FORMAT_DATETIME)
location = openapi.Parameter('location', openapi.IN_QUERY,
                             description="param localização do endereço da pessoa", type=openapi.TYPE_STRING)
id = openapi.Parameter('id', openapi.IN_QUERY,
                       description="param id de um Rádio", type=openapi.TYPE_STRING)
timestamp = openapi.Parameter('timestamp', openapi.IN_QUERY,
                              description="FORMAT: YYYY-MM-DD", type=openapi.FORMAT_DATETIME)


class GpsViewSet(generics.ListCreateAPIView):
    queryset = Gps.objects.all().order_by('-created_at')
    serializer_class = GpsSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]
    ordering_fields = ['created_at', 'location', 'id', 'timestamp']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if self.request.user.groups.filter(name='radio:gps_add').exists():
                return GpsSerializer
            else:
                raise PermissionDenied
        elif self.request.user.groups.filter(name__icontains='radio:gps').exists():
            return GpsSerializer
        else:
            raise PermissionDenied

    @swagger_auto_schema(method='post', request_body=GpsSerializer)
    @action(detail=True, methods=['POST'])
    def create(self, request):
        if self.request.user.groups.filter(name='radio:gps_add').exists():
            serializer = GpsSerializer(
                data=request.data['locations'], many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied

    @swagger_auto_schema(method='get', manual_parameters=[created_at, location, id, timestamp])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        created_at = self.request.query_params.get('created_at')
        location = self.request.query_params.get('location')
        id = self.request.query_params.get('id')
        timestamp = self.request.query_params.get('timestamp')
        has_created_at = Q()
        has_location = Q()
        has_id = Q()
        has_timestamp = Q()
        if created_at is not None:
            has_created_at = Q(created_at__icontains=created_at)
        if location is not None:
            has_location = Q(location__icontains=location)
        if id is not None:
            has_id = Q(id__icontains=id)
        if timestamp is not None:
            has_timestamp = Q(timestamp__icontains=timestamp)

        queryset = queryset.filter(
            has_created_at, has_location, has_id, has_timestamp)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if serializer.data == []:
            raise NotFound
        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Você não tem permissão para acessar este recurso."}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(exc, NotFound):
            return Response({"detail": "Recurso não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)
