from django.urls import path

from apps.alert.api.v1.viewsets import *

app_name = 'apps.alert'

urlpatterns = [
    # Alertas
    # http://localhost:8000/api/v1/alert/cortex/
    path('cortex/', AddVehicleAlertCortexListView.as_view(), name='add_list_cortex_alert'),
]