from django.urls import path
from global_login_required import login_not_required

from apps.address.views import *
from apps.address.api import viewsets

app_name = 'apps.address'

urlpatterns = [
    path('', viewsets.AddressList.as_view(), name='list_json'),
    path('<uuid:uuid>/', viewsets.AddressRetrieve.as_view(), name='address_detail'),
]
