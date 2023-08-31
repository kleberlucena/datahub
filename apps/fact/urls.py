from django.urls import path

from .views import *

app_name = 'fact'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
]