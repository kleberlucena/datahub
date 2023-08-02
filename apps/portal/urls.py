from django.urls import path

from .views import *

app_name = 'portal'

urlpatterns = [
    path('api-v1/entity_list_json/', EntityListJson.as_view(), name='entity_list_json'),
    path('list_entity/', EntityListView.as_view(), name='list_entity'),
    path('task-military-api-portal/', TaskGetMilitaryFromPortalView.as_view(), name='task_military_api_portal'),
    path('task-entity-api-portal/', TaskGetEntityFromPortalView.as_view(), name='task_entity_api_portal'),
    path('command_portal/', ComandosAPIPortalView.as_view(), name='command_portal'),
    path('search-military/', SearchMilitaryView.as_view(), name='search_military'),



]
