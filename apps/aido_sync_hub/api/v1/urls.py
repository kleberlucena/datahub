from django.urls import path
from apps.aido_sync_hub.api.v1 import viewsets

app_name = 'aido_sync_hub'


urlpatterns = [
    path('update/', viewsets.SyncAPIView.as_view(), name='sync_update'),
]