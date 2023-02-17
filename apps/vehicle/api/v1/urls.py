from django.urls import path

from apps.vehicle.api.v1 import viewsets

app_name = 'apps.vehicle'

urlpatterns = [
    path('', viewsets.AddVehicleListView.as_view(), name='vehicle_json'),
    path('<uuid:uuid>/', viewsets.VehicleRetrieveDestroyView.as_view(), name='retrieve_json'),
    path('<uuid:uuid>/owner/', viewsets.VehicleAddOwnerView.as_view(), name='add_owner_json'),
    path('<uuid:uuid>/custodian/', viewsets.VehicleAddCustodianView.as_view(), name='add_custodian_json'),
    path('<uuid:uuid>/renter/', viewsets.VehicleAddRenterView.as_view(), name='add_renter_json'),
    path('placa/<str:placa>/', viewsets.VehicleByPlacaViewSet.as_view(), name='vehicle_by_placa_json'),
]