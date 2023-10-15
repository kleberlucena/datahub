from django.urls import path
from apps.point_interest.api.v1 import viewsets

app_name = 'point_interest_api'

urlpatterns = [
    path('spots/', viewsets.SpotListView.as_view(), name='list_filter_spots'),
    path('spots-by-type/', viewsets.SpotListbyTypeView.as_view(), name='list_filter_spots_type'),
    path('spots-filter/', viewsets.SpotListFilterView.as_view(), name='list_filter_spots_index'),
]
