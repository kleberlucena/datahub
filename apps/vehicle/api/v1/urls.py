from django.urls import path

from apps.vehicle.api.v1 import viewsets

app_name = 'apps.vehicle'

urlpatterns = [
    path('placa/<str:placa>/', viewsets.VehicleByPlacaViewSet.as_view(), name='vehicle_by_placa_json'),
]