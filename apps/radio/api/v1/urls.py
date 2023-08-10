from django.urls import path
from apps.radio.api.v1 import viewsets

app_name = 'radio'

urlpatterns = [
    path('gps/', viewsets.GpsViewSet.as_view(), name='gps'),
]