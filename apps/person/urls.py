from django.urls import path

from .views import *

app_name = 'person'

urlpatterns = [
    path('api-v1/person_list_json/', PersonListJson.as_view(), name='person_list_json'),
    path('list_person/', PersonListView.as_view(), name='list_person'),
    path('task-tattoo-api-person/', TaskSetEntityFromTattooView.as_view(), name='task-tattoo-api-person'),
    path('task-nickname-api-person/', TaskSetEntityFromNicknameView.as_view(), name='task-nickname-api-person'),
    path('task-face-api-person/', TaskSetEntityFromFaceView.as_view(), name='task-face-api-person'),
    path('task-physical-api-person/', TaskSetEntityFromPhysicalView.as_view(), name='task-physical-api-person'),
    path('task-person-api-person/', TaskSetEntityFromPersonView.as_view(), name='task-person-api-person'),
    path('command_person/', ComandosAPIPersonView.as_view(), name='command_person'),
    path('search-person/', SearchPersonView.as_view(), name='search_person'),



]
