from django.urls import path

from .views import *

app_name = 'portal'

urlpatterns = [
    path('api-v1/entity_list_json/', EntityListJson.as_view(), name='entity_list_json'),
    path('list_entity/', EntityListView.as_view(), name='list_entity'),
    path('command_portal/', ComandosAPIPortalView.as_view(), name='command_portal'),
    path('search-military/', SearchMilitaryView.as_view(), name='search_military'),
    path('militaries/', AutocompleteMilitaryView.as_view(), name='list_militaries'),
]
