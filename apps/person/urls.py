from django.urls import path

from .views import *
from .api import viewsets

app_name = 'apps.person'

urlpatterns = [
    path('api-v1/list_person/', viewsets.PersonList.as_view(), name='person_list_json'),
]
