from django.urls import path
from global_login_required import login_not_required

from .views import *
from .api import viewsets

app_name = 'apps.image'

urlpatterns = [
    path('', viewsets.ImageList.as_view(), name='image_list_json'),
    path('<uuid:uuid>/', viewsets.ImageRetrieve.as_view(), name='image_detail'),
]
