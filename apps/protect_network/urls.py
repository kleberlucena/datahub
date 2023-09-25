from django.urls import path
from . import views


app_name = 'protect_network'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('estabelishment/', views.EstablishmentView.as_view(), name='estabelishment'),
]
