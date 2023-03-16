from django.http import HttpResponse, Http404
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, mixins, status
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm, get_objects_for_user
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from apps.portal.models import Entity, Military
from base.models import Suggestion
from . import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AddSuggestionView(generics.ListCreateAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = serializers.SuggestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']

    @action(detail=True, methods=['GET'], permission_classes=DjangoObjectPermissions)
    def list(self, request, *args, **kwargs):
        self.permission_classes = [DjangoModelPermissions]
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def perform_create(self, serializer):
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = self.request.user
                    military = Military.objects.get(cpf=user.username)
                    entity = Entity.objects.get(id=military.entity.id)
                    instance = serializer.save(entity=entity, created_by=user)
                    assign_perm("change_suggestion", self.request.user, instance)
                    assign_perm("delete_suggestion", self.request.user, instance)
                    return Response(serializer.data, status=201)
            except Exception as e:
                logger.warn('Warning while save Suggestion - {}'.format(e))
                transaction.set_rollback(True)
                return Response(status=403)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @swagger_auto_schema(method='post')
    @action(detail=True, methods=['POST'])
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Optionally restricts the returned suggestion_list to a given user,
        by filtering against a `username` query parameter in the URL.
        Optionally restricts the returned list_suggestion to a given user creator,
        """
        queryset = Suggestion.objects.all()
        my = self.request.query_params.get('my')
        has_my = Q()
        if my is not None:
            has_my = Q(created_by=self.request.user)
        return queryset.filter(has_my)



class SuggestionUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = serializers.SuggestionSerializer
    permission_classes = [DjangoObjectPermissions]

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Suggestion, uuid=kwargs['uuid'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Suggestion, uuid=kwargs['uuid'])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=self.request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=422)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Suggestion, uuid=kwargs['uuid'])
        user = self.request.user
        if user.has_perm('base.delete_suggestion', instance):
            instance.soft_delete_cascade_policy_action(deleted_by=user)
            return Response('Success', status=204)
        else:
            return Response('Unauthorized', status=401)