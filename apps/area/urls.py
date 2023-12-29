from django.urls import path
from . import views



app_name = 'area'

urlpatterns = [
  path('', views.AreaListView.as_view(), name='index'),  
  path('area/list/', views.AreaListView.as_view(), name='area_list'),  
  path('area/add/', views.CreateAreaView.as_view(), name='area_add'), 
  path('<int:pk>/area/update', views.UpdateAreaView.as_view(), name='area_update'),
  path('<int:pk>/area/delete', views.DeleteAreaView.as_view(), name='area_delete'),
  path('<int:pk>/area/detail', views.DetailAreaView.as_view(), name='area_detail'),

]