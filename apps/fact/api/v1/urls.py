from django.urls import path

from . import viewsets

app_name = 'apps.fact'

urlpatterns = [
    path('fact-types/', viewsets.FactTypeListViewSet.as_view(), name='fact_type_json'),
    path('', viewsets.AddFactListView.as_view(), name='add_list_fact_json'),
    path('<uuid:uuid>/', viewsets.FactRetrieveDestroyView.as_view(), name='fact_retrieve_json'),
]