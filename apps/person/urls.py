from django.urls import path

from .views import *
from .api import viewsets

app_name = 'apps.person'

urlpatterns = [
    path('api-v1/', viewsets.PersonList.as_view(), name='list_json'),
    path('api-v1/<uuid:uuid>/', viewsets.PersonRetrieve.as_view(), name='retrieve_json'),
]
