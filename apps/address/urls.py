from django.urls import path

from apps.address.views import *
from apps.address.api import viewsets

app_name = 'apps.image'

urlpatterns = [
    path('api-v1/list_image/', viewsets.ImageList.as_view(), name='image_list_json'),
]
