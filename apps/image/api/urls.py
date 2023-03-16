from django.urls import path
from global_login_required import login_not_required

from . import viewsets

app_name = 'image_api'

urlpatterns = [
    path('', viewsets.ImageList.as_view(), name='image_list_json'),
    path('<uuid:uuid>/', viewsets.ImageRetrieve.as_view(), name='image_detail'),
]
