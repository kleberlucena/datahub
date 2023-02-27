from django.urls import path

from apps.vehicle.api.v1 import viewsets

app_name = 'apps.vehicle'

urlpatterns = [
    path('', viewsets.AddVehicleListView.as_view(), name='vehicle_json'),
    path('<uuid:uuid>/', viewsets.VehicleRetrieveUpdateDestroyView.as_view(), name='retrieve_json'),
    path('<uuid:uuid>/owner/', viewsets.VehicleAddOwnerView.as_view(), name='add_owner_json'),
    path('<uuid:uuid>/custodian/', viewsets.VehicleAddCustodianView.as_view(), name='add_custodian_json'),
    path('<uuid:uuid>/renter/', viewsets.VehicleAddRenterView.as_view(), name='add_renter_json'),
    path('placa/<str:placa>/', viewsets.VehicleByPlacaViewSet.as_view(), name='vehicle_by_placa_json'),
    path('chassi/<str:chassi>/', viewsets.VehicleByChassiViewSet.as_view(), name='vehicle_by_chassi_json'),
    path('renavam/<str:renavam>/', viewsets.VehicleByRenavamViewSet.as_view(), name='vehicle_by_renavam_json'),
    path('motor/<str:motor>/', viewsets.VehicleByMotorViewSet.as_view(), name='vehicle_by_motor_json'),
    path('cpf/<str:cpf>/', viewsets.VehicleByCPFViewSet.as_view(), name='vehicle_by_cpf_json'),
]