from django.urls import path
from . import views

app_name = 'fact'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('fact-types/', views.FactTypeListView.as_view(), name='fact-type-list'),
    path('fact-types/create/', views.FactTypeCreateView.as_view(), name='fact-type-create'),
    path('fact-types/<int:pk>/update/', views.FactTypeUpdateView.as_view(), name='fact-type-update'),
    path('fact-types/<int:pk>/delete/', views.FactTypeDeleteView.as_view(), name='fact-type-delete'),
    
    path('facts/', views.FactListView.as_view(), name='fact-list'),
    path('facts/create/', views.FactCreateView.as_view(), name='fact-create'),
    path('facts/<int:pk>/update/', views.FactUpdateView.as_view(), name='fact-update'),
    path('facts/<int:pk>/delete/', views.FactDeleteView.as_view(), name='fact-delete'),
    
    path('fact-images/', views.FactImageListView.as_view(), name='fact-image-list'),
    path('fact-images/create/', views.FactImageCreateView.as_view(), name='fact-image-create'),
    path('fact-images/<int:pk>/update/', views.FactImageUpdateView.as_view(), name='fact-image-update'),
    path('fact-images/<int:pk>/delete/', views.FactImageDeleteView.as_view(), name='fact-image-delete'),
    
    # Add URLs for other models as needed
]