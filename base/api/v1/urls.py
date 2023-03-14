from django.urls import path

from . import viewsets

app_name = 'base'

urlpatterns = [
    path('suggestions/', viewsets.AddSuggestionView.as_view(), name='add_list_suggestion_json'),
    path('suggestions/<uuid:uuid>/', viewsets.SuggestionUpdateDestroyView.as_view(), name='update_delete_suggestion_json'),
]