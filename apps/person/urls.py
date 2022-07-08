from django.urls import path
from global_login_required import login_not_required

from .views import *
from .api import viewsets

app_name = 'apps.person'

urlpatterns = [
    path('api-v1/', login_not_required(viewsets.PersonList.as_view()), name='list_json'),
    path('api-v1/<uuid:uuid>/', login_not_required(viewsets.PersonRetrieve.as_view()), name='retrieve_json'),
]
