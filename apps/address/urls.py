from django.urls import path
from global_login_required import login_not_required

from apps.address.views import *
from apps.address.api import viewsets

app_name = 'apps.address'

urlpatterns = [
    path('api-v1/', viewsets.AddressList.as_view(), name='list_json'),
    path('api-v1/<int:id>/', viewsets.AddressList.as_view(), name='retrieve_json'),
]
