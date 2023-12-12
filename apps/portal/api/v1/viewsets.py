from django.http import HttpResponse, Http404
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, mixins, status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.decorators import action
from guardian.shortcuts import assign_perm
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.portal.models import Military
from apps.portal.api.v1 import serializers
from base import helpers as base_helpers
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

name = openapi.Parameter('name', openapi.IN_QUERY,
                                  description="param nome do militar", type=openapi.TYPE_STRING)
register = openapi.Parameter('register', openapi.IN_QUERY,
                                    description="param matrícula do militar", type=openapi.TYPE_STRING)
email = openapi.Parameter('email', openapi.IN_QUERY,
                                    description="param e-mail do militar", type=openapi.TYPE_STRING)
nickname = openapi.Parameter('nickname', openapi.IN_QUERY,
                                    description="param nome de guerra do militar", type=openapi.TYPE_STRING)
cpf = openapi.Parameter('cpf', openapi.IN_QUERY,
                        description="param número do CPF do militar", type=openapi.TYPE_STRING)


class MilitaryListView(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    queryset = Military.objects.all()

    def get_serializer_class(self):            
        if self.request.user.groups.filter(name__in=['portal:military']).exists():
            return serializers.MilitarySerializer
        else:
            raise PermissionDenied

    @swagger_auto_schema(method='get',
                         manual_parameters=[
                                            name,
                                            cpf,
                                            register,
                                            email,
                                            nickname])
    @action(detail=True, methods=['GET'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=['GET'], permission_classes=DjangoModelPermissions)
    def list(self, request, *args, **kwargs):
        try:
            # Retrieve the parameter from the request
            term = request.query_params.get('term')

            queryset = self.get_queryset().filter(
                self.build_filter_conditions(term)
            )
            queryset = self.get_queryset().filter(
                self.build_filter_conditions()
            )
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            logger.error('Error while getting military - {}'.format(e))
            raise ValidationError(e)
        
    def build_filter_conditions(self,term):
        logger.info('No filtro personalizado - {}'.format(self.request.user))
        filters = Q()
        query_params = self.request.query_params
        try:
            # TODO atualizar parâmetros
            query_dict = {'name':  'name', 'cpf': 'cpf', 'nickname': 'nickname', 'register': 'register', 'email': 'email'}

            for field, flag in query_dict.items():
                if value := query_params.get(field):
                    q = Q(**{f"{flag}__icontains": value}) if field in ['cpf', 'register'] else Q(
                        **{f"{flag}__unaccent__icontains": value})
                    filters &= q
                elif term:
                    q = Q(**{f"{flag}__icontains":term}) if field in ['cpf', 'register'] else Q(
                        **{f"{flag}__unaccent__icontains":term})
                    filters &= q
            logger.info('Query_filter - {}'.format(filters))
            return filters
        except Exception as e:
             logger.Error('Exception - {}'.format(e))
             raise e