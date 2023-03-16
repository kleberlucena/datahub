from django.urls import path

from .views import *

app_name = 'address'

urlpatterns = [
    path('api-v1/address_list_json/', AddressListJson.as_view(), name='address_list_json'),
    path('list_address/', AddressListView.as_view(), name='list_address'),
    path('task-address-api-entity/', TaskSetEntityFromAddressView.as_view(), name='task-address-api-entity'),
    path('command_address/', CommandsAPIAddressView.as_view(), name='command_address'),
]
