from django.urls import path
from global_login_required import login_not_required

from .views import *
from .api import viewsets

app_name = 'apps.image'

urlpatterns = [
    path('api-v1/list_image/', viewsets.ImageList.as_view(), name='image_list_json'),
]
