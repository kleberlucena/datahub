from django.urls import path
from apps.protect_network.api.v1 import viewsets

app_name = 'protect_network_api'

urlpatterns = [
    path('spots/', viewsets.SpotListView.as_view(), name='list_filter_spots'),
    path('spots-by-type/', viewsets.SpotListbyTypeView.as_view(), name='list_filter_spots_type'),
    path('spots-by-network/', viewsets.SpotListbyNetworkView.as_view(), name='list_filter_spots_network'),
    path('spots-filter/', viewsets.SpotListFilterView.as_view(), name='list_filter_spots_index'),
]
