from django.urls import path
from . import views



app_name = 'area'

urlpatterns = [
  path('', views.AreaListView.as_view(), name='index'),  
  path('area/list/', views.AreaListView.as_view(), name='area_list'),  
  path('area/add/', views.CreateAreaView.as_view(), name='area_add'), 
  path('<int:pk>/area/update', views.UpdateAreaView.as_view(), name='area_update'),
  path('<int:pk>/area/delete', views.DeleteAreaView.as_view(), name='area_delete'),

#   path('qpp/list/', views.QppListView.as_view(), name='qpp_list'),  
#   path('qpp/add/', views.CreateQppView.as_view(), name='qpp_add'), 
#   path('<int:pk>/qpp/update', views.UpdateQppView.as_view(), name='qpp_update'),
#   path('<int:pk>/qpp/delete', views.DeleteQppView.as_view(), name='qpp_delete'),

#   path('cpr/list/', views.CprListView.as_view(), name='cpr_list'),  
#   path('cpr/add/', views.CreateCprView.as_view(), name='cpr_add'), 
#   path('<int:pk>/cpr/update', views.UpdateCprView.as_view(), name='cpr_update'),
#   path('<int:pk>/cpr/delete', views.DeleteCprView.as_view(), name='cpr_delete'),

# ]