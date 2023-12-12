
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, RedirectView, DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework import generics, filters
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from . import models, tasks, services
from apps.portal.api.v1 import serializers


class EntityListJson(BaseDatatableView):
    max_display_length = 100
    model = models.Entity
    columns = ['id', 'name', 'child_exists', 'category', 'hierarchy', 'created_at',
               'updated_at']
    # permission_required = 'entity.view_entity'


class EntityListView(TemplateView):
    template_name = 'entity_list.html'
    # teste.delay()
    # permission_required = 'entity.view_entity'


class ComandosAPIPortalView(TemplateView):
    template_name = 'command_portal.html'


class MilitaryListJson(BaseDatatableView):
    max_display_length = 100
    model = models.Military
    columns = ['id', 'rank', 'register', 'nickname', 'name',
               'cpf', 'activity_status', 'unidade']

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'rank':
            rank = models.Promotion.objects.filter(military=row.id).last()
            row.rank = rank.rank
            return row.rank

        if column == 'unidade':
            unit = models.HistoryTransfer.objects.filter(military=row.id).last()
            row.unidade = unit.entity.name
            return row.unidade

        return super(MilitaryListJson, self).render_column(row, column)


class MilitaryListView(TemplateView):
    template_name = 'military_list.html'


class MilitaryProfileView(DetailView):
    template_name = 'profile.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        object = get_object_or_404(models.Military, id=id_)
        promotions = models.Promotion.objects.filter(military=id_)
        object.rankActual = promotions.latest('created_at')
        object.promotions = promotions

        histories = models.HistoryTransfer.objects.filter(
            military=id_)
        object.histories = histories
        object.unitActual = histories.latest('created_at').entity.name

        return object


class SearchMilitaryView(TemplateView):
    template_name = 'search_military.html'


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
    queryset = models.Military.objects.all()

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
                    filters |= q
            logger.info('Query_filter - {}'.format(filters))
            return filters
        except Exception as e:
             logger.Error('Exception - {}'.format(e))
             raise e